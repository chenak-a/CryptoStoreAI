from __future__ import annotations
import os
from binance.client import Client
from package.crypto import Crypto
from package.crypto import Coin
from package.datastore import Datastore
from package.user import User
from package.strategySell import BuySellmidTerm
import time

from dotenv import load_dotenv
load_dotenv('/Users/chena/AI/ai/.idea/.env')
class Controller: 
    #short cut to long to write dont ask question
    HEUR1H = Client.KLINE_INTERVAL_1HOUR
    HEUR4H = Client.KLINE_INTERVAL_4HOUR
    HEUR1D = Client.KLINE_INTERVAL_1DAY
    def __init__(self) -> None:
        self.user : dict[str,User] = {}
        self.store = Crypto("store")
    
        Datastore(Client(api_key=os.getenv("APIKEY"),
                        api_secret=os.getenv("APISEC")))
        
    def addUser(self ,Username ,api_key , api_secret) -> Controller:
        self.user[Username] = User(api_key,api_secret)
        return self
    
    def getbalance(self,user) -> Controller:
        self.user[user].balance()
        return self
    def addcoinUser(self,user:str,name :str) -> Controller:
     
        Datastore().connectUserandcoin(name,self.user[user])
        self.user[user].addAsset(name)
        
        
        return self
    def removecoinUser(self,user,name) -> Controller:
        self.user[user].removeAsset(name)
        return self
    def addcoin(self , name : str) -> Controller:
        name = name.upper()
        val = Crypto(name)
        Datastore().addcoin(val)
        val.add(Coin(name + self.HEUR1H,self.HEUR1H,BuySellmidTerm()))
        val.add(Coin(name + self.HEUR4H,self.HEUR4H,BuySellmidTerm()))
        val.add(Coin(name + self.HEUR1D,self.HEUR1D,BuySellmidTerm()))
        self.store.add(val)
        return self
    
    def data(self,name:str = "",heur :str = "") -> Controller:
      
        if name is not "":
            print("dsa")
            self.store.getcoin(name,name+heur)
        else :
            print("dsacc")
            self.store.data()
        return self
    
    def getjson(self,name:str = "",heur :str = ""):
        self.store.getcoin(name,name+heur)
def run():
    userinput = Controller()
    userinput.addUser("me",api_key=os.getenv("APIKEY"),api_secret=os.getenv("APISEC"))
    userinput.addcoin("FETUSDT").addcoin("IOTAUSDT")
    userinput.addcoinUser("me","FETUSDT").getbalance("me").data("IOTAUSDT") 
    print
if __name__ == '__main__':
    start_time = time.time()
    run()
    print("--- %s seconds ---" % (time.time() - start_time))
   
    

    