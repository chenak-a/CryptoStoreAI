from __future__ import annotations
import os
from binance.client import Client
from pacage.crypto import Abscrypto
from pacage.crypto import Crypto
from pacage.crypto import Coin
from pacage.datastore import Datastore
from pacage.user import User
from dotenv import load_dotenv
load_dotenv('/Users/chena/AI/ai/.idea/.env')
class Activate: 
    #short cut to long to write dont ask question
    HEUR1H = Client.KLINE_INTERVAL_1HOUR
    HEUR4H = Client.KLINE_INTERVAL_4HOUR
    HEUR1D = Client.KLINE_INTERVAL_1DAY
    def __init__(self) -> None:
        self.user : dict[str,User] = {}
        self.store = Crypto("store")
    
        Datastore(Client(api_key=os.getenv("APIKEY"),
                        api_secret=os.getenv("APISEC")))
        
    def addUser(self ,Username ,api_key , api_secret) -> Activate:
        self.user[Username] = User(api_key,api_secret)
        return self
    
    def getbalance(self,user) -> Activate:
        self.user[user].balance()
        return self
    def addcoinUser(self,user,name) -> Activate:
        self.user[user].addAsset(name)
        Datastore()
        return self
    def removecoinUser(self,user,name) -> Activate:
        self.user[user].removeAsset(name)
        return self
    def addcoin(self , name : str) -> Activate:
        name = name.upper()
        val = Crypto(name)
        val.add(Coin(name + self.HEUR1H,self.HEUR1H))
        val.add(Coin(name + self.HEUR4H,self.HEUR4H))
        val.add(Coin(name + self.HEUR1D,self.HEUR1D))
        self.store.add(val)
        return self
    
    def data(self,name:str = "",heur :str = "") -> Activate:
        if name is not "":
            self.store.getcoin(name,name+heur)
        else :
            self.store.data()
        return self
if __name__ == '__main__':
    valeur = Activate()
    valeur.addUser("me",api_key=os.getenv("APIKEY"),api_secret=os.getenv("APISEC"))
    valeur.addcoinUser("me","IOTAUSDT").getbalance("me")
    #valeur.addcoin("FETUSDT").addcoin("IOTAUSDT").data("FETUSDT",valeur.HEUR1H)
    

    