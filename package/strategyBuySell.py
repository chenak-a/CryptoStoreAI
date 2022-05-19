
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import pandas as df
import numpy as np
class AbsBuySell(ABC):
    @abstractmethod
    def BuySell(self) -> list:
        pass
    
class BuySellLongTerm(AbsBuySell):
    def BuySell(self,df : df) -> list:
        situation4 = []
        for mn in range(len(df.index)):
            level0 = df["amb13"][mn] >= 0.95 and df["amb14"][mn] >= 0.95 and df["amb2"][mn] >= 0.85 and df["amb0"][
                mn] >= 0.85
            level1 = df["amb13"][mn] >= 0.85 and df["amb14"][mn] >= 0.80 and df["amb2"][mn] >= 0.63 and df["amb0"][
                mn] >= 0.69
            level2 = df["amb13"][mn] >= 0.69 and df["amb14"][mn] >= 0.70 and df["amb2"][mn] >= 0.70 and df["amb0"][
                mn] >= 0.75
            level7 = df["amb2"][mn] >= 0.95 and df["amb99"][mn] >= 0.98
            level10 = df["amb99"][mn] >= 0.95 and df["amb2"][mn] >= 0.80 and df["ambb5"][mn] >= 0.45 and df["rsiK"][
                mn] >= 0.63
            level15 = df["ww1"][mn] >= 0.70 and df["aroonu"][mn] >= 92 and df["ww1"][mn] <= df["ww"][mn]
            supertop = level0 or level1 or level2 or level7
            sellT0 = supertop or level7 or level10 or level15
            level3h = df["amb13"][mn] >= 0.67 and df["amb14"][mn] >= 0.67 and df["amb2"][mn] >= 0.80
            level4h = df["amb14"][mn] >= 0.55 and df["amb2"][mn] >= 0.75 and df["aroonu"][mn] >= 92 and df["ambb5"][
                mn] >= 0.70 and df["rsiK"][mn] >= 0.82 and df["ci"][mn] >= 0.73
            sellT1 = sellT0 or level4h or level3h or df["amb55"][mn] >= 0.97
           
            level0b = df ["ww1"] [mn] <= 0.3  and df ["aroond"] [mn] >= 92   and df ["amb13"] [mn] <= 0.1 and  df ["ci"] [mn] >= 0.40 and  df ["BUY2"] [mn] >= 0.95 
            level123 =  df ["ww1"] [mn] <= 0.01 and df ["amb99"] [mn] <= 0.01
            level5b = df ["ww1"] [mn] <= 0.1  and  df ["ww7"] [mn] >= 0.5 and df ["aroond"] [mn] >= 92  and  df ["ci"] [mn] <= 0.20
            level6b = df ["ww1"] [mn] <= 0.1  and  df ["ww7"] [mn] >= 0.5 and  df ["BUY2"] [mn] <= 0.1
            level7b = df ["ww1"] [mn] <= 0.6  and  df ["ww7"] [mn] >= 0.9 and  df ["BUY2"] [mn] <= 0.15 and df ["aroond"] [mn] >= 92
            level8b =  df ["ww1"] [mn] <= 0.3  and  df ["ww7"] [mn] >= 0.5 and  df ["BUY2"] [mn] >= 0.97 and df ["amb14"] [mn] >= 0.15 and df ["amb13"] [mn] <= 0.10
            level9b = df ["amb14"] [mn] >= 0.65 and df ["amb13"] [mn] <= 0.2 and df ["amb99"] [mn] >= 0.97
            level11b = df ["ww5"] [mn] <= -0.4 and  df ["ww5"] [mn]  >=  df ["ww4"] [mn] and df ["ambb"] [mn] <= 0.01
            level1b=  df ["ci"] [mn] <= 0.3 and df ["ci"] [mn] <= 0.3 and  df ["ambb5"] [mn] <= 0.14 and  df ["amb13"] [mn] <= 0.1 and df ["amb14"] [mn] <= 0.1  and df ["amb99"] [mn] <= 0.1 

            #level0b or level123 or level5b or level6b or level7b
            if level0b or level123 or level5b or level6b or level7b:
                situation4.append(1.0)
            #sellT1
            elif sellT1:
                situation4.append(2.0)
            else:
                situation4.append(0.0)
       
        return  situation4


