from __future__ import annotations
from abc import ABC, abstractmethod
from binance.client import Client as binanceclient


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
    def __init__(self,api_key ="", api_secret="") -> None:
        binanceclient.__init__(self,api_key,api_secret)
        self.portfolio :dict[str,float] = {}
        self.totaleBalance = 0
        
    
    def addAsset(self,name) -> None:
        print(name)
        self.portfolio[name] = 0.0
        print(self.portfolio)
        pass
    
    def removeAsset(self,name) -> None:
        del self.portfolio[name] 
        pass
    def buy(self) ->None:
        pass
    def sell(self) -> None:
        pass
    
    def update(self,name ):
        if name.statement()[0]:
            self.buy(name.statement()[1])
        else:
            self.sell(name.statement()[1])
                
 
    def balance(self) -> int:
        
        assert self.portfolio.values is not None , "list is empty"
        self.totaleBalance = 0
        for coin in self.portfolio:
            print(coin.split("USDT")[0])

            asset = self.get_asset_balance(asset=coin.split("USDT")[0].upper(), recvWindow=9000)['free']
            prince = self.get_klines(symbol=coin,interval = self.KLINE_INTERVAL_1HOUR , limit = 1)[0][4]
            resultAsset = float(asset) * float(prince)
            self.portfolio[coin] = resultAsset
            self.totaleBalance += resultAsset
        return self.totaleBalance