#!/usr/bin/env python
# coding: utf-8

# In[41]:


import time
from scrapingbee import ScrapingBeeClient
client = ScrapingBeeClient(api_key='WUZ24G0V4BQDPQQP4OAJZNVS3UOGOG3F1EROO35MHYN5QRIWYPOKLONRZMWYSCWKM8U9R1J5GSYN4JC5')
response = client.get('https://opensea.io/assets/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/4949',
                    )

print('Response HTTP Status Code: ', response.status_code)
page_html = response.content
#print('Response HTTP Response Body: ', page_html)


# In[42]:


from bs4 import BeautifulSoup
from lxml import etree #alternative of xpaths in beautifulsoup
soup = BeautifulSoup(page_html, "html.parser")
lxml_text = etree.HTML(str(soup))
#print(soup.prettify)


# In[51]:


'''NFT Parser'''

main_dict={} #will contain all data
NFT_details = {}

try:
    price = soup.find(class_='Overflowreact__OverflowContainer-sc-10mm0lu-0 gjwKJf Price--fiat-amount Price--fiat-amount-secondary')
    price = price.get_text()
    price=price.replace("($","")
    price=price.replace(")","")
    NFT_details["NFT_price"] = price
except:
    price=""
    NFT_details["NFT_price"] = price

owner_details = {} 

name = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/section[2]/div[1]/div/a/span')
name = name[0].text
owner_details["name"] = name


#extracting owner name and address by going in page
for href in soup.select("#main > div > div > div > div.fresnel-container.fresnel-greaterThanOrEqual-lg > div > div.item--wrapper > div.item--main > section.item--counts > div.Blockreact__Block-sc-1xf18x6-0.Flexreact__Flex-sc-1twd32i-0.FlexColumnreact__FlexColumn-sc-1wwz3hp-0.VerticalAlignedreact__VerticalAligned-sc-b4hiel-0.CenterAlignedreact__CenterAligned-sc-cjf6mn-0.dLdEmb.jYqxGr.ksFzlZ.iXcsEj.cgnEmv > div > a"):
    link = href.get('href')
    print("The owner page link is : ", link)


link
    
#clicking owner
response_owner_page_html = client.get('https://opensea.io'+ link,
                    )
soup_owner_page_html = BeautifulSoup(response_owner_page_html.content, "html.parser")
owner_page_lxml_text = etree.HTML(str(soup_owner_page_html))


if link.startswith("/0x"):
    link=link.replace("/","")
    ETH_address = link
    owner_details["ETH_address"] = ETH_address
    
    opensea_username = owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[2]/div")
    opensea_username = opensea_username[0].text
    owner_details["username"] = opensea_username
    main_dict.update(NFT_details)
    main_dict["owner"] = owner_details
    
    
else:
    ETH_address = owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[3]/button/div")
    ETH_address = ETH_address[0].text
    owner_details["ETH_address"] = ETH_address

    link=link.replace("/","")
    opensea_username = link
    owner_details["username"] = opensea_username
    main_dict.update(NFT_details)
    main_dict["owner"] = owner_details
    main_dict["NFT_details"] = NFT_details
    #main_dict["NFT_details"].update(NFT_details)

#main_dict
print("----------------------NFT Details----------------------------")
print(main_dict)

'''Current Active Bids'''
current_active_bids =[]
count =0
try:
    for i in range(2,5):
        active_bids ={}
        
        cab_price = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[2]/div/span')
        cab_price = cab_price[0].text
        cab_price = cab_price.replace("$","")
        active_bids["Bid_price"] = cab_price

        cab_expiry = lxml_text.xpath('//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[4]/div/span')
        cab_expiry = cab_expiry[0].text
        active_bids["Bid_expiry"] = cab_expiry

        cab_buyer = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[5]/div/div/a/span')
        cab_buyer = cab_buyer[0].text
        active_bids["Bid_buyer"] = cab_buyer

        current_active_bids.append(active_bids)
        count +=1
    # print("\n----------------------Current Active Bids----------------------------")
    # print(current_active_bids)

except:
    
    print("\n----------------------Current Active Bids----------------------------")
    main_dict["offers"] = current_active_bids
    print(current_active_bids , "\n")
    print("Total available CURRENT ACTIVE BIDS are: ", count)


'''Sales history'''

sales_history =[]
transfer_history =[]
sales_count = 0
transfer_count=0


