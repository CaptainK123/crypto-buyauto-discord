import requests
import json
import time
from decimal import Decimal
from settings import api_key,api_secret,discord_autho,balance_margin,testnet1
from binance.client import Client

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

    
    
    for line in lines:
        long_split = line.split("BUY/LONG")
        short_split = line.split("SELL/SHORT")
        if len(long_split) > 1:
            position = "BUY/LONG"
            break
        elif len(short_split) > 1:
            position = "SELL/SHORT"
            break

        
    return content,instrument,target,stoploss,position
content, instrument, target, stoploss,position = retrieve_last_message('637630528056459301')

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
    
    content, instrument, target, stoploss, position = retrieve_last_message('637630528056459301')
    modified_string = instrument.replace("$", "") + "USDT"
    print(modified_string)
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(key)  
    data = data.json()
    last_price = float(data['price'])
    quantity = (usdt_balance * 0.15) / last_price
    
    quantity = float(round(quantity, 2))
    print(stoploss)
    print(target)
    print(instrument)
    print(balance_margin)
    print(usdt_balance)
    print(quantity)
    print(position)
    if modified_string not in bought_symbols:
        target = float(target.split(" ")[0])
        if position == 'BUY/LONG':
            buyorder=client.futures_create_order(symbol=modified_string,side='BUY',type='MARKET',quantity=quantity)     
            print(buyorder)
        elif position == 'SELL/SHORT':
            buyorder=client.futures_create_order(symbol=modified_string,side='SELL',type='MARKET',quantity=quantity)  
            print(buyorder)
              
        



        
        bought_symbols.append(modified_string)
    else:
        send_message_to_user(f"{modified_string} already bought.")
    # Add delay before checking for new messages again
    time.sleep(30)
