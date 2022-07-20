from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import pandas as df
import numpy as np
#Strategy pattern
class AbsBuy(ABC):
    @abstractmethod
    def Buy(self,df : df) -> bool:
        """decision tree

        Returns:
            list: BUY(1) and sell(2) point 
        """
        pass
class BuyLongTerm(AbsBuy):
    def Buy(self,df : df,mn :int) -> bool:
        level7b = df ["ww1"] [mn] <= 0.6  and  df ["ww7"] [mn] >= 0.9 and  df ["BUY2"] [mn] <= 0.15 and df ["aroond"] [mn] >= 92
        return level7b
class BuymidTerm(AbsBuy):
    def Buy(self,df : df,mn :int) -> bool:
        level5b1 =  df ["amb55"] [mn] <= 0.15 and   df ["ambb5"] [mn] >= 0.55 and   df ["ci"] [mn] <= 0.5
        level12341 =  df ["ww1"] [mn] <= 0.05 and df ["amb99"] [mn] <= 0.01 and df ["BUY2"] [mn] >= 0.96
        level7b = df ["ww1"] [mn] <= 0.6  and  df ["ww7"] [mn] >= 0.87 and  df ["BUY2"] [mn] <= 0.15 and df ["aroond"] [mn] >= 92
        level1b=  df["ambb5"][mn] >= 0.7 and  df ["amb15"] [mn] <= 0.1 and df ["amb14"] [mn] <= 0.1 and df ["amb13"] [mn] <= 0.1  and df ["amb55"] [mn] <= 0.1 and df ["ww1"] [mn] <= 0.025
        level0b1 = df ["ww1"] [mn] <= 0.3  and  df ["ci"] [mn] >= 0.20    and  df ["ci"] [mn] <= 0.40 and  df ["BUY2"] [mn] >= 0.95 and  df ["amb13"] [mn] >= 0.55 and df ["ww6"] [mn] <=0.2
        level0b = df ["ww1"] [mn] <= 0.3  and df ["aroond"] [mn] >= 92   and df ["amb13"] [mn] <= 0.1 and  df ["ci"] [mn] >= 0.40 and  df ["BUY2"] [mn] >= 0.95 
        level123 =  df ["ww1"] [mn] <= 0.01 and df ["amb99"] [mn] <= 0.01
        level5b =  df ["amb55"] [mn] <= 0.15 and   df ["ambb5"] [mn] >= 0.55 and   df ["ci"] [mn] <= 0.05
        level6b = df ["ww1"] [mn] <= 0.1  and  df ["ww7"] [mn] >= 0.5 and  df ["BUY2"] [mn] <= 0.1
        level9b = df ["ww6"] [mn] >=0.24 and df ["ww1"] [mn] <=0.55 and df ["amb55"] [mn] <= 0.2 and df ["amb15"] [mn] >= 0.65 and df ["amb15"] [mn] >= 0.65 and df ["amb14"] [mn] >= 0.6 and df ["amb13"] [mn] >= 0.5 and  df["rsiK"][mn] <= 30.0 
        #level9b or level6b or level5b or level123 or level1b or level7b or level12341
        #? level0b ? level12341 xF level0b1 xF level5b1
        return  level9b or level6b or level5b or level123 or level1b or level7b or level12341
    