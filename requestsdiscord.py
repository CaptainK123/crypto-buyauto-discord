import requests
import json
import time
from settings import api_key,api_secret,discord_autho,balance_margin,testnet1,discord_channel,market_pos
from binance.client import Client
import re

usdt_balance = 0
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
    key = "https://api.binance.com/api/v3/ticker/price?symbol=" + modified_string
    print(key)
    data = requests.get(key)  
    data = data.json()
    last_price = float(data['price'])
    if usdt_balance>6:
        quantity = (usdt_balance * balance_margin) / last_price
    elif usdt_balance <5:
        quantity = 0    
    
    quantity = float(round(quantity, 2))
    if usdt_balance>6:
        quantity_entry =(usdt_balance * balance_margin) / entry_price
    elif usdt_balance <5:
        quantity = 0 
    
    
    
    quantity_entry = float(round(quantity, 2))
    
    print(stoploss)
    print(target)
    print(instrument)
    print(balance_margin)
    print(usdt_balance)
    print(quantity)
    print(position)
    print(entry_price)
    if modified_string not in bought_symbols:
        target = float(target.split(" ")[0])

        if position == 'BUY/LONG':
            if market_pos == 'MARKET':
                buyorder=client.futures_create_order(symbol=modified_string,side='BUY',type='MARKET',quantity=quantity)     
                print(buyorder)
                buyorderlimit1=client.futures_create_order(symbol=modified_string,side='SELL',type='STOP_MARKET',stopPrice=stoploss,closePosition='true') 
                sellorderlimit1=client.futures_create_order(symbol=modified_string,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice=target,closePosition='true') 
            elif market_pos == 'LIMIT':
                buyorder=client.futures_create_order(symbol=modified_string,side='BUY',type='LIMIT',quantity=quantity_entry,price = entry_price,timeInForce='GTC')       
                print(buyorder)
                buyorderlimit1=client.futures_create_order(symbol=modified_string,side='SELL',type='STOP_MARKET',stopPrice=stoploss,closePosition='true') 
                sellorderlimit1=client.futures_create_order(symbol=modified_string,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice=target,closePosition='true')
        elif position == 'SELL/SHORT':
            if market_pos == 'MARKET':
                buyorder=client.futures_create_order(symbol=modified_string,side='SELL',type='MARKET',quantity=quantity)  
                print(buyorder)
                buyorderlimit=client.futures_create_order(symbol=modified_string,side='BUY',type='STOP_MARKET',stopPrice=stoploss,closePosition='true') 
                sellorderlimit=client.futures_create_order(symbol=modified_string,side='BUY',type='TAKE_PROFIT_MARKET',stopPrice=target,closePosition='true') 
            elif market_pos == 'LIMIT': 
                sellorder=client.futures_create_order(symbol=modified_string,side='SELL',type='LIMIT',quantity=quantity_entry,price= entry_price,timeInForce='GTC')       
                print(sellorder)
                buyorderlimit=client.futures_create_order(symbol=modified_string,side='BUY',type='STOP_MARKET',stopPrice=stoploss,closePosition='true') 
                sellorderlimit=client.futures_create_order(symbol=modified_string,side='BUY',type='TAKE_PROFIT_MARKET',stopPrice=target,closePosition='true')
 

        



        
        bought_symbols.append(modified_string)
    else:
        send_message_to_user(f"{modified_string} already bought.")
    # Add delay before checking for new messages again
    time.sleep(30)