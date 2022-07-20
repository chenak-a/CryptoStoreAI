from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd
#Strategy pattern
class AbsCorrection(ABC):
    @abstractmethod
    def correction(self,data : pd.DataFrame) -> pd.DataFrame:
        """correction layer is ame to remove inconsistencies by 
        overlaying data of an Asset in different time Frame.
        (see the bigger picture) 

        Args:
            data (pd.DataFrame): pd 

        Returns:
            pd.DataFrame: pd
        """
        pass
class CorrectionLayer1(AbsCorrection):
    def correction(self,data : pd.DataFrame) -> pd.DataFrame: 
    
       
        for x in range(len(data.index)):
            try :

                if data.at[x,'BUYSELL']  == 1.0: 
                    if  data.at[x,'prmacdin']-data.at[x-1,'prmacdfast']  < 0.3 and  data.at[x,'prmacdin'] < data.at[x-1,'prmacdfast'] or  data.at[x,'amb55']-data.at[x-4,'amb55'] < -0.01  :
                        data.at[x,'BUYSELL'] = 0.0
                    if data.at[x,'BUY2'] < 0.13 or data.at[x,'pck3d']  > 0.2 or data.at[x,'pk3d']  > 0.75 and  data.at[x,'amb55']-data.at[x-2,'amb55']  > 0.0 or data.at[x,'pk1d']  < 0.2 and data.at[x,'pck1d']  < -0.3 and data.at[x,'pck1d']-data.at[x-2,'pck1d']  >= 0.0 or data.at[x,'pck3d']-data.at[x-1,'pck3d'] >= 0.0 and  data.at[x,'pck3d']<-0.2 or data.at[x,'pck3d'] > -0.02 and data.at[x,'pck3d']-data.at[x-1,'pck3d'] >= 0.0   :
                        data.at[x,'BUYSELL'] = 1.0

                ...
            except :
                pass
            if  data.at[x,'BUYSELL']  == 0.0:
                layer1level0 = data.at[x,'pk1d'] > 0.8 and data.at[x,'amb14'] > 0.5 and data.at[x,'amb15'] > 0.5 and data.at[x,'amb1'] > 0.1
                layer1level1 =  data.at[x,'pk1d'] > 0.7 and  data.at[x,'amb14'] > 0.7 and data.at[x,'amb13'] < 0.2 and data.at[x,'amb14'] > data.at[x,'amb13'] 
                if layer1level0 or layer1level1   :
                    data.at[x,'BUYSELL'] = 2.0  
            if x <= 50:
                data.at[x,'BUYSELL'] = 0.0
        return data