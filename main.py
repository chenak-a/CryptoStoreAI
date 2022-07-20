from __future__ import annotations

import os
import time

from binance.client import Client
from dotenv import load_dotenv

from package.crypto import Coin, Crypto
from package.datastore import Datastore
from package.strategybuy import BuyLongTerm ,BuymidTerm
from package.strategysell import SellLongTerm ,SellmidTerm
from package.user import User
from package.correction import CorrectionLayer1
from package.database import Database
pathNow = os.getcwd()
load_dotenv(pathNow+"/.env")

#Facade pattern
class Controller: 
    HOUR1H = Client.KLINE_INTERVAL_1HOUR
    HOUR2H = Client.KLINE_INTERVAL_2HOUR
    HOUR4H = Client.KLINE_INTERVAL_4HOUR
    HOUR6H = Client.KLINE_INTERVAL_6HOUR
    HOUR12H = Client.KLINE_INTERVAL_12HOUR
    HOUR3D = Client.KLINE_INTERVAL_3DAY
    HOUR1D = Client.KLINE_INTERVAL_1DAY
    def __init__(self) -> None:
        self.user : dict[str,User] = {}
        self.store = Crypto("store")
        self.store.parent = None

        Datastore(Client(api_key=os.getenv("APIKEY"),
                        api_secret=os.getenv("APISEC")))
        Database()

    def addUser(self ,Username ,api_key , api_secret) -> Controller:
        self.user[Username] = User(Username,api_key,api_secret)
        Database().adduser(Username,api_key,api_secret)
        return self

    def getbalance(self,user) -> Controller:
        self.user[user].balance()
        return self
    def addcoinUser(self,user:str,name :str) -> Controller:
        name = name.upper()
        Datastore().connectUserandcoin(name,self.user[user])
        self.user[user].addAsset(name)


        return self
    def removecoinUser(self,user,name) -> Controller:
        self.user[user].removeAsset(name)
        return self
    def addcoin(self , name : str) -> Controller:
        name = name.upper()
        val = Crypto(name,CorrectionLayer1())

        Datastore().addcoin(val)
        #trading time framme
        val.add(Coin(name + self.HOUR4H,self.HOUR4H,BuymidTerm(),SellmidTerm()))
        #added layer
        val.add(Coin(name + self.HOUR3D,self.HOUR3D,BuyLongTerm(),SellmidTerm(),12))
        val.add(Coin(name + self.HOUR1D,self.HOUR1D,BuyLongTerm(),SellmidTerm(),4))
      
        self.store.add(val)
        return self

    def data(self,name:str = "",hour :str = "") -> Controller:
        name = name.upper()
        if name is not "":
            self.store.getcoin(name,name+hour)
        else :

            self.store.data()
        return self

def run():
    run = Controller()
    run.addUser("chenak",api_key=os.getenv("APIKEY"),api_secret=os.getenv("APISEC"))
    listcoin :list = [ "BTCUSDT",
      "ETHUSDT",
      "IOTAUSDT",
      "FETUSDT",
      "NEARUSDT",
      "NKNUSDT",
      "ADAUSDT",
      "POWRUSDT",
      "CTXCUSDT",
      "IOTXUSDT",
      "VGXUSDT",
      "BNBUSDT",
      "BONDUSDT",
      "ADXUSDT",
      "ATAUSDT",
      "ARUSDT",
      "ETCUSDT",
      "WANUSDT",
      "MATICUSDT",
      "DOTUSDT",
      "TORNUSDT",
      "CTSIUSDT",
      "QTUMUSDT"]
    for coinin in listcoin:
        run.addcoin(coinin).addcoinUser("chenak",coinin)
        run.addcoin(coinin).data(coinin)
        time.sleep(60)
    
            
if __name__ == '__main__':
    start_time = time.time()
    run()
    print("--- %s seconds ---" % (time.time() - start_time))
