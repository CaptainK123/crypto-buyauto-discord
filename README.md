# crypto-buyauto-discord
A program that buys crypto in binance from signals in discord
The program takes the last message from a discord server and filters it and takes the information, then uses the binance api to place the order.Therefore, if you run a program for the first time, it will make the order from the last message, so be careful.After 30 seconds it checks for a new message, if not it continues to wait for a new message



INSTALATION:

You must have python installed and 

pip install python-binance 

pip install jsonlib 

pip install requests

Download both files in 1 folder

SETUP:

Go to settings.py and and you have to put your api key and secret.

Тhe minimum purchase for one transaction must be over 5$ if it is less it will not go through you can change the margin from settings.

You can change the order whether it is market or limit, i.e. buy it immediately or wait for the price that is written in discord as an entry

How to find discord channel ID:
![Untitled](https://user-images.githubusercontent.com/123463421/214431737-33b5a65a-0c59-4d3d-86c7-29f03cac1ea0.png)


How to find discord authorization key:
Go to https://discord.com/
CTRL-SHIFT-I to open dev tools
Go to network tab
start writing in some chat
In network tab filter type "typing"
Go to typing and find authorization:
![image](https://user-images.githubusercontent.com/123463421/214433666-ed22ffb3-40d8-4dc8-8889-0cf02bbb551d.png)



How to create API BINANCE:https://www.binance.com/en-ZA/support/faq/how-to-create-api-360002502072


HOW TO MAKE IT RUN 24/7:

You can use google cloud and create VM machine(first 3 months free) - https://www.youtube.com/watch?v=azh8J0acu6A

You can use Repl.it but be careful you have to protect your api keys in secret enviroment (Free) - https://www.youtube.com/watch?v=t7FsGcEUoRM

HOW TO DO IT WITH MULTIPLE DISCORD CHANNELS:

For now, it's best to just run multiple instances of the program with different Channel ID settings



DISCLAIMER:

The program is still in beta so you can test it at https://testnet.binancefuture.com/en/futures/ , but if you dont want that you can change it from True to False in settings.


You have to go trough all the coins in binance and select ISOLATED!!!!!!


SOON SUPPORT FOR BITGET

CONTACT ME:

If you have any questions you can message me in discord: Captain_Koalaツ#1665