class BuySellmidTerm(AbsBuySell):
    def BuySell(self,df : df) -> list:
        situation4 = []
        lagestammb5 = np.array(df['ambb5'].nlargest(n=50))[49]

        for mn in range(len(df.index)):
            level0 = df["amb13"][mn] >= 0.95 and df["amb14"][mn] >= 0.95 and df["amb2"][mn] >= 0.85 and df["amb0"][
                mn] >= 0.85
            level1 = df["amb13"][mn] >= 0.85 and df["amb14"][mn] >= 0.80 and df["amb2"][mn] >= 0.63 and df["amb0"][
                mn] >= 0.69
            level2 = df["amb13"][mn] >= 0.69 and df["amb14"][mn] >= 0.70 and df["amb2"][mn] >= 0.70 and df["amb0"][
                mn] >= 0.75
            level7 = df["amb2"][mn] >= 0.95 and df["amb99"][mn] >= 0.98
            level10 = df["amb99"][mn] >= 0.95 and df["amb2"][mn] >= 0.80 and df["ambb5"][mn] >= 0.45 and df["rsiK"][
                mn] >= 0.63
            level15 = df["ww1"][mn] >= 0.70 and df["aroonu"][mn] >= 92 and df["ww1"][mn] <= df["ww"][mn]
            supertop = level0 or level1 or level2 or level7
            sellT0 = supertop or level7 or level10 or level15
            level3h = df["amb13"][mn] >= 0.67 and df["amb14"][mn] >= 0.67 and df["amb2"][mn] >= 0.80
            level4h = df["amb14"][mn] >= 0.55 and df["amb2"][mn] >= 0.75 and df["aroonu"][mn] >= 92 and df["ambb5"][
                mn] >= 0.70 and df["rsiK"][mn] >= 0.82 and df["ci"][mn] >= 0.73
            sellT1 = sellT0 or level4h or level3h
            level5mh = df ["BUY2"] [mn] <=0.94 and df ["amb2"] [mn] >=0.30 and   df ["amb13"] [mn] >= 0.18 and   df ["amb0"] [mn] >= 0.45
            level126 =  df["amb55"][mn] >= 0.90 and  df["rsiK"][mn] >= 0.95 and  df["ci"][mn] >= 0.75 and df["amb13"][mn] <= 0.1
            level6mh = df ["amb13"] [mn] >= 0.75 and df ["amb14"] [mn] >= 0.70 and df ["amb15"] [mn] >= 0.70 and df ["amb55"] [mn] >= 0.55 and df ["aroonu"] [mn] >= 92 and df ["aroond"] [mn] <= 30 and df ["ambb5"] [mn] >= 0.75 and df ["ci"] [mn] >= 0.75 and df ["rsiK"] [mn] >= 0.83  and df ["amb99"] [mn] >= 0.18
            sellT2 = sellT1 or level5mh or level6mh or level126
            level0b = df ["ww1"] [mn] <= 0.3  and df ["aroond"] [mn] >= 92   and df ["amb13"] [mn] <= 0.1 and  df ["ci"] [mn] >= 0.40 and  df ["BUY2"] [mn] >= 0.95 
            level123 =  df ["ww1"] [mn] <= 0.01 and df ["amb99"] [mn] <= 0.01
            level5b =  df ["amb55"] [mn] <= 0.15 and   df ["ambb5"] [mn] >= 0.55 and   df ["ci"] [mn] <= 0.05
            level6b = df ["ww1"] [mn] <= 0.1  and  df ["ww7"] [mn] >= 0.5 and  df ["BUY2"] [mn] <= 0.1
            level7b = df ["ww1"] [mn] <= 0.6  and  df ["ww7"] [mn] >= 0.9 and  df ["BUY2"] [mn] <= 0.15 and df ["aroond"] [mn] >= 92
            level8b =  df ["amb55"] [mn] <= 0.15 and   df ["ambb5"] [mn] >= 0.72 and   df ["ci"] [mn] <= 0.1
            level9b = df ["amb55"] [mn] <= 0.2 and df ["amb15"] [mn] >= 0.65 and df ["amb15"] [mn] >= 0.65 and df ["amb14"] [mn] >= 0.6 and df ["amb13"] [mn] >= 0.5 and  df["rsiK"][mn] <= 30.0
            level11b = df ["amb13"] [mn] <= 0.2 and df ["amb14"] [mn] <= 0.2 and  df ["amb15"] [mn] >= 0.5 and df ["amb55"] [mn] <= 0.55 and df ["ci"] [mn] <= 0.06
            level1b=  df ["amb14"] [mn] >= 0.6 and df ["amb55"] [mn] <= 0.2 and  df ["ci"] [mn] <= 0.2
            
            if level0b or level123  or level6b or level7b or level1b or level11b or level9b or level8b or level5b:
                situation4.append(1.0)
            elif sellT2 or (df["BUY2"][mn] <= 0.1 and df["amb55"][mn] >= 0.8) or (df["ci"][mn] >= 0.90 and df["amb55"][mn] >= 0.90 and df["amb13"][mn] >= 0.6) :
                situation4.append(2.0)
            else:
                situation4.append(0.0)
        return situation4
