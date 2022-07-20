from __future__ import annotations
from abc import ABC, abstractmethod
from binance.client import Client as binanceclient
from package.database import Database



class AbsUser(ABC):
    @abstractmethod
    def balance(self) ->int:
        pass
    @abstractmethod
    def addAsset(self) -> None:
        pass
    @abstractmethod
    def removeAsset(self) -> None:
        pass
    @abstractmethod
    def buy(self) ->None:
        pass
    @abstractmethod
    def sell(self) -> None:
        pass
class User(ABC,binanceclient):
    def __init__(self, name :str ,api_key :str , api_secret:str) -> None:
        binanceclient.__init__(self,api_key,api_secret)
        self.name = name
        self.keyid = api_key
        self.portfolio :dict[str,float] = {}
        self.totaleBalance = 0


    def addAsset(self,name :str) -> None:
        """Add new asset to list

        Args:
            name (str): name of the asset
        """
        self.portfolio[name] = 0.0
        pass

    def removeAsset(self,name :str) -> None:
        """remove asset from the list

        Args:
            name (str): name of the asset
        """
        del self.portfolio[name] 
        pass
    
    def buy(self,state) ->None:
        print("a")
        pass
    def sell(self,state) -> None:
        
        print("b")
        pass

    def update(self,name  ):
        """Update user when an important change accrue in specific 
        asset if he is subscribe too

        Args:
            name (Crypto): Asset 
        """
        if name.statement()[0]:
            self.buy(name.statement()[1])
        else:
            self.sell(name.statement()[1])

    def getBalancecoin(self,coin :str ,timeframe :str,preiode :int) -> float:
        """_summary_

        Args:
            coin (str): coin
            timeframe (str): Time Frame
            preiode (int): periode -> 1 new 0 last

        Returns:
            float: balance
        """
        asset = self.get_asset_balance(asset=coin.split("USDT")[0].upper(), recvWindow=9000)['free']
        prince = self.get_klines(symbol=coin,interval = timeframe, limit = 2)[preiode][4]
        print(prince)
        return float(asset) * float(prince)
  
    def balance(self) -> int:
        """Calculat balance of all asset in the lists

        Returns:
            int: balance
        """
        assert self.portfolio.values is not None , "list is empty"
        self.totaleBalance = 0
        for coin in self.portfolio:

            resultAsset = self.getBalancecoin(coin,self.KLINE_INTERVAL_1HOUR,1 )
            self.portfolio[coin] = resultAsset
            print("{0} : {1:.2f}".format(coin,resultAsset))
           
            Database().updateBalance(self.name,self.keyid,coin,resultAsset)
            self.totaleBalance += resultAsset
        print("total : {0:.2f}".format(self.totaleBalance))
        
        return self.totaleBalance