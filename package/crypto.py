from __future__ import annotations
from abc import ABC, abstractmethod
from cProfile import label
from re import I
from unicodedata import name
from typing import Iterable
from datetime import datetime
from package.datastore import Datastore
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import json
import package.cry as cry
import matplotlib.dates as md
from .correction import AbsCorrection
import os
from .strategyBuySell import AbsBuySell
pathName = os.path.join ("C:/Users/chena/AI2.0/CryptoStoreAutomate/model/")
import concurrent.futures
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
    def data(self) -> dict:
        pass
    
class Crypto(Abscrypto):
    def __init__(self,name:str ,correctionlayer : AbsCorrection  = None) -> None:
        self.container : dict = {}
        self.name :str = name
        self.containterdata : tuple[(str,pd.DataFrame,int)] = ()
        self.correctionlayer :AbsCorrection = correctionlayer
        
        
    def __str__(self) -> str:
        return self.name
    
    def add (self ,composent : Abscrypto ) -> None:
        composent.parent = self
        self.container[str(composent)] = composent
      
        pass
    
    def remove (self , composent: Abscrypto) -> None:
        composent.parent(None)
        del self.container[str(composent)] 
        pass
    def setcontainerdata(self,data ) -> None:
        self.containterdata = data
    def combine(self,listpd : pd.DataFrame,comin :int ,name : str) :
        
        list = listpd[ (listpd["Open time"] > self.containterdata[1]["Open time"][0])   ]
  
        y = 0
        i = 0
        m = []
        z = []
    
        while i < len( self.containterdata[1].index) :
         
            if( y < len(list.index)):
                if self.containterdata[1]["Open time"][i] < list.iloc[y]["Open time"]:
                    m.append(0.0)
                    z.append(datetime.fromtimestamp (self.containterdata[1]["Close time"][i]/ 1000))
                    
                    i += 1
                else:
                    if(  ((self.containterdata[1]["Open time"][i] >= list.iloc[y]["Open time"] ) and  ( self.containterdata[1]["Close time"][i] <= list.iloc[y]["Close time"])) ):
                        m.append(list.iloc[y]["amb55"])
                        z.append(datetime.fromtimestamp (self.containterdata[1]["Close time"][i]/ 1000))
                        i += 1 
                      
                    else:
                        
                        y += 1
             
            else:
                break
        data ={'time': z, 'pk': m}
        dfa = pd.DataFrame(data = data)
        self.containterdata[1]["pk"+name] = dfa["pk"]
        self.containterdata[1]["pck"+name] = dfa["pk"].pct_change(periods=10).ewm(com=comin).mean()
   
   
       
    def correction(self) -> None:
        buysell = self.containterdata[1][self.containterdata[1]["BUYSELL"] == 1.0]
        
        for x in buysell.index:
            if ((self.containterdata[1].at[x,'pck1d']  < 0.2 and self.containterdata[1].at[x,'pk3d']  > 0.2 )  or (self.containterdata[1].at[x,'pck1d']  < 0.1 and self.containterdata[1].at[x,'pck3d']  < 0.1 ) )  :
                self.containterdata[1].at[x,'BUYSELL'] = 0.0
            if((self.containterdata[1].at[x,'BUY2'] < 0.13  ) or  (self.containterdata[1].at[x,'pk3d']  > 0.1 and self.containterdata[1].at[x,'pck3d']  > 0.1 and self.containterdata[1].at[x,'pck1d'] > 0.1 ) or (self.containterdata[1].at[x,'pk1d']  < 0.15 and self.containterdata[1].at[x,'pck1d']  < -0.4 and self.containterdata[1].at[x,'pk3d']  < 0.11 and self.containterdata[1].at[x,'pck3d']  > -0.1) ):
                 self.containterdata[1].at[x,'BUYSELL'] = 1.0
            if x <= 50:
                 self.containterdata[1].at[x,'BUYSELL'] = 0.0
        print(buysell)
                
    def analyser(self ,data : Iterable[tuple]) -> None:
        i = 0
        for x,y,z in data:
            if i == 0 :
                self.containterdata = (x,y,z)
            else:
                self.combine(y,z,x.replace(self.name,""))
                
            i +=1
        
    
        self.containterdata[1].append(self.correctionlayer.correction(self.containterdata[1])) 
       
        self.activateBUYSELL()
        self.json()
      
        pass
    
    def data(self) -> dict:
        
        def calldata(variable :Abscrypto) -> dict:
            return variable.data()
        with concurrent.futures.ThreadPoolExecutor() as executers:
            result = executers.map(calldata,self.container.values()) 
        if self.parent is not None : 
            self.analyser(result)
          
        return self.containterdata
        
    def activateBUYSELL(self) ->Crypto:
        print("aa")
        self.notify(True,self.containterdata[1]["Close"][len(self.containterdata[1].index)-1])
        return self
    def json(self) -> Crypto:
        assert self.containterdata is not None , "containter empty"
        
        #delete
        self.containterdata[1]["ci"] = self.containterdata[1]["pk"+"3d"]
        self.containterdata[1]["rsiK"] = self.containterdata[1]["pck"+"3d"]*100 
        self.containterdata[1]["ambb5"] = self.containterdata[1]["ci"]
        self.containterdata[1]["aroonu"] = self.containterdata[1]["pk"+"1d"]*100 
        self.containterdata[1]["aroond"] = self.containterdata[1]["pck"+"1d"]*100 
        ###
        completeName = os.path.join(os.getenv("SERVER"), "temp.json")
        name = {"name": str(self.name)}
        time = {"time" : str(self.containterdata[0].replace(self.name,"") )}
        z = json.loads(self.containterdata[1].to_json())
        z.update(name)
        z.update(time)
        with open(completeName, 'w') as f:
            json.dump(z, f)
        return self
    def notify(self,sell : bool,price :float) -> None:
        self.sell  = False
        self.price = price
        Datastore().notify(self)
    def statement(self) :
        return self.sell,self.price
    def getcoin(self, name:str ,hour :str = "") -> Crypto:
    
        if (self.container.__contains__(name)):
            if hour.replace(name,"") is "":
                self.container.get(name).data()
            else :
                self.container.get(name).getcoin(hour).json().activateBUYSELL()
        return self
                
        

    
