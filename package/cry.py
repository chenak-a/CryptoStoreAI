import numpy as np
from scipy import stats

def EWMArsi (price,limi):
    defprice = price.diff()
    g , l = defprice.copy() , defprice.copy()
    g[g < 0.0]=0.0
    l[l > 0.0]=0.0
    ewmag = g.ewm(com=(limi-1),min_periods=limi).mean()
    ewmal =l.abs().ewm(com=(limi-1),min_periods=limi).mean()
    rs =ewmag/ewmal

    rsi = 100 -(100/(1+rs))
    rsi1= rsi[len(rsi)-1]


    return rsi
def rsiso(rsi,KD):
    rsimin=rsi.rolling(14).min()
    rsimax=rsi.rolling(14).max()
    stochrsi = (rsi - rsimin)*100 / (rsimax - rsimin)
    krsi=stochrsi.rolling(3).mean()
    drsi=krsi.rolling(3).mean()
    K =krsi[len(krsi)-1]
    D =drsi[len(drsi)-1]
    if(KD == "k"):
        return K
    elif (KD == "D"):
        return D
    elif(KD == "KD"):
        print("Stoch rsi K% :" + str(K))
        print("Stoch rsi D% :" + str(D))
        pass
    elif(KD == "TK"):
        return krsi
    elif (KD == "TD"):
        return drsi

def ma (price,limi,get):
    pricema = price.ewm(span=limi).mean()
    pricelast= pricema[limi-1]
    if(get == "P"):
        return pricelast
        print("Ma :" + str(pricelast))
    elif(get =="R"):
        return pricema


def volosc (volume,get):
    v1 , v2  = volume.copy(), volume.copy()
    vma1= v1.ewm(span=35).mean()
    vma2= v2.ewm(span=5).mean()
    vma= ((vma2-vma1)/vma1)*100
    if (get == "P"):
        print("Volumeosc: " + str(vma[len(vma) - 1]))
    elif (get == "R"):
        return vma


def pentevolosc(Volumsoci,VT):
    if(VT == "V"):
        y=np.array(Volumsoci)
        x=np.arange(len(Volumsoci))
        slope, intercept, r, p, std_err = stats.linregress (x, y)
        return slope
    elif(VT == "T"):
        penVoc =[0]
        for n in range(len(Volumsoci)):
            try:
                y = np.array([Volumsoci[n], Volumsoci[n+1]])
                x = np.arange(2)
                slope, intercept, r, p, std_err = stats.linregress (x, y)
                penVoc.append(slope)
            except:
                pass
        return penVoc
def pentrsi(rsi,VT):
    if (VT == "V"):
        y = np.array (rsi)
        x = np.arange (len (rsi))
        slope, intercept, r, p, std_err = stats.linregress (x, y)
        return slope
    elif (VT == "T"):
        penrsi = [0,0]
        for n in range (len (rsi)):
            try:
                y = np.array ([rsi [n], rsi [n + 1], rsi [n + 2]])
                x = np.arange (3)
                slope, intercept, r, p, std_err = stats.linregress (x, y)
                penrsi.append (slope)
            except:
                pass
        return penrsi
def pentrsiK(rsiK,VT):
    if (VT == "V"):
        y = np.array (rsiK)
        x = np.arange (len (rsiK))
        slope, intercept, r, p, std_err = stats.linregress (x, y)
        return slope
    elif (VT == "T"):
        penrsiK=[0]
        for n in range (len (rsiK)):
            try:
                y = np.array ([rsiK [n], rsiK [n + 1]])
                x = np.arange (2)
                slope, intercept, r, p, std_err = stats.linregress (x, y)
                penrsiK.append (slope)
            except:
                pass
        return penrsiK
def pentrsiD(rsiD,VT):
    if (VT == "V"):
        y = np.array (rsiD)
        x = np.arange (len (rsiD))
        slope, intercept, r, p, std_err = stats.linregress (x, y)
        return slope
    elif (VT == "T"):
        penrsiD=[0]
        for n in range (len (rsiD)):
            try:
                y = np.array ([rsiD [n], rsiD [n + 1]])
                x = np.arange (2)
                slope, intercept, r, p, std_err = stats.linregress (x, y)
                penrsiD.append (slope)
            except:
                pass
        return penrsiD
def volumegain(Volume,VT):
    if (VT == "V"):
        VG=Volume[0]-Volume[1]
        return VG
    elif (VT == "T"):
        VGTN=[0]
        for n in range (len (Volume)):
            try:
                VGT=Volume [n] - Volume [n+1]
                VGTN.append(VGT)
            except:
                pass
        return VGTN
def macd(price,C26h):
    ewm12 = price.ewm (span = 12, adjust = False).mean ()
    ewm26 = price.ewm (span = 26, adjust = False).mean ()
    macd = ewm12 - ewm26
    histogram=macd.ewm (span = 9, adjust = False).mean ()
    histogrammacd=macd-histogram
    if(C26h == "macd"):
        return macd
    elif(C26h == "histogram"):
        return histogram
    elif(C26h == "histogrammacd"):
        return histogrammacd
def efi13(price,volume):
    difprice=price.diff(13)*volume
    return difprice
def penthistogram(histogram,VT):
    if (VT == "V"):
        y = np.array (histogram)
        x = np.arange (len (histogram))
        slope, intercept, r, p, std_err = stats.linregress (x, y)
        return slope
    elif (VT == "T"):
        penhistogram = [0]
        for n in range (len (histogram)):
            try:
                y = np.array ([histogram [n], histogram [n + 1]])
                x = np.arange (2)
                slope, intercept, r, p, std_err = stats.linregress (x, y)
                penhistogram.append (slope)
            except:
                pass
        return penhistogram
def prmacd(macd):
    macdmin=macd[macd.argmin()]
    macdmax=macd[macd.argmax()]
    macdto=macdmax-macdmin
    macd1=((macd-macdmin)/macdto)*100
    return macd1
def aroon(price,UD):
    m = 14
    list = []
    for _ in range(m):
        list.append(0)
    x=price.index.stop
    y=x-m
    for n in range(y):
        if (UD == "U"):
            nb = m+n
            prmax=price[n:nb].argmax()
            nbmax=nb-prmax
            arup=((m-nbmax)/m)*100
            list.append(arup)
        elif(UD == "D"):
            nb = m + n
            prmin = price[n:nb].argmin()
            nbmin = nb - prmin
            ardw = ((m - nbmin) / m) * 100
            list.append(ardw)
    la=np.array(list)
    return la

def la1 (list1,list2,index):

   list = [1 for x in range(index)]
   list01= [0 for x in range(index)]
   list12 = []
   list22 = []
   list12 = list1
   list22 = list2
   print("idnex : " ,index)
   for a in range(index):
        for b in range(len(list12)):
            if (list12[b]== a):
                list[a] = 0

                pass
        for c in range(len(list22)):
            if (list22[c] == a):
                list[a] = 0
                pass

   la = np.array(list)


   return la
def la (list1,index):

   list = [0 for x in range(index)]

   list12 = []

   list12 = list1

   print("idnex : " ,index)
   for a in range(index):
        for b in range(len(list12)):
            if (list12[b]== a):
                list[a] = 1

                pass

   la = np.array(list)


   return la