class BuySellshortTerm(AbsBuySell):
    def BuySell(self,df : df) -> list:
        situation4 = []
        lagestammb5 = np.array(df['ambb5'].nlargest(n=50))[49]

        for mn in range(len(df.index)):
            level0 = df["amb13"][mn] >= 0.95 and df["amb14"][mn] >= 0.95 and df["amb2"][mn] >= 0.85 and df["amb0"][
                mn] >= 0.85
            level1 = df["amb13"][mn] >= 0.85 and df["amb14"][mn] >= 0.80 and df["amb2"][mn] >= 0.63 and df["amb0"][
                mn] >= 0.69
            level2 = df["amb13"][mn] >= 0.69 and df["amb14"][mn] >= 0.70 and df["amb2"][mn] >= 0.70 and df["amb0"][
                mn] >= 0.75
            level7 = df["amb2"][mn] >= 0.95 and df["amb99"][mn] >= 0.98
            level10 = df["amb99"][mn] >= 0.95 and df["amb2"][mn] >= 0.80 and df["ambb5"][mn] >= 0.45 and df["rsiK"][
                mn] >= 0.63
            level15 = df["ww1"][mn] >= 0.70 and df["aroonu"][mn] >= 92 and df["ww1"][mn] <= df["ww"][mn]
            supertop = level0 or level1 or level2 or level7
            sellT0 = supertop or level7 or level10 or level15
            level3h = df["amb13"][mn] >= 0.67 and df["amb14"][mn] >= 0.67 and df["amb2"][mn] >= 0.80
            level4h = df["amb14"][mn] >= 0.55 and df["amb2"][mn] >= 0.75 and df["aroonu"][mn] >= 92 and df["ambb5"][
                mn] >= 0.70 and df["rsiK"][mn] >= 0.82 and df["ci"][mn] >= 0.73
            sellT1 = sellT0 or level4h or level3h
            level5mh = df ["BUY2"] [mn] <=0.94 and df ["amb2"] [mn] >=0.30 and   df ["amb13"] [mn] >= 0.18 and   df ["amb0"] [mn] >= 0.45
            level126 =  df["amb55"][mn] >= 0.90 and  df["rsiK"][mn] >= 0.95 and  df["ci"][mn] >= 0.75 and df["amb13"][mn] <= 0.1
            level6mh = df ["amb13"] [mn] >= 0.75 and df ["amb14"] [mn] >= 0.70 and df ["amb15"] [mn] >= 0.70 and df ["amb55"] [mn] >= 0.55 and df ["aroonu"] [mn] >= 92 and df ["aroond"] [mn] <= 30 and df ["ambb5"] [mn] >= 0.75 and df ["ci"] [mn] >= 0.75 and df ["rsiK"] [mn] >= 0.83  and df ["amb99"] [mn] >= 0.18
            sellT2 = sellT1 or level5mh or level6mh
            level0b = df ["ww1"] [mn] <= 0.3  and df ["aroond"] [mn] >= 92   and df ["amb13"] [mn] <= 0.1 and  df ["ci"] [mn] >= 0.40 and  df ["BUY2"] [mn] >= 0.95 
            level123 =  df ["ww1"] [mn] <= 0.01 and df ["amb99"] [mn] <= 0.01
            level5b = df ["ww1"] [mn] <= 0.1  and  df ["ww7"] [mn] >= 0.5 and df ["aroond"] [mn] >= 92  and  df ["ci"] [mn] <= 0.20
            level6b = df ["ww1"] [mn] <= 0.1  and  df ["ww7"] [mn] >= 0.5 and  df ["BUY2"] [mn] <= 0.1
            level7b = df ["ww1"] [mn] <= 0.6  and  df ["ww7"] [mn] >= 0.9 and  df ["BUY2"] [mn] <= 0.15 and df ["aroond"] [mn] >= 92
            # level6b or level7b
            if  False:
                situation4.append(1.0)
            #sellT2
            elif False:
                situation4.append(2.0)
            else:
                situation4.append(0.0)
        return situation4
