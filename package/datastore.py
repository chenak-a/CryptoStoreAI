from __future__ import annotations
from binance.client import Client
from threading import Lock, Thread
from .user import User
from .crypto import abstractmethod
class SingletonMeta(type):

    _instances = {}

    _lock: Lock = Lock()


    def __call__(cls, *args, **kwargs):

        with cls._lock:

            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Datastore(metaclass=SingletonMeta):
    
    def __init__(self, value: Client) -> None:
        self.client = value
        self.observatory : dict[str, tuple[abstractmethod, list[User]]] = {}
        
    
    def addcoin(self,coin:abstractmethod) -> None:
        if str(coin) not in self.observatory :
            self.observatory[str(coin)] = (coin,[])
       
      
    def connectUserandcoin(self,coin:str,user:User) -> Datastore:
   
        if coin  in self.observatory:
            self.observatory[coin][1].append(user)
        
        return self
    def notify(self,coin:abstractmethod) ->User:
        try:
            for user in self.observatory[str(coin)][1]:
                user.update(self.observatory[str(coin)][0])
        except:
            self.addcoin(coin)
       
    def deleteusderconnection(self,coin:abstractmethod) -> Datastore:
        self.observatory[coin].remove(User)
        return self
    def getclient(self) -> Client:
        assert self.client is not None , "is null"
        return self.client
    
