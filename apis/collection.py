from app import celery

from flask_restful import reqparse, Resource
from utils.amazon_common import custom_json_response
import json
import requests
import time
from flask import Flask 
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from app import cache
from ast  import literal_eval as ev
from .orderbook import common

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

collection_parser = reqparse.RequestParser()

collection_parser.add_argument(
    "collection", dest="collection",
    location='json', required=True,
    help='collection is missing',
    )


class Collection(Resource):

    @auth.login_required
    def post(self):
        try:
            print("here", flush=True)
            flag=True
            args = collection_parser.parse_args()
            print(args)
            payload = args.collection
            # payload=ev(payload)
            print(payload)
            task_2.delay()

            return custom_json_response(payload, "Success", 200)
        except Exception as err:
            return custom_json_response({}, str(err), 500)


@celery.task(bind=True, trail=True)
def task_2(self, payload):
    response = client.get('https://opensea.io/collection/boredapeyachtclub',
                    )
    print('Response HTTP Status Code: ', response.status_code)
    page_html = response.content
    
    from bs4 import BeautifulSoup
    from lxml import etree #alternative of xpaths in beautifulsoup
    soup_2 = BeautifulSoup(page_html, "html.parser")
    lxml_text_2 = etree.HTML(str(soup_2))
    
    '''Collection Details'''
    
    main_dict ={} #main dict having all article details
    bored_ape_details={}
    items = lxml_text_2.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[2]/div[5]/div/div[1]/a/div/div[1]/span/div")
    items = items[0].text
    bored_ape_details["items"] = items

    #optional fields
    owners = lxml_text_2.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[2]/div[5]/div/div[2]/a/div/div[1]/span/div") #extracting owners
    owners = owners[0].text
    bored_ape_details["owners"] = owners

    volume_traded = lxml_text_2.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[2]/div[5]/div/div[4]/a/div/div[1]/span/div") #extracting volumn_trades
    volume_traded = volume_traded[0].text
    bored_ape_details["volume_traded"] = volume_traded

    main_dict["Collection"] = bored_ape_details

    #Collection details
    print("----------------------Collection Details----------------------------")
    print(bored_ape_details)
    
    '''NFT details'''

    NFT_details = {} #will have NFT details
    for i in range(2,3): #loop to scrap all articles
        for href in soup_2.select("#main > div > div > div.Blockreact__Block-sc-1xf18x6-0.dBFmez > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.dBFmez.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div > div:nth-child("+str(i)+") > div > article > a"):
            link = href.get('href')
            print("Scraping article #",i)
            print("The article page link is : ", link)
            
        #clicking article
        response_article_html = client.get('https://opensea.io'+ link,
                            )
        soup = BeautifulSoup(response_article_html.content, "html.parser")
        lxml_text = etree.HTML(str(soup)) 
        
        common(soup,lxml_text)