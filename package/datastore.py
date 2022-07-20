from __future__ import annotations
from binance.client import Client
from threading import Lock
from .user import User
from pymongo import MongoClient
from .crypto import abstractmethod
#Singleton pattern
class SingletonMeta(type):

    _instances = {}

    _lock: Lock = Lock()


    def __call__(cls, *args, **kwargs):
        """lock multithreading calls 

        """
        with cls._lock:

            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Datastore(metaclass=SingletonMeta):

    def __init__(self, value: Client = None) -> None:

        self.client = value
        self.observatory : dict[str, tuple[abstractmethod, list[User]]] = {}

        
    def addcoin(self,coin:abstractmethod) -> None:
        """follow specific asset
        """
        if str(coin) not in self.observatory :
            self.observatory[str(coin)] = (coin,[])


    def connectUserandcoin(self,coin:str,user:User) -> Datastore:
        """subscribe user to a coin for notification

        Args:
            coin (str): Asset
            user (User): user
        """
        if coin  in self.observatory:
            self.observatory[coin][1].append(user)

        return self
    def notify(self,coin:abstractmethod) ->User:
        """coin send notification to all user there are subscribe to it  

        Args:
            coin (str): Asset
            user (User): user
        """
        try:
            for user in self.observatory[str(coin)][1]:
                user.update(self.observatory[str(coin)][0])
        except:
            self.addcoin(coin)
        
    def deleteusderconnection(self,coin:abstractmethod) -> Datastore:
        """remove subscription

        Args:
            coin (abstractmethod): Asset

        """
        self.observatory[coin].remove(User)
        return self
    def getclient(self) -> Client:
        """get client

        Returns:
            Client: binance api
        """
        assert self.client is not None , "is null"
        return self.client