try:
    for i in range(2,100):
        sales ={}
        transfer ={}
        outer_details = {}
        outer_details_t={}
        
        event = lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[1]/span")
        event = event[0].text
        if event == "Sale":
            date_of_sale = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[5]/div/a/text()') 
            date_of_sale = date_of_sale[0]
            outer_details["date_of_sale"] = date_of_sale

            sale_price = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[2]/div/div/div[2]/text()') 
            sale_price = sale_price[0]
            sale_price=sale_price.replace("['","")
            sale_price=sale_price.replace(" ]","")
            outer_details["sale_price_ETH"] = sale_price
            
            old_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[3]/div/a/span') 
            old_owner = old_owner[0].text
            sales["name"] = old_owner
                #old owner page
            for old_owner_details in soup.select("#main > div > div > div > div.fresnel-container.fresnel-greaterThanOrEqual-lg > div > div.item--frame.item--trading-history > div > div > div > div > div > div > div.Scrollboxreact__DivContainer-sc-1b04elr-0.ddtCpj.EventHistory--container > div > div:nth-child("+str(i)+") > div:nth-child(3) > div > a"):
                old_owner_details_link = old_owner_details.get('href')
                    #  print("*************Old Owner Link**************")
                    #  print(old_owner_details_link)
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


                new_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[4]/div/a/span') 
                new_owner = new_owner[0].text
                sales["name"] = new_owner
                
                
                #new owner pages
                for new_owner_details in soup.select("#main > div > div > div > div.fresnel-container.fresnel-greaterThanOrEqual-lg > div > div.item--frame.item--trading-history > div > div > div > div > div > div > div.Scrollboxreact__DivContainer-sc-1b04elr-0.ddtCpj.EventHistory--container > div > div:nth-child("+str(i)+") > div:nth-child(4) > div > a"):
                    new_owner_details_link = new_owner_details.get('href')
                    #  print("*************New Owner Link**************\n")
                    #  print(new_owner_details_link)
                
                #clicking owner
                new_owner_page_html = client.get('https://opensea.io'+ new_owner_details_link,
                                    )
                soup_new_owner_page_html = BeautifulSoup(new_owner_page_html.content, "html.parser")
                new_owner_page_lxml_text = etree.HTML(str(soup_new_owner_page_html))
                #time.sleep(5)
                
                if new_owner_details_link.startswith('/0x'):
                    new_owner_details_link=new_owner_details_link.replace("/","")
                    new_owner_address = new_owner_details_link
                    sales["ETH_address"] = new_owner_address
                    
                    new_owner_username = new_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[2]/div")
                    new_owner_username = new_owner_username[0].text
                    sales["user_name"] = new_owner_username
                    
                    outer_details["new_owner"] = sales
                else:
                    new_owner_address = new_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[3]/button/div")
                    new_owner_address = new_owner_address[0].text
                    sales["ETH_address"] = new_owner_address
                    
                    new_owner_details_link=new_owner_details_link.replace("/","")
                    new_owner_username = new_owner_details_link
                    sales["username"] = new_owner_username
                    outer_details["new_owner"] = sales

                
                sales_history.append(outer_details)
                
                sales_count +=1
            
        elif event=="Transfer":
            date_of_sale = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[5]/div/a/text()') 
            date_of_sale = date_of_sale[0]
            outer_details_t["date_of_sale"] = date_of_sale

            # sale_price = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[2]/div/div/div[2]/text()') 
            # sale_price = sale_price[0]
            # sale_price=sale_price.replace("['","")
            # sale_price=sale_price.replace(" ]","")
            sale_price =""
            outer_details_t["sale_price_ETH"] = sale_price

                
            old_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[3]/div/a/span') 
            old_owner = old_owner[0].text
            transfer["name"] = old_owner
            
                #old owner page
            for old_owner_details in soup.select("#main > div > div > div > div.fresnel-container.fresnel-greaterThanOrEqual-lg > div > div.item--frame.item--trading-history > div > div > div > div > div > div > div.Scrollboxreact__DivContainer-sc-1b04elr-0.ddtCpj.EventHistory--container > div > div:nth-child("+str(i)+") > div:nth-child(3) > div > a"):
                old_owner_details_link = old_owner_details.get('href')
                    #  print("*************Old Owner Link**************")
                    #  print(old_owner_details_link)
                
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
                    


                new_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[4]/div/a/span') 
                new_owner = new_owner[0].text
                transfer["name"] = new_owner
                
                #new owner pages
                for new_owner_details in soup.select("#main > div > div > div > div.fresnel-container.fresnel-greaterThanOrEqual-lg > div > div.item--frame.item--trading-history > div > div > div > div > div > div > div.Scrollboxreact__DivContainer-sc-1b04elr-0.ddtCpj.EventHistory--container > div > div:nth-child("+str(i)+") > div:nth-child(4) > div > a"):
                    new_owner_details_link = new_owner_details.get('href')
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
                    transfer["ETH_address"] = new_owner_address
                    
                    new_owner_username = new_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[2]/div")
                    new_owner_username = new_owner_username[0].text
                    transfer["user_name"] = new_owner_username
                    
                    outer_details_t["new_owner"] = transfer
                else:
                    new_owner_address = new_owner_page_lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div[1]/div[3]/div[3]/button/div")
                    new_owner_address = new_owner_address[0].text
                    transfer["ETH_address"] = new_owner_address
                    
                    new_owner_details_link=new_owner_details_link.replace("/","")
                    new_owner_username = new_owner_details_link
                    transfer["username"] = new_owner_username
                    outer_details_t["new_owner"] = transfer

                
                transfer_history.append(outer_details_t)
                
                transfer_count +=1
                
                     
except:
    print("\n----------------------Sales History----------------------------")
    main_dict["sales"] = sales_history
    print(sales_history, "\n")
    print("Total available Sale Events are: ", sales_count , "\n")
    
    print("\n----------------------Transfer History----------------------------")
    main_dict["transfer"] = transfer_history
    print(transfer_history, "\n")
    print("Total available Transfer Events are: ", transfer_count , "\n")
    

print("All details: \n", main_dict)