class Coin(Abscrypto):
    LIMIT = 300
    def __init__(self,name:str,hour:str,strategy:AbsBuySell,com :int = 0) -> None:
        self.name : str = name
        self.hour : str = hour
        self.strategy : AbsBuySell = strategy
        self.com = com
        
    def initialization(self) ->None:
        #endTime=1642222800000
        self.dataIn =  pd.DataFrame( Datastore().getclient().get_klines(symbol=self.parent, interval=self.hour, limit=self.LIMIT), dtype=float,columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time",
                              "Quote asset volume",
                              "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume",
                              "Can be ignored"])
        df = self.dataIn
        rsi = cry.EWMArsi(df["Close"], 14)
        rsiK = cry.rsiso(rsi, "TK")
        rsiD = cry.rsiso(rsi, "TD")
        Volumsoci = cry.volosc(df["Volume"], "R")
        penVoc = cry.pentevolosc(Volumsoci, "T")
        penrsi = cry.pentrsi(rsi, "T")
        penrsiK = cry.pentrsiK(rsiK.fillna(0), "T")
        penrsiD = cry.pentrsiK(rsiD.fillna(0), "T")
        VGTN = cry.volumegain(df["Volume"], "T")
        macd = cry.macd(df["Close"], "macd")
        histogram = cry.macd(df["Close"], "histogram")
        histogrammacd = cry.macd(df["Close"], "histogrammacd")
        efi13 = cry.efi13(df["Close"], df["Volume"])
        penthistogram = cry.penthistogram(histogram, "T")
        AroonU = cry.aroon(df["Close"], "U")
        AroonD = cry.aroon(df["Close"], "D")

        df["rsi"] = rsi
        df["rsiK"] = rsiK
        df["rsiD"] = rsiD
        df["Volumsoci"] = Volumsoci
        df["penVoc"] = penVoc
        df["penrsi"] = penrsi
        df["penrsiK"] = penrsiK
        df["penrsiD"] = penrsiD
        df["VGTN"] = VGTN
        df["macd"] = macd
        df["histogram"] = histogram
        df["histogrammacd"] = histogrammacd
        df["efi13"] = efi13
        df["penthistogram"] = penthistogram
        prmacd = cry.prmacd(df["macd"])
        df["prmacd"] = prmacd
        prhistogram = cry.prmacd(df["histogram"])
        df["prhistogram"] = prhistogram
        prVo = cry.prmacd(df["Quote asset volume"])
        df["prVo"] = prVo
        penprvo = cry.pentevolosc(df["prVo"], "T")
        df["penprvo"] = penprvo
        prefi13 = cry.prmacd(df["efi13"])
        df["prefi13"] = prefi13

        df["aroonu"] = AroonU
        df["aroond"] = AroonD
        macdin = cry.macd(macd, "macd")
        df["macdin"] = macdin
        macdfast = cry.macd(macd, "histogram")
        df["macdfast"] = macdfast

        prmacdin = cry.prmacd(df["macdin"]) / 100
        df["prmacdin"] = prmacdin
        prmacdfast = cry.prmacd(df["macdfast"]) / 100
        df["prmacdfast"] = prmacdfast
        Y = np.array(
            df[["aroonu", "rsiK", "rsiD", "penrsiK", "penrsi", 'prmacd', "prhistogram", "prVo", "rsi"]] / 100)
        Y = np.nan_to_num(Y)


        model11 = tf.keras.models.load_model(pathName+"model_BUY2.h5")
        amb1111 = model11.predict(Y)
        df["amb1111"] = amb1111
        model = tf.keras.models.load_model(pathName+"model_buy.h5")
        amb = model.predict(Y)
        df["amb"] = amb
        model12 = tf.keras.models.load_model(pathName+"model_BUY10.h5")
        amb12 = model12.predict(Y)
        df["amb12"] = amb12
        model14 = tf.keras.models.load_model(pathName+"model_buyo.h5")
        amb14 = model14.predict(Y)
        df["amb14"] = amb14
        model15 = tf.keras.models.load_model(pathName+"model_buyo1.h5")
        amb15 = model15.predict(Y)
        df["amb15"] = amb15
        model13 = tf.keras.models.load_model(pathName+"model_BUY11.h5")
        amb13 = model13.predict(Y)
        df["amb13"] = amb13

        modelBUY1 = tf.keras.models.load_model(pathName+"model_BUY1.h5")
        BUY1 = modelBUY1.predict(Y)
        df["BUY1"] = BUY1

        modelBUY2 = tf.keras.models.load_model(pathName+"model_BUY3.h5")
        BUY2 = modelBUY2.predict(Y)
        df["BUY2"] = BUY2

        model0 = tf.keras.models.load_model(pathName+"model_sell4.h5")

        model1 = tf.keras.models.load_model(pathName+"model_sell98.h5")
        amb1 = model1.predict(Y)
        df["amb1"] = amb1
        model99 = tf.keras.models.load_model(pathName+"model_sell10.h5")
        amb99 = model99.predict(Y)
        df["amb99"] = amb99

        model2 = tf.keras.models.load_model(pathName+"model_sell2.h5")
        amb2 = model2.predict(Y)
        df["amb2"] = amb2

        model3 = tf.keras.models.load_model(pathName+"model_sell0.1_1x6.h5")
        amb3 = model3.predict(Y)
        df["amb3"] = amb3

        modei = tf.keras.models.load_model(pathName+"model_buytomp.h5")
        ambi = modei.predict(Y)
        df["ambi"] = ambi

        amb0 = model0.predict(Y)

        df["amb0"] = amb0
        df["ambto"] = (df["amb0"] + df["amb1"] + df["amb2"] + df["amb3"]) / 4
        Y2 = np.array(
            df[["aroonu", "rsiK", "rsiD", "penrsiK", "penrsi", 'prmacd', "prhistogram", "prVo", "rsi", "BUY2",
                "amb13", "amb99", "ambi", "amb14", "amb15", "amb0", "amb1", "amb2", "amb3", "ambto"]] / 100)
        Y2 = np.nan_to_num(Y2)

        model55 = tf.keras.models.load_model (pathName+"model_b5.h5")
        amb55 = model55.predict (Y2)
        df ["amb55"] =   1-cry.prmacd (amb55) / 100
        modelop = tf.keras.models.load_model(pathName+"model_b1.h5")
        ambb = modelop.predict(Y2)
        df["ambb"] = cry.prmacd(ambb) / 100

        modelop5 = tf.keras.models.load_model(pathName+"model30.h5")
        ambb5 = modelop5.predict(Y2)
        df["ambb5"] = cry.prmacd(ambb5) / 100
        df["amb1111"] = cry.prmacd(amb1111) / 100
        df["amb"] = cry.prmacd(amb) / 100
        df["BUY1"] = cry.prmacd(BUY1) / 100

        df["BUY2to"] = df["BUY2"].ewm(span=10).mean()
        df["amb55to"] = df["amb55"].ewm(span=5).mean()
        df["ww"] = ((df["rsiD"] - df["prmacdin"]) / 100).ewm(span=2).mean()
        df["ww"] = cry.prmacd(df["ww"]) / 100
        df["ww1"] = ((df['rsiK'] - df["prmacdfast"]) / 100).ewm(span=2).mean()
        df["ww1"] = cry.prmacd(df["ww1"]) / 100
        df["ww2"] = ((df["rsi"] - df["prhistogram"]) / 100).ewm(span=2).mean()
        df["ww3"] = ((df['amb'] - df["ambb"])).ewm(span=2).mean()
        df["ci"] = 1 - cry.prmacd(df["ww3"]) / 100
        df["ww4"] = ((df["rsiD"] - df["prhistogram"]) / 100).ewm(span=2).mean()
        df["ww5"] = ((df['rsiK'] - df["prmacd"]) / 100).ewm(span=2).mean()
        df["ww6"] = df['rsi'] - df["prhistogram"]
        df["ww6"] = cry.prmacd(df["ww6"]) / 100
        df["ww7"] = df['rsi'] - df["prmacd"]
        df["ww7"] = cry.prmacd(df["ww7"]) / 100

        df["efi13"] = cry.prmacd(df["efi13"]) / 100
        df['amb133'] = df["amb13"].ewm(span=2).mean()
        df['amb1333'] = df["amb133"].ewm(span=2).mean()
        df['amb13333'] = df["amb1333"].ewm(span=2).mean()
        df["amo"] = df["macdin"] - df["macdfast"]
        df["amo"] = cry.prmacd(df["amo"]) / 100
        df["amo"] = cry.pentrsiK(df["amo"], "T")
        df["amo"] = cry.prmacd(df["amo"]) / 100
        df["amo1"] = df["macdfast"] - df["macdin"]
        df["amo1"] = cry.prmacd(df["amo1"]) / 100
        df["amo1"] = cry.pentrsiK(df["amo1"], "T")
        df["amo1"] = cry.prmacd(df["amo1"]) / 100
        df["amb14"] = cry.prmacd(df["amb14"]) / 100
        df["amb15"] = cry.prmacd(df["amb15"]) / 100
        df["amb99"] = cry.prmacd(df["amb99"]) / 100
        df["ambb"] = cry.prmacd(df["ambb"]) / 100
        df["ambb5"] = 1 - (cry.prmacd(df["ambb5"]) / 100)
        df["ambi"] = cry.prmacd(df["ambi"]) / 100
        # good for sell
        # df["ww8"] = ((df["amb133"] - df["ambb5"])).ewm(span=2).mean()
        # df["ww8"] = cry.prmacd(df["ww8"])

        esa = df["Close"].ewm(span=5, adjust=False).mean()
        d = abs(df["Close"] - esa).ewm(span=5, adjust=False).mean()
       
        df["ww8"] = (df["BUY2"] - df["ambb5"]).ewm(span=2).mean()
        df["ww8"] = cry.prmacd(df["ww8"])
        self.dataIn = df
        
        self.dataIn["BUYSELL"] = self.strategy.BuySell(self.dataIn)
        
    def __str__(self) -> str:
        return self.name
    
    
    def add(self, composent: Abscrypto) -> None:
        return super().add(composent)
    
    def remove(self, composent: Abscrypto) -> None:
        return super().remove(composent)
    
    def data(self) -> tuple:
        self.initialization()
        dictionerydata = (self.name,self.dataIn,self.com)
        self.parent.setcontainerdata(dictionerydata)
 
        return dictionerydata
      
       
    