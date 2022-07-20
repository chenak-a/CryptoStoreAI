from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import pandas as df
import numpy as np
#Strategy pattern
class AbsSell(ABC):
    def __init__(self,level : int = -1 ) -> None:
        self.level :int = level
    @abstractmethod
    def Sell(self ,df : df, mn :int) -> bool:
       
        """decision tree

        Returns:
            list: BUY(1) and sell(2) point 
        """
        pass
    def getlevel(self):
        return self.level
class SellLongTerm(AbsSell):

    def Sell(self ,df : df,mn :int) -> bool:
        
        level0 = df["amb13"][mn] >= 0.95 and df["amb14"][mn] >= 0.95 and df["amb2"][mn] >= 0.85 and df["amb0"][
        mn] >= 0.85
        level1 = df["amb13"][mn] >= 0.85 and df["amb14"][mn] >= 0.80 and df["amb2"][mn] >= 0.63 and df["amb0"][
        mn] >= 0.69
        level2 = df["amb13"][mn] >= 0.69 and df["amb14"][mn] >= 0.70 and df["amb2"][mn] >= 0.70 and df["amb0"][
        mn] >= 0.75
        level3 = df["amb2"][mn] >= 0.95 and df["amb99"][mn] >= 0.98
        level4 = df["amb99"][mn] >= 0.95 and df["amb2"][mn] >= 0.80 and df["ambb5"][mn] >= 0.45 and df["rsiK"][
        mn] >= 0.63
        level5 = df["ww1"][mn] >= 0.70 and df["aroonu"][mn] >= 92 and df["ww1"][mn] <= df["ww"][mn]
        supertop = level0 or level1 or level2 or level3
        sellT0 = supertop or level3 or level4 or level5
        level6 = df["amb13"][mn] >= 0.67 and df["amb14"][mn] >= 0.67 and df["amb2"][mn] >= 0.80
        level4h = df["amb14"][mn] >= 0.55 and df["amb2"][mn] >= 0.75 and df["aroonu"][mn] >= 92 and df["ambb5"][
        mn] >= 0.70 and df["rsiK"][mn] >= 0.82 and df["ci"][mn] >= 0.73
        sellT1 = sellT0 or level4h or level6 or df["amb55"][mn] >= 0.97
        return sellT1
class SellmidTerm(AbsSell):
    def Sell(self ,df : df,mn :int) -> tuple:
        value :str = ""
        level0 = df["amb13"][mn] >= 0.95 and df["amb14"][mn] >= 0.95 and df["amb2"][mn] >= 0.85 and df["amb0"][mn] >= 0.85
        if level0 and value == "" :
            value = "level0"
        level1 = df["amb13"][mn] >= 0.85 and df["amb14"][mn] >= 0.80 and df["amb2"][mn] >= 0.63 and df["amb0"][mn] >= 0.69
        if level1 and value == "" :
            value = "level1" 
        level2 = df["amb13"][mn] >= 0.69 and df["amb14"][mn] >= 0.70 and df["amb2"][mn] >= 0.70 and df["amb0"][mn] >= 0.75
        if level2 and value == "" :
            value = "level2"  
        level3 = df["amb2"][mn] >= 0.95 and df["amb99"][mn] >= 0.98
        if level3 and value == "" :
            value = "level3"  
        level4 = df["amb99"][mn] >= 0.95 and df["amb2"][mn] >= 0.80 and df["ambb5"][mn] >= 0.45 and df["rsiK"][
            mn] >= 0.63
        if level4 and value == "" :
            value = "level4"
        level5 = df["ww1"][mn] >= 0.70 and df["aroonu"][mn] >= 92 and df["ww1"][mn] <= df["ww"][mn]
        if level5 and value == "" :
            value = "level5"
        supertop = level0 or level1 or level2 or level3
        sellT0 = supertop or level3 or level4 or level5
        level6 = df["amb13"][mn] >= 0.67 and df["amb14"][mn] >= 0.67 and df["amb2"][mn] >= 0.80
        if level6 and value == "" :
            value = "level6"
        level7 = df["amb14"][mn] >= 0.55 and df["amb2"][mn] >= 0.75 and df["aroonu"][mn] >= 92 and df["ambb5"][
            mn] >= 0.70 and df["rsiK"][mn] >= 0.82 and df["ci"][mn] >= 0.73
        if level7 and value == "" :
            value = "level7"
        sellT1 = sellT0 or level7 or level6
        level8 = df ["BUY2"] [mn] <=0.94 and df ["amb2"] [mn] >=0.30 and   df ["amb13"] [mn] >= 0.18 and   df ["amb0"] [mn] >= 0.45
        if level8 and value == "" :
            value = "level8"
        level9 =  df["amb55"][mn] >= 0.90 and  df["rsiK"][mn] >= 0.95 and  df["ci"][mn] >= 0.75 and df["amb13"][mn] <= 0.1
        if level9 and value == "" :
            value = "level9"
        level10 = df ["amb13"] [mn] >= 0.75 and df ["amb14"] [mn] >= 0.70 and df ["amb15"] [mn] >= 0.70 and df ["amb55"] [mn] >= 0.55 and df ["aroonu"] [mn] >= 92 and df ["aroond"] [mn] <= 30 and df ["ambb5"] [mn] >= 0.75 and df ["ci"] [mn] >= 0.75 and df ["rsiK"] [mn] >= 0.83  and df ["amb99"] [mn] >= 0.18
        if level10 and value == "" :
            value = "level10"
        level11 = df["amb13"][mn] >=0.8 and df["amb15"][mn] >=0.8 and df["amb55"][mn] >=0.8
        if level11 and value == "" :
            value = "level11"
        level12 = df["amb13"][mn] >=0.85 and df["amb14"][mn] >=0.82 and df["amb15"][mn] >=0.85 and df["amb55"][mn] >=0.65
        if level12 and value == "" :
            value = "level12"
        sellT2 = sellT1 or level8 or level10 or level9 or level11 or level12
        sellT3 = df ["amb55"] [mn] >= 0.50 and df["amb15"][mn] >=0.30 and df ["amb55"] [mn] > df["amb15"][mn] and df["amb14"][mn] <=0.05 and df["amb13"][mn] <=0.05  and df["macd"][mn] <= df["histogram"][mn]
        if sellT3 and value == "" :
            value = "sellT3"
        if AbsSell.getlevel(self) == 0 :
            return  (level0 or level1 or level2 or level3,value)
        elif  AbsSell.getlevel(self) == 1 :
            return (supertop or level3 or level4 or level5,value)
        else:
            return (sellT2 or sellT3  or (df["BUY2"][mn] <= 0.1 and df["amb55"][mn] >= 0.8) or (df["ci"][mn] >= 0.90 and df["amb55"][mn] >= 0.90 and df["amb13"][mn] >= 0.6)  or df ["amb2"] [mn] >= 0.9 and  df["amb13"][mn] >= 0.75,value)
    

    ...