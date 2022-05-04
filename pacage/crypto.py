from __future__ import annotations
from abc import ABC, abstractmethod
from re import L
from unicodedata import name
from typing import List
from pacage.datastore import Datastore
import pandas as pd
class Abscrypto(ABC):
    

    @property
    def parent(self) -> Abscrypto:
        return self._parent

    @parent.setter
    def parent(self, parent:Abscrypto):
        self._parent = parent
    @parent.deleter
    def parent(self):
        del self._parent
    @abstractmethod
    def add (self ,composent : Abscrypto ) -> None:
        pass
    
    @abstractmethod
    def remove (self , composent: Abscrypto) -> None:
        pass
    

    @abstractmethod
    def data(self) -> None:
        pass
    
class Crypto(Abscrypto):
    def __init__(self,name:str) -> None:
        self.list : dict = {}
        self.name :str = name
        
    def __str__(self) -> str:
        return self.name
    
    def add (self ,composent : Abscrypto ) -> None:
        composent.parent = self
    
        self.list[str(composent)] = composent
      
        pass
    
    def remove (self , composent: Abscrypto) -> None:
        composent.parent(None)
        del self.list[str(composent)] 
        pass
    

    
    def data(self) -> None:
        for value  in self.list.values():
            value.data()
    def notify(self,sell : bool,price :float) -> None:
        self.sell  = False
        self.price = price
        Datastore().notify(self)
    def statement(self) :
        return self.sell,self.price
    def getcoin(self, name:str ,heur :str = "") -> None:
        if (self.list.__contains__(name)):
            if heur is "":
                self.list.get(name).data()
            else :
                self.list.get(name).getcoin(heur)
     

    
class Coin(Abscrypto):
    LIMIT = 300
    def __init__(self,name:str,heur:str) -> None:
        self.name : str = name
        self.heur : str = heur
        
       
        
        
    def __str__(self) -> str:
        return self.name
    def initilization(self) ->None:
        self.dataIn =  pd.DataFrame( Datastore().getclient().get_klines(symbol=self.parent, interval=self.heur, limit=self.LIMIT), dtype=float,columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time",
                              "Quote asset volume",
                              "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume",
                              "Can be ignored"])

    
    def add(self, composent: Abscrypto) -> None:
        return super().add(composent)
    
    def remove(self, composent: Abscrypto) -> None:
        return super().remove(composent)
    

        
    def data(self) -> None:
        self.initilization()
       
        self.parent.notify(True,self.dataIn["Close"][self.LIMIT-1])
       
    