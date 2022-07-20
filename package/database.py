from __future__ import annotations
from threading import Lock

from pymongo import MongoClient

#Singleton pattern
class SingletonMetadb(type):

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

class Database(metaclass=SingletonMetadb):

    def __init__(self) -> None:
        client = MongoClient(port=27017)
        self.mydb = client["cryptoDatabase"]
        if "datastore" not in  self.mydb.list_collection_names():
             self.mydb.create_collection("datastore")
        if "usercrypto" not in  self.mydb.list_collection_names():
             self.mydb.create_collection("usercrypto")
    def addcollectopm(self,name :str,heur:str,data ) -> None:
        
        
        if  self.mydb["datastore"].count_documents({"name" :name, "TimeFrame.heur" : heur}) != 0:
            nameColletion = self.mydb["datastore"].find_one({"name" :name, "TimeFrame.heur" : heur}, { "_id" : 0 ,"TimeFrame.dataid": 1})["TimeFrame"]["dataid"]
            self.mydb.drop_collection(nameColletion)
            newCollection =  self.mydb.create_collection(name+heur)
            newCollection.insert_many(data)
            print(newCollection.find_one({}))
            self.mydb["datastore"].update_one({"name" : name , "TimeFrame.heur" : heur},{"$set" : { "TimeFrame.dataid" : newCollection.name}})
         
        else :
            newCollection =  self.mydb.create_collection(name+heur)
            newCollection.insert_many(data)
            print(newCollection.find_one({}))
            self.mydb["datastore"].insert_one({"name" : name , "TimeFrame" :{"heur" : heur,"dataid" : newCollection.name}})
        print("------------------")
        for i in self.mydb["datastore"].find({"name" :name}):

            print(i)
    def gainloss(self,name :str ,fram24h :float,fram1w:float,fram1M:float) -> None:
        if  self.mydb["datastore"].count_documents({"name" :name}) != 0:
            self.mydb["datastore"].update_one({"name" : name },{"$set" : { "gainlose.24h" :fram24h,"gainlose.1w" :fram1w,"gainlose.1M" :fram1M } })
        else :
            self.mydb["datastore"].insert_one({"name" : name ,"gainlose.24h" :fram24h,"gainlose.1w" :fram1w,"gainlose.1M" :fram1M })
        print(self.mydb["datastore"].find_one({}))
    def projection(self,name :str ,sum : float) -> None:
        if  self.mydb["datastore"].count_documents({"name" :name}) != 0:
            self.mydb["datastore"].update_one({"name" : name },{"$set" : { "projection" : sum } })
        else :
            self.mydb["datastore"].insert_one({"name" : name , "projection" : sum  })
    def adduser(self,name :str,APIKEY :str , APISEC :str   ):
        if  self.mydb["usercrypto"].count_documents({"UserName" : name}) == 0:
            self.mydb["usercrypto"].insert_one({"UserName" : name, "key" : {"APIKEY" : APIKEY , "APISEC" : APISEC }  , "balance" : {} })
    def updateBalance(self,name : str,idKey :str ,crypto:str,balance :float) -> None:
        if  self.mydb["usercrypto"].count_documents({"UserName" : name,"key.APIKEY": idKey }) == 1:
            self.mydb["usercrypto"].update_one({"UserName" : name,"key.APIKEY": idKey },{"$set":  { "balance."+crypto : balance }})
            ...
        ...