"""
calcular valor de dolar ccl en base a valores de adrs

Daniel Pablo Paz

"""


import yfinance as yf
import pandas as pd
import datetime
from datetime import date
import matplotlib.pyplot as plt
import numpy as np

tickers=["ARS=X","GGAL.BA",'GGAL',"YPFD.BA","YPF","PAMP.BA","PAM",]
data=pd.DataFrame(columns=tickers)

##### establecer time range partiendo de HOY
delta_dias= 360
hoy=date.today()
fecha_hoy =  hoy.isoformat()
ini = hoy - datetime.timedelta(days=delta_dias)
fecha_ini = ini.isoformat()

for ticker in tickers:
    ################ descargar valores de Yahoo Finance
    tik=yf.download( ticker, start= fecha_ini, end=hoy, interval="1d")
    data[ticker]= tik['Close']

#Esta linea es para cuando hay datos en blanco que interpole y complete los datos vacios
#Es muy util cuando se usan cocientes entre series temporales que operan distintos horarios
# inplace=True implica que retonra el resultado dentro de l mismo objeto por eso no asigna =
# entonces las dos lineas siguientes serian identicas
data.interpolate(method='linear',inplace=True)
data= data.interpolate(method='linear',inplace=False)


#Primero defino tablas a llenar, una para los tipos de dolar y otra para las brechas
dolares=pd.DataFrame()
brechas=pd.DataFrame()

#Voy armando la tabla con los ditintos dolares
dolares['Oficial'] = data["ARS=X"]

#Calculo del dolar CCL como el promedio del CCL de GGAL, PAM e YPF
dolares['CCL'] = data['GGAL.BA']*10 /data['GGAL']
dolares['CCL'] += data['YPFD.BA']*1/data['YPF'] 
dolares['CCL'] += data['PAMP.BA']*25/data['PAM']
dolares['CCL'] /= 3
dolares["CCL_EMA9"] = dolares['CCL'].ewm(span=9).mean()
dolares["CCL_EMA26"] = dolares['CCL'].ewm(span=26).mean()

print(dolares.tail())
print("CCL Ema9 Ultimo = " , dolares["CCL_EMA9"][-1])


plt.figure().suptitle("Dolar CCL")
dolares['CCL'].plot(legend="CCL")
dolares['CCL_EMA9'].plot(legend="ema9")
dolares['CCL_EMA26'].plot(legend="ema26")
data['ARS=X'].plot(legend="Oficial")




import pandas_profiling as ppf
data=data.dropna(axis=1, how="all")
ppf.ProfileReport(data)