class BuySellshortTermMin(AbsBuySell):
    def BuySell(self,df : df) -> list:
        situation4 = []
        lagestammb5 = np.array(df['ambb5'].nlargest(n=50))[49]

        for mn in range(len(df.index)):
            level0 = df["amb13"][mn] >= 0.90 and df["amb14"][mn] >= 0.80 and df["amb2"][mn] >= 0.80 and df["amb0"][
                mn] >= 0.80
            level1 = df["amb13"][mn] >= 0.80 and df["amb14"][mn] >= 0.80 and df["amb2"][mn] >= 0.63 and df["amb0"][
                mn] >= 0.69
            level2 = df["amb13"][mn] >= 0.69 and df["amb14"][mn] >= 0.70 and df["amb2"][mn] >= 0.70 and df["amb0"][
                mn] >= 0.75
            level7 = df["amb2"][mn] >= 0.95 and df["amb99"][mn] >= 0.98
            level10 = df["amb99"][mn] >= 0.80 and df["amb2"][mn] >= 0.80 and df["ambb5"][mn] >= 0.45 and df["rsiK"][
                mn] >= 0.63
            level15 = df["ww1"][mn] >= 0.90 and df["aroonu"][mn] >= 92 and df["ww1"][mn] <= df["ww"][mn] and df["ambb5"][mn] <= 0.2
            supertop = level0 or level1 or level2 or level7
            sellT0 = supertop or level7 or level10 or level15
            level3h = df["amb13"][mn] >= 0.67 and df["amb14"][mn] >= 0.67 and df["amb2"][mn] >= 0.80
            level4h = df["amb14"][mn] >= 0.55 and df["amb2"][mn] >= 0.75 and df["aroonu"][mn] >= 92 and df["ambb5"][
                mn] >= 0.70 and df["rsiK"][mn] >= 0.82 and df["ci"][mn] >= 0.73
            level126 =  df["amb55"][mn] >= 0.80 and  df["rsiK"][mn] >= 0.95 and  df["ci"][mn] >= 0.70
            level0b = df ["ww1"] [mn] <= 0.3  and df ["aroond"] [mn] >= 92   and df ["amb13"] [mn] <= 0.1 and  df ["ci"] [mn] >= 0.40 and  df ["BUY2"] [mn] >= 0.95 
            level123 =  df ["ww1"] [mn] <= 0.01 and df ["amb99"] [mn] <= 0.01
            level5b = df ["ww1"] [mn] <= 0.1  and  df ["ww7"] [mn] >= 0.5 and df ["aroond"] [mn] >= 92  and  df ["ci"] [mn] <= 0.20
            level6b = df ["ww1"] [mn] <= 0.1  and  df ["ww7"] [mn] >= 0.5 and  df ["BUY2"] [mn] <= 0.1
            level7b = df ["ww1"] [mn] <= 0.6  and  df ["ww7"] [mn] >= 0.9 and  df ["BUY2"] [mn] <= 0.15 and df ["aroond"] [mn] >= 92
            level112b =  df ["amb1111"][mn] >=0.001 and  df ["ambb"][mn] <=0.1 and df ["aroond"] [mn] >= 92 and df ["amb99"] [mn] <= 0.03 and df ["amb55"] [mn] <= 0.07
            #level0b or level123 or level5b or level6b or level7b
            if  False :
                situation4.append(1.0)
            #level7 or level15 or level0 or level126
            elif False:
                situation4.append(2.0)
            else:
                situation4.append(0.0)
        return situation4