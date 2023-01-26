import requests
import json
import time
from decimal import Decimal
from settings import api_key,api_secret,discord_autho,balance_margin,testnet1,discord_channel,market_pos,leverage_change
from binance.client import Client
import re
import math

number = 0
quantity1 = 0
quantity_entry1 = 0
quantity2 = 0
quantity_entry2 = 0
usdt_balance = 0
word = 0
position2 = 0
entry_price2=0
entry_price_saver=0
nuumber_tracker = 0
nuumber_tracker1 = 0
client = Client(api_key=api_key, api_secret=api_secret,testnet = testnet1)
def retrieve_last_message(channelid):
    global content
    headers = {
        'authorization': discord_autho
    }
    position = "Position not found"
    r = requests.get(f'https://discord.com/api/v6/channels/{channelid}/messages?limit=3', headers=headers)
    jsonn = json.loads(r.text)
    last_message = jsonn[-3]
    content = last_message['content']
    lines = content.strip().split("\n")
    instrument = lines[0].strip()
    target = '0'
    stoploss = '0'
    entry_price = '0'
    for line in lines:
        if "Target 1:" in line:
             target = line.split(":")[1].strip().split("(")[0]
        elif "Stoploss:" in line:
            stoploss = line.split(":")[1].strip().split("(")[0]

    match = re.search("Entry: ([\d.]+)", content)
    if match:
        entry_price = float(match.group(1))
        
    
    for line in lines:
        long_split = line.split("BUY/LONG")
        short_split = line.split("SELL/SHORT")
        if len(long_split) > 1:
            position = "BUY/LONG"
            break
        elif len(short_split) > 1:
            position = "SELL/SHORT"
            break

        
    return content,instrument,target,stoploss,position,entry_price
content, instrument, target, stoploss,position,entry_price = retrieve_last_message(discord_channel)

def send_message_to_user(message):
    # code to send message to user
    pass   

