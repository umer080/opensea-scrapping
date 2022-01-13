#!/usr/bin/env python
# coding: utf-8

# In[5]:


import time
from scrapingbee import ScrapingBeeClient
client = ScrapingBeeClient(api_key='NK1MMOQX7SEUQR57SNH6CEXNCSVPLLN953JY75A1BZBZHVQHEM04CJKTEGD0ARHFWTPU2EW4T6KFCS0N')
response = client.get('https://opensea.io/collection/boredapeyachtclub',
                    )

print('Response HTTP Status Code: ', response.status_code)
page_html = response.content
#print('Response HTTP Response Body: ', page_html)


# In[6]:


from bs4 import BeautifulSoup
from lxml import etree #alternative of xpaths in beautifulsoup
soup_2 = BeautifulSoup(page_html, "html.parser")
lxml_text_2 = etree.HTML(str(soup_2))
#print(soup.prettify)


# In[7]:


#task-2

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
for i in range(2,4): #loop to scrap all articles
    for href in soup_2.select("#main > div > div > div.Blockreact__Block-sc-1xf18x6-0.dBFmez > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.dBFmez.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div > div:nth-child("+str(i)+") > div > article > a"):
        link = href.get('href')
        print("Scraping article #",i)
        print("The article page link is : ", link)

    #clicking article
    response_article_html = client.get('https://opensea.io'+ link,
                        )
    response_article_html = BeautifulSoup(response_article_html.content, "html.parser")
    article_lxml_text = etree.HTML(str(response_article_html)) 

    article_price = article_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div/section/div[2]/div[2]/div[2]/div") 
    article_price = article_price[0].text
    article_price = article_price.replace("($","")
    article_price = article_price.replace(")","")
    NFT_details["price"] = article_price

    article_expiry = article_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div/section/div[1]/div[1]/div/div/span[2]")
    article_expiry = article_expiry[0].text
    article_expiry = article_expiry.replace(" \n","")
    NFT_details["expiry"] = article_expiry


    owner_details = {} 

    name = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/section[2]/div[1]/div/a/span')
    name = name[0].text
    owner_details["name"] = name

    #extracting owner name and address by going in page
    for href in response_article_html.select("#main > div > div > div > div.fresnel-container.fresnel-greaterThanOrEqual-lg > div > div.item--wrapper > div.item--main > section.item--counts > div.Blockreact__Block-sc-1xf18x6-0.Flexreact__Flex-sc-1twd32i-0.FlexColumnreact__FlexColumn-sc-1wwz3hp-0.VerticalAlignedreact__VerticalAligned-sc-b4hiel-0.CenterAlignedreact__CenterAligned-sc-cjf6mn-0.dLdEmb.jYqxGr.ksFzlZ.iXcsEj.cgnEmv > div > a"):
        owner_link = href.get('href')
        print("The owner page link is : ", owner_link)


    #clicking owner
    response_owner_page_html = client.get('https://opensea.io'+ owner_link,
                        )
    soup_owner_page_html = BeautifulSoup(response_owner_page_html.content, "html.parser")
    owner_page_lxml_text = etree.HTML(str(soup_owner_page_html))


    if owner_link.startswith("/0x"): #address check condition
        owner_link=owner_link.replace("/","")
        ETH_address = owner_link
        owner_details["ETH_address"] = ETH_address
        
        opensea_username = owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[2]/div")
        opensea_username = opensea_username[0].text
        owner_details["username"] = opensea_username
        NFT_details["owner"] = owner_details
        main_dict["NFT_details"] = NFT_details
        
        
    else:
        ETH_address = owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[3]/button/div")
        ETH_address = ETH_address[0].text
        owner_details["ETH_address"] = ETH_address

        owner_link=owner_link.replace("/","")
        opensea_username = owner_link
        owner_details["username"] = opensea_username
        NFT_details["owner"] = owner_details
        main_dict["NFT_details"] = NFT_details

    print("----------------------NFT Details----------------------------")
    print(NFT_details)


    '''Current Active Bids'''

    current_active_bids =[] #will have all the data of current active bids
    count =0
    try:
        for i in range(2,4):
            active_bids ={}
                                            
            cab_price = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[2]/div/span')
            cab_price = cab_price[0].text
            cab_price = cab_price.replace("$","")
            active_bids["Bid_price"] = cab_price

            cab_expiry = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[4]/div/span')
            cab_expiry = cab_expiry[0].text
            active_bids["Bid_expiry"] = cab_expiry

            buyer_details={}
            
            cab_buyer = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[5]/div/div/a/span')
            cab_buyer = cab_buyer[0].text
            buyer_details["name"] = cab_buyer
            
            
            
            for buyer in article_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/ul/li["+str(i)+"]/div[5]/div/div/a"):
                    buyer_page_link = buyer.get('href')
                    #print(buyer_page_link)
            #clicking buyer
            response_buyer_page_html = client.get('https://opensea.io'+ buyer_page_link,
                                )
            soup_cab_buyer_page_html = BeautifulSoup(response_buyer_page_html.content, "html.parser")
            cab_buyer_page_lxml_text = etree.HTML(str(soup_cab_buyer_page_html))


            if buyer_page_link.startswith("/0x"):
                buyer_page_link=buyer_page_link.replace("/","")
                ETH_address = buyer_page_link
                buyer_details["ETH_address"] = ETH_address
                
                
                buyer_username = cab_buyer_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[2]/div")
                buyer_username = buyer_username[0].text
                buyer_details["username"] = buyer_username
                
                active_bids["buyer"] = buyer_details
                #active_bids.update(buyer_details)
            
                #current_active_bids.append(active_bids)
                
                
            else:
                ETH_address = cab_buyer_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[3]/button/div")
                ETH_address = ETH_address[0].text
                buyer_details["ETH_address"] = ETH_address

                buyer_page_link=buyer_page_link.replace("/","")
                buyer_username = buyer_page_link
                buyer_details["username"] = buyer_username
                
                active_bids["buyer"] = buyer_details
                #active_bids.update(buyer_details)
                #current_active_bids.append(active_bids)
                
            
            count +=1
            current_active_bids.append(active_bids)
        print("\n----------------------Current Active Bids----------------------------")
        main_dict["offers"] = current_active_bids
        print(current_active_bids , "\n")
        print("Total available CURRENT ACTIVE BIDS are: ", count)
            
            

    except:
        print("\n----------------------Current Active Bids----------------------------")
        main_dict["offers"] = current_active_bids
        print(current_active_bids , "\n")
        print("Total available CURRENT ACTIVE BIDS are: ", count)

    '''sales & transfer history'''

    sales_history =[]
    transfer_history =[]
    sales_count = 0
    transfer_count=0
    # sales_html = response.content
    # sales_soup = BeautifulSoup(sales_html, "html.parser")
    # sales_lxml = etree.HTML(str(sales_soup))

    try:
        for i in range(2,10):
            sales ={}
            transfer ={}
            outer_details = {}
            outer_details_t={}
            
            event = article_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[1]/span")
            event = event[0].text
            print(event)
            if event == "Sale": #event check (Sales or transfer)
                #print("Sale event")
                date_of_sale = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[5]/div/a/text()') 
                date_of_sale = date_of_sale[0]
                outer_details["date_of_sale"] = date_of_sale

                sale_price = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[2]/div/div/div[2]/text()') 
                sale_price = sale_price[0]
                sale_price=sale_price.replace("['","")
                sale_price=sale_price.replace(" ]","")
                outer_details["sale_price_ETH"] = sale_price
                
                old_owner = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[3]/div/a/span') 
                old_owner = old_owner[0].text
                sales["name"] = old_owner
                    #old owner page
                for old_owner in article_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[3]/div/a"):
                    old_owner_details_link = old_owner.get('href')
                    #print("Old owner")
                    #print(old_owner_details_link)
                        
                    #clicking owner
                    old_owner_page_html = client.get('https://opensea.io'+ old_owner_details_link,
                                        )
                    soup_old_owner_page_html = BeautifulSoup(old_owner_page_html.content, "html.parser")
                    old_owner_page_lxml_text = etree.HTML(str(soup_old_owner_page_html))
                    #time.sleep(5)
                    
                    if old_owner_details_link.startswith('/0x'):
                        old_owner_details_link=old_owner_details_link.replace("/","")
                        old_owner_address = old_owner_details_link
                        sales["ETH_address"] = old_owner_address
                        
                        old_owner_username = old_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[2]/div")
                        old_owner_username = old_owner_username[0].text
                        sales["username"] = old_owner_username
                        
                        outer_details["old_owner"] = sales
                        #print("2: ",sales_old_owner_details)
                    else:
                        old_owner_address = old_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[3]/button/div")
                        old_owner_address = old_owner_address[0].text
                        sales["ETH_address"] = old_owner_address
                        
                        old_owner_details_link=old_owner_details_link.replace("/","")
                        old_owner_username = old_owner_details_link
                        sales["username"] = old_owner_username
                        
                        outer_details["old_owner"] = sales
                        #print("3: ",sales_old_owner_details)

                    new_owner_details={}
                    
                    new_owner = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[4]/div/a/span') 
                    new_owner = new_owner[0].text
                    new_owner_details["name"] = new_owner
                    #outer_details["new_owner"]=sales
                    
                    
                    #new owner pages
                    
                    for new_owner in article_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[4]/div/a"):
                        new_owner_details_link = new_owner.get('href')
                        #print("New owner")
                        #print(new_owner_details_link)
                    
                        #  print("*************New Owner Link**************\n")
                        #  print(new_owner_details_link)
                    
                    #clicking owner
                    new_owner_page_html = client.get('https://opensea.io'+ new_owner_details_link,
                                        )
                    soup_new_owner_page_html = BeautifulSoup(new_owner_page_html.content, "html.parser")
                    new_owner_page_lxml_text = etree.HTML(str(soup_new_owner_page_html))
                    
                    if new_owner_details_link.startswith('/0x'):
                        new_owner_details_link=new_owner_details_link.replace("/","")
                        new_owner_address = new_owner_details_link
                        new_owner_details["ETH_address"] = new_owner_address
                        
                        new_owner_username = new_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[2]/div")
                        new_owner_username = new_owner_username[0].text
                        new_owner_details["user_name"] = new_owner_username
                        
                        outer_details["new_owner"] = new_owner_details
                    else:
                        new_owner_address = new_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[3]/button/div")
                        new_owner_address = new_owner_address[0].text
                        new_owner_details["ETH_address"] = new_owner_address
                        
                        new_owner_details_link=new_owner_details_link.replace("/","")
                        new_owner_username = new_owner_details_link
                        new_owner_details["username"] = new_owner_username
                        outer_details["new_owner"] = new_owner_details

                    sales_count +=1
                    
                sales_history.append(outer_details)
            
            elif event == "Transfer":
                date_of_sale = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[5]/div/a/text()') 
                date_of_sale = date_of_sale[0]
                outer_details_t["date_of_sale"] = date_of_sale

                # sale_price = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[2]/div/div/div[2]/text()') 
                # sale_price = sale_price[0]
                # sale_price=sale_price.replace("['","")
                # sale_price=sale_price.replace(" ]","")
                sale_price = ""
                outer_details_t["sale_price_ETH"] = sale_price
                
                old_owner = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[3]/div/a/span') 
                old_owner = old_owner[0].text
                transfer["name"] = old_owner
                    #old owner page
                for old_owner in article_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[3]/div/a"):
                    old_owner_details_link = old_owner.get('href')

                        
                    #clicking owner
                    old_owner_page_html = client.get('https://opensea.io'+ old_owner_details_link,
                                        )
                    soup_old_owner_page_html = BeautifulSoup(old_owner_page_html.content, "html.parser")
                    old_owner_page_lxml_text = etree.HTML(str(soup_old_owner_page_html))
                    
                    if old_owner_details_link.startswith('/0x'):
                        old_owner_details_link=old_owner_details_link.replace("/","")
                        old_owner_address = old_owner_details_link
                        transfer["ETH_address"] = old_owner_address
                        
                        old_owner_username = old_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[2]/div")
                        old_owner_username = old_owner_username[0].text
                        transfer["username"] = old_owner_username
                        
                        outer_details_t["old_owner"] = transfer
                       
                    else:
                        old_owner_address = old_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[3]/button/div")
                        old_owner_address = old_owner_address[0].text
                        transfer["ETH_address"] = old_owner_address
                        
                        old_owner_details_link=old_owner_details_link.replace("/","")
                        old_owner_username = old_owner_details_link
                        transfer["username"] = old_owner_username
                        
                        outer_details_t["old_owner"] = transfer
                       

                    new_owner_details={}
                    
                    new_owner = article_lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[4]/div/a/span') 
                    new_owner = new_owner[0].text
                    new_owner_details["name"] = new_owner
                    
                    
                    #new owner pages
                    
                    for new_owner in article_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[4]/div/a"):
                        new_owner_details_link = new_owner.get('href')
                        #print("New owner")
                        #print(new_owner_details_link)
                    
                    
                    #clicking owner
                    new_owner_page_html = client.get('https://opensea.io'+ new_owner_details_link,
                                        )
                    soup_new_owner_page_html = BeautifulSoup(new_owner_page_html.content, "html.parser")
                    new_owner_page_lxml_text = etree.HTML(str(soup_new_owner_page_html))
                    
                    if new_owner_details_link.startswith('/0x'):
                        new_owner_details_link=new_owner_details_link.replace("/","")
                        new_owner_address = new_owner_details_link
                        new_owner_details["ETH_address"] = new_owner_address
                        
                        new_owner_username = new_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[2]/div")
                        new_owner_username = new_owner_username[0].text
                        new_owner_details["user_name"] = new_owner_username
                        
                        outer_details["new_owner"] = new_owner_details
                    else:
                        new_owner_address = new_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[3]/button/div")
                        new_owner_address = new_owner_address[0].text
                        new_owner_details["ETH_address"] = new_owner_address
                        
                        new_owner_details_link=new_owner_details_link.replace("/","")
                        new_owner_username = new_owner_details_link
                        new_owner_details["username"] = new_owner_username
                        outer_details_t["new_owner"] = new_owner_details

                    transfer_count +=1
                    
                transfer_history.append(outer_details_t)
            
                    
        print("\n----------------------Sales History----------------------------")
        main_dict["sales"] = sales_history
        print(sales_history, "\n")
        print("Total available Sale Events are: ", sales_count , "\n")
        
        print("\n----------------------Transfer History----------------------------")
        main_dict["transfer"] = transfer_history
        print(transfer_history, "\n")
        print("Total available Transfer Events are: ", transfer_count , "\n")
                    
                
    except:
        print("\n----------------------Sales History----------------------------")
        main_dict["sales"] = sales_history
        print(sales_history, "\n")
        print("Total available Sale Events are: ", sales_count , "\n")
        
        print("\n----------------------Transfer History----------------------------")
        main_dict["transfer"] = transfer_history
        print(transfer_history, "\n")
        print("Total available Transfer Events are: ", transfer_count , "\n")


print("----------------------Main Dict----------------------------")
print(main_dict)

