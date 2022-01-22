


def common(soup,lxml_text):
    
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
        #main_dict["NFT_details"] = NFT_details
        #main_dict["NFT_details"].update(NFT_details)

    #main_dict
    print("----------------------NFT Details----------------------------")
    print(main_dict)

    # '''Current Active Bids'''

    current_active_bids =[] #will have all the data of current active bids
    count =0
    try:
        for i in range(2,4):
            active_bids ={}
            
            try:           #articles                     
                cab_price = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[2]/div/span')
                cab_price = cab_price[0].text
                cab_price = cab_price.replace("$","")
                active_bids["Bid_price"] = cab_price
                
                cab_expiry = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[4]/div/span')
                cab_expiry = cab_expiry[0].text
                active_bids["Bid_expiry"] = cab_expiry
                buyer_details={}
                
                cab_buyer = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[5]/div/div/a/span')
                cab_buyer = cab_buyer[0].text
                buyer_details["name"] = cab_buyer
                
                
                
                for buyer in lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/ul/li["+str(i)+"]/div[5]/div/div/a"):
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
                    
                
                    count +=1
                current_active_bids.append(active_bids)
               
            except:
                cab_price = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[2]/div/span')
                cab_price = cab_price[0].text
                cab_price = cab_price.replace("$","")
                active_bids["Bid_price"] = cab_price
                
                cab_expiry = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[4]/div/span')
                cab_expiry = cab_expiry[0].text
                active_bids["Bid_expiry"] = cab_expiry
                
            

                buyer_details={}
                
                cab_buyer = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div/div/div/ul/li['+str(i)+']/div[5]/div/div/a/span')
                cab_buyer = cab_buyer[0].text
                buyer_details["name"] = cab_buyer
                
                
                
                for buyer in lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div/div/div/ul/li["+str(i)+"]/div[5]/div/div/a"):
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

    try:
        for i in range(2,4):
            sales ={}
            transfer ={}
            outer_details = {}
            outer_details_t={}
            
            event = lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[1]/span")
            event = event[0].text
            print(event)
            if event == "Sale": #event check (Sales or transfer)
                #print("Sale event")
                date_of_sale = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[5]/div/a/text()') 
                date_of_sale = date_of_sale[0]
                outer_details["date_of_sale"] = date_of_sale
                
                try:
                    sale_price = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[2]/div/div/div[2]/text()') 
                    #print("Here 2")
                    sale_price = sale_price[0]
                    # print(sale_price)
                    # sale_price=sale_price.replace("['","")
                    # sale_price=sale_price.replace(" ]","")
                    outer_details["sale_price_ETH"] = sale_price
                except:
                    sale_price = ""
                    outer_details["sale_price_ETH"] = sale_price
                
                try:
                    old_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[3]/div/a/span') 
                    old_owner = old_owner[0].text
                    sales["name"] = old_owner
                    
                except:
                    old_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[3]/div/a[1]/span') 
                    old_owner = old_owner[0].text
                    sales["name"] = old_owner
                    
                    #old owner page
                for old_owner in lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[3]/div/a"):
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
                    
                    try:
                        new_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[4]/div/a/span') 
                        new_owner = new_owner[0].text
                        new_owner_details["name"] = new_owner
                        
                    except:
                         new_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[4]/div/a[1]/span') 
                         new_owner = new_owner[0].text
                         new_owner_details["name"] = new_owner
                    #outer_details["new_owner"]=sales
                
                    #new owner pages
                    
                    for new_owner in lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[4]/div/a"):
                        new_owner_details_link = new_owner.get('href')
                        #print("New owner")
                        
                    
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
                date_of_sale = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[5]/div/a/text()') 
                date_of_sale = date_of_sale[0]
                outer_details_t["date_of_sale"] = date_of_sale

              
                sale_price = ""
                outer_details_t["sale_price_ETH"] = sale_price
                
                try:
                    old_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[3]/div/a/span') 
                    old_owner = old_owner[0].text
                    transfer["name"] = old_owner
                except:
                    old_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[3]/div/a[1]/span') 
                    old_owner = old_owner[0].text
                    transfer["name"] = old_owner
                
                        #old owner page
                for old_owner in lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[3]/div/a"):
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
                    
                    try:
                        new_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[4]/div/a/span') 
                        new_owner = new_owner[0].text
                        new_owner_details["name"] = new_owner
                    except:
                        new_owner = lxml_text.xpath('/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div['+str(i)+']/div[4]/div/a[1]/span') 
                        new_owner = new_owner[0].text
                        new_owner_details["name"] = new_owner    
                    
                    #new owner pages
                    
                    for new_owner in lxml_text.xpath("/html/body/div[1]/div[1]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div["+str(i)+"]/div[4]/div/a"):
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
    return main_dict