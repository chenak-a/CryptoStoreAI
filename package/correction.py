from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from unittest import expectedFailure
import pandas as pd

class AbsCorrection(ABC):
    @abstractmethod
    def correction(self,data : pd.DataFrame) -> pd.DataFrame:
        pass
class CorrectionLayer1(AbsCorrection):
    def correction(self,data : pd.DataFrame) -> pd.DataFrame: 
        try :
            buysell = data[data["BUYSELL"] == 1.0] 
            for x in buysell.index:
                if ((data.at[x,'pck1d']  < 0.2 and data.at[x,'pk3d']  > 0.2 )  or (data.at[x,'pck1d']  < 0.1 and data.at[x,'pck3d']  < 0.1 ) )  :
                    data.at[x,'BUYSELL'] = 0.0
                if((data.at[x,'BUY2'] < 0.13  ) or  (data.at[x,'pk3d']  > 0.1 and data.at[x,'pck3d']  > 0.1 and data.at[x,'pck1d'] > 0.1 ) or (data.at[x,'pk1d']  < 0.15 and data.at[x,'pck1d']  < -0.4 and data.at[x,'pk3d']  < 0.11 and data.at[x,'pck3d']  > -0.1) ):
                    data.at[x,'BUYSELL'] = 1.0
                if x <= 50:
                    data.at[x,'BUYSELL'] = 0.0
            print(buysell)
        except :
            pass
      
        return data
    