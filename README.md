# crypto-buyauto-discord
A program that buys crypto in binance from signals in discord
The program takes the last message from a discord server and filters it and takes the information, then uses the binance api to place the order.Therefore, if you run a program for the first time, it will make the order from the last message, so be careful.After 30 seconds it checks for a new message, if not it continues to wait for a new message
INSTALATION:
How to use it. You must have python installed and 
pip install python-binance 
pip install jsonlib 
pip install requests

SETUP:
Go to settings.py and and you have to put your api key and secret.
Тhe minimum purchase for one transaction must be over 5$ if it is less it will not go through you can change the margin from settings.


HOW TO MAKE IT RUN 24/7:

You can use google cloud and create VM machine(first 3 months free) - https://www.youtube.com/watch?v=azh8J0acu6A
You can use Repl.it but be careful you have to protect your api keys in secret enviroment (Free) - https://www.youtube.com/watch?v=t7FsGcEUoRM




DISCLAIMER:
The program is still in beta so you can test it at https://testnet.binancefuture.com/en/futures/ , but if you dont want that you can change it from True to False in settings.
In the future I will make it possible to be from more than one server channel for now it only allows one and I will make stoploss and takeprofit as well as support in bitget

You have to go trough all the coins in binance and select ISOLATED!!!!!!

CONTACT ME:
If you have any questions you can message me in discord: Captain_Koalaツ#1665