bought_symbols = []
while True:
    
    for item in client.futures_account_balance():
        if item['asset'] == 'USDT':
            usdt_balance = float(item['balance'])
            break
        print(usdt_balance)
    
    content, instrument, target, stoploss, position, entry_price = retrieve_last_message(discord_channel)
    modified_string = instrument.replace("$", "") + "USDT"
    print(modified_string)
    key = f"https://api.binance.com/api/v3/ticker/price?symbol={modified_string}"
    data = requests.get(key)  
    data = data.json()
    if 'price' in data.keys():
        last_price = float(data['price'])
    else:
        word = 1
        

    
    if modified_string in ["SHIBUSDT", "LUNCUSDT", "XECUSDT"]:
        modified_string = "1000" + modified_string

        
        stoploss *= 1000
        number = 1
        
        entry_price *=1000
        
        last_price *= 1000


    if word == 0:
        quantity1 = (usdt_balance * balance_margin) / last_price
        if quantity1 > 1:
            quantity2 = math.floor(quantity1)
        elif quantity_entry1 <1:
            quantity_entry2 = quantity1 
        quantity_entry1 =(usdt_balance * balance_margin) / entry_price
        if quantity_entry1 >1:
            quantity_entry2= math.floor(quantity_entry1)
        elif quantity_entry1 <1:
            quantity_entry2 = quantity1 
    else:
        print("No quantity")

    print(quantity2)
    print(position)
    print(quantity_entry2)
    print(modified_string)
    print(stoploss)
    print(target)

    
    
    if modified_string not in bought_symbols:
        nuumber_tracker1 = 0
        nuumber_tracker = 0
        target = float(target.split(" ")[0])
        if number==1:
            target*=1000
            stoploss*=1000
            stoploss = str(stoploss)
            stoploss = stoploss[:stoploss.index(".") + 7]
            
            print(target)
            print(stoploss)
        entry_price2 = entry_price    
        if position == 'BUY/LONG':
            position2 = position
            if market_pos == 'MARKET':
                client.futures_change_leverage(symbol=modified_string, leverage=leverage_change)
                buyorder=client.futures_create_order(symbol=modified_string,side='BUY',marginType='ISOLATED',isIsolated='TRUE',type='MARKET',quantity=quantity2)     
                print("Buying " + modified_string + " at " + str(last_price) + " quantity " + str(quantity2) + ".")
                bought = modified_string
                entry_price_saver = last_price
                buyorderlimit1=client.futures_create_order(symbol=modified_string,side='SELL',type='STOP_MARKET',stopPrice=stoploss,closePosition='true') 
                
                sellorder=client.futures_create_order(symbol=modified_string,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice=target,closePosition='true')

                
            elif market_pos == 'LIMIT':
                client.futures_change_leverage(symbol=modified_string, leverage=leverage_change)
                buyorder=client.futures_create_order(symbol=modified_string,side='BUY',type='LIMIT',marginType='ISOLATED',quantity=quantity_entry2,price = entry_price,timeInForce='GTC')       
                print("Creating BUY LIMIT order " + modified_string + " at  " + str(entry_price) + " quantity " + str(quantity_entry2) + ".")
               
                bought = modified_string
                buyorderlimit1=client.futures_create_order(symbol=modified_string,side='SELL',type='STOP_MARKET',stopPrice=stoploss,closePosition='true') 
                sellorder=client.futures_create_order(symbol=modified_string,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice=target,closePosition='true')
        elif position == 'SELL/SHORT':
            position2 = position
            if market_pos == 'MARKET':
                client.futures_change_leverage(symbol=modified_string, leverage=leverage_change)
                buyorder=client.futures_create_order(symbol=modified_string,side='SELL',type='MARKET',marginType='ISOLATED',quantity=quantity2)  
                print("Selling " + modified_string + " at " + str(last_price) + " quantity " + str(quantity2) + ".")
                entry_price_saver = last_price
                bought = modified_string
                buyorderlimit=client.futures_create_order(symbol=modified_string,side='BUY',type='STOP_MARKET',stopPrice=stoploss,closePosition='true') 
                sellorder=client.futures_create_order(symbol=modified_string,side='BUY',type='TAKE_PROFIT_MARKET',stopPrice=target,closePosition='true')
            elif market_pos == 'LIMIT': 
                client.futures_change_leverage(symbol=modified_string, leverage=leverage_change)
                sellorder=client.futures_create_order(symbol=modified_string,side='SELL',type='LIMIT',marginType='ISOLATED',quantity=quantity_entry2,price= entry_price,timeInForce='GTC')       
                print("Creating SELL LIMIT order " + modified_string + " at  " + str(entry_price) + " quantity " + str(quantity_entry2) + ".")
                bought = modified_string
                buyorderlimit=client.futures_create_order(symbol=modified_string,side='BUY',type='STOP_MARKET',stopPrice=stoploss,closePosition='true') 
                sellorder=client.futures_create_order(symbol=modified_string,side='BUY',type='TAKE_PROFIT_MARKET',stopPrice=target,closePosition='true')
        bought_symbols.append(modified_string)


        
    elif re.search("closing now", content, re.IGNORECASE) and nuumber_tracker < 1:
        print(bought)
        print(last_price)
        
        print(last_price)
        print(entry_price2)
        if position2 == 'SELL/SHORT':
            key = f"https://api.binance.com/api/v3/ticker/price?symbol={bought}"
            data = requests.get(key)  
            data = data.json()
            last_price = float(data['price'])
            sellorder=client.futures_create_order(symbol=bought,side='BUY',type='TAKE_PROFIT_MARKET',stopPrice=last_price,closePosition='true')
            print (sellorder)
            nuumber_tracker +=1
        elif position2 == 'BUY/LONG':
            key = f"https://api.binance.com/api/v3/ticker/price?symbol={bought}"
            data = requests.get(key)  
            data = data.json()
            last_price = float(data['price'])
            sellorder=client.futures_create_order(symbol=bought,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice=last_price,closePosition='true')
            print (sellorder)
            nuumber_tracker +=1
    elif re.search("close now", content, re.IGNORECASE) and nuumber_tracker < 1:

        if position2 == 'SELL/SHORT':
            key = f"https://api.binance.com/api/v3/ticker/price?symbol={bought}"
            data = requests.get(key)  
            data = data.json()
            last_price = float(data['price'])
            sellorder=client.futures_create_order(symbol=bought,side='BUY',type='TAKE_PROFIT_MARKET',stopPrice=last_price,closePosition='true')
            property(sellorder)
            nuumber_tracker +=1
        elif position2 == 'BUY/LONG':
            key = f"https://api.binance.com/api/v3/ticker/price?symbol={bought}"
            data = requests.get(key)  
            data = data.json()
            last_price = float(data['price'])
            sellorder=client.futures_create_order(symbol=bought,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice=last_price,closePosition='true')
            property(sellorder)
            nuumber_tracker +=1

    elif re.search("SL to enty", content, re.IGNORECASE) and nuumber_tracker1 < 1:
        if position2 == 'SELL/SHORT':
            if market_pos == 'MARKET':
                buyorderlimit1=client.futures_create_order(symbol=bought,side='SELL',type='STOP_MARKET',stopPrice=entry_price_saver,closePosition='true')
                print(buyorderlimit1)
                nuumber_tracker1+=1

            elif market_pos == 'LIMIT':
                buyorderlimit=client.futures_create_order(symbol=bought,side='BUY',type='STOP_MARKET',stopPrice=entry_price2,closePosition='true') 
                print(buyorderlimit)
                nuumber_tracker1+=1
        elif position2 == 'BUY/LONG':
            if market_pos == 'MARKET':
                buyorderlimit1=client.futures_create_order(symbol=bought,side='SELL',type='STOP_MARKET',stopPrice=entry_price_saver,closePosition='true')
                print(buyorderlimit1)
                nuumber_tracker1+=1


            elif market_pos == 'LIMIT':
                buyorderlimit1=client.futures_create_order(symbol=bought,side='SELL',type='STOP_MARKET',stopPrice=entry_price2,closePosition='true')
                print(buyorderlimit1)
                nuumber_tracker1+=1

    else:
        send_message_to_user(f"{modified_string} already bought.")
    # Add delay before checking for new messages again
    time.sleep(30)