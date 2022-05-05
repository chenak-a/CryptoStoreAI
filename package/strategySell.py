
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
            sellT1 = sellT0 or level4h or level3h


            if (df["ambb5"][mn] >= 0.8) and mn > 30:
                situation4.append(1.0)
            elif (sellT1):
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

            if (df["ambb5"][mn] >= 0.63 and df["BUY2"][mn] >= 0.88 or df["ambb5"][mn] >= 0.63 and df["BUY2"][mn] <= 0.15   ) and mn > 30:

                situation4.append(1.0)
            elif (sellT1):
                situation4.append(2.0)
            else:
                situation4.append(0.0)
        return situation4