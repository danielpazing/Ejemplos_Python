# -*- coding: utf-8 -*-
"""
Created on Tue Mar24 2021

@danielpazing: Daniel Paz

www.logsis.com.ar

Conexion_IOL API
FUNCIONES PARA CONECTARSE A LA API DE IOL

SE DEBE TENER EL ARCHIVO DE USER Y PASSWODR EN FORMATO TXT EN LA MISMA CARPETA
 
"""

import pandas as pd
import time
import datetime
import requests
import json
import pandas as pd
from datetime import date
import datetime as dt

##### definir constantes
pd.options.display.max_columns=4
pd.options.display.precision=2

### VARAIBLES GLOBALES
myuser= ""
mypass= ""
token=""
atoken=""

### leer archivo txt con credenciales de acceso a cta iol
def leer_claves_txt(nombre_archivo):
    txt= pd.read_csv(nombre_archivo)
    myuser=txt.iloc[0,0]
    mypass=txt.iloc[0,1]
    return myuser, mypass

##### establecer time renge partiendo de HOY
delta_dias= 365*5
hoy=date.today()
fecha_hoy =  hoy.isoformat()
ini = hoy - datetime.timedelta(days=delta_dias)
fecha_ini = ini.isoformat()
t_inicio= datetime.datetime.utcnow()

wwwsand = "https://api-sandbox.invertironline.com"
wwwiol = "https://api.invertironline.com"


### definir funciones

def hora():
    hora1=dt.datetime.now().strftime("%H:%M:%S")
    print(hora1)
    return hora

def pedir_token(myuser,mypass):
    url = "https://api.invertironline.com/token"
 
    data= {"username": myuser, "password": mypass, "grant_type":"password"}
    r= requests.post(url=url, data=data).json()
    token= r
    print("Respuesta: ",r)
    return r

def actualizar_token(tk):
    
    exp=dt.datetime.strptime(tk[".expires"], "%a, %d %b %Y %H:%M:%S GMT")
    ahora= dt.datetime.utcnow()
    tiempo = exp-ahora
    dias=tiempo.days
    
    if dias==0:
        tokenOK= tk
        print ("token valido por:",tiempo)
    else:
        tokenOK= pedir_token(myuser,mypass)
        print("nuevo token")
        token=tokenok
        atoken=token["access_token"]
        
    return tokenOK


def iol_getHist( ticker, desde,hasta,atoken,market="bCBA",compresion="d"):
    """ 
    Parameters
    ----------
    ticker , desde:fecha_ini, hasta:fecha_fin (mm-dd-yyyy) , compresion= "d" , "h"
    Returns
    -------
    dataframe : Index(['ultimoPrecio', 'variacion', 'apertura', 'maximo', 'minimo',
       'fechaHora', 'tendencia', 'cierreAnterior', 'montoOperado',
       'volumenNominal', 'precioPromedio', 'moneda', 'precioAjuste',
       'interesesAbiertos', 'puntas', 'cantidadOperaciones'],
      dtype='object')
        
    """
    ########## reaparado!!!!!   26-03-2021
    
    url_base= "https://api.invertironline.com/api/v2/"
    endpoint= "/Titulos/"+ticker+"/Cotizacion/seriehistorica/" 
    Tx_3= "/sinAjustar"
    url3= url_base +market+endpoint + desde +"/"+hasta + Tx_3
    headers={"Authorization":"Bearer " +atoken}
    
    datos_serie= requests.get(url=url3,headers=headers).json()
    print( ticker + " : Descargado a dataframe")
    
    data= pd.DataFrame(datos_serie)
    data.index=pd.to_datetime(data.fechaHora)
    data=data.resample(compresion).last()
    data["Low"]=data.minimo
    data["High"]=data.maximo
    data["Date"]=data.index
    data["Close"]=data.ultimoPrecio
    data["Open"]=data.apertura
    data["Volume"]=data.montoOperado
    data=data.drop(["moneda","interesesAbiertos","puntas"], axis=1)
    data=data.dropna()   
    return data

def iol_panel(instrumento, panel, pais,atoken):
    
    """
    Devuelve['simbolo', 'ultimoPrecio', 'variacionPorcentual', 'apertura',
       'maximo', 'minimo', 'ultimoCierre', 'volumen', 'cantidadOperaciones',
       VolMedioOper]
    """

    url_base= "https://api.invertironline.com/api/v2/"
    endpoint= "Cotizaciones/"+instrumento+"/"+panel+"/"+pais
    url= url_base+endpoint
    headers={"Authorization" :"Bearer " +atoken}        
    data= requests.get(url=url, headers= headers).json()["titulos"]
    tabla= pd.DataFrame.from_dict(data)
    #tabla=tabla.drop(["puntas","fechaVencimiento","tipoOpcion","precioEjercicio","fecha","mercado","moneda"], axis=1)      
    tabla["VolMedioOper"] = tabla["volumen"]/tabla["cantidadOperaciones"]
    return tabla
    
def iol_precio(mercado, ticker, atoken):
    
    url_base= "https://api.invertironline.com/api/v2/"
    endpoint= mercado+"/Titulos/"+ticker+"/Cotizacion"    
    url=url_base+ endpoint
    
    headers={"Authorization" :"Bearer " +atoken}        
    data= requests.get(url=url, headers= headers).json()
    #print("Ultimo Precio ",ticker, data["ultimoPrecio"]  , " - Tendencia:", data['tendencia'])
    return data


def iol_cuenta():

    url_base= "https://api.invertironline.com/api/v2/"
    endpoint= "estadocuenta"
    url= url_base+endpoint
    headers={"Authorization" :"Bearer " +atoken}        
    data= requests.get(url=url, headers= headers).json()
    print("cuenta Nro: ",data["cuentas"][0]["numero"])
    return(data)
    
def iol_portafolio(atoken,pais="Argentina"):

    url_base= "https://api.invertironline.com/api/v2/"
    endpoint= "portafolio/"+pais
    url= url_base+endpoint
    headers={"Authorization" :"Bearer " +atoken}        
    data= requests.get(url=url, headers= headers).json()
    #df=pd.DataFrame(data["activos"])


    return data

def iol_operaciones(atoken):
 
    url_base= "https://api.invertironline.com/api/v2/"
    endpoint= "Operaciones/"
    url= url_base+endpoint
    headers={"Authorization" :"Bearer " +atoken}        
    data= requests.get(url=url, headers= headers).json()
    df=pd.DataFrame(data)
    print(df)
    return(df)

#####################################
def mepccl(atoken):
   
    ##### establecer time renge partiendo de HOY
    delta_dias= 5
    hoy=date.today()
    fecha_hoy =  hoy.isoformat()
    ini = hoy - dt.timedelta(days=delta_dias)
    fecha_ini = ini.isoformat()
    
    ### leer usuario y password - generar 1er token
    
          
    tickers2 = ["GD30D","AL30D","GD30C","AL30C","GD30","AL30"]
    precios=pd.DataFrame()
    
    for ticker in tickers2:
    
        data=iol_getHist( ticker, desde=fecha_ini,hasta=fecha_hoy,atoken=atoken,market="bcba")
        precios[ticker]=data.Close
   
    precios["MEP"]=precios["GD30"]/ precios["GD30D"]
    precios["CCL"]= precios["GD30"] /precios["GD30C"]
    
    mephoy=round(precios["MEP"][-1],4)
    cclhoy=round(precios["CCL"][-1],4)
    
    """
    plt.plot(precios.index, precios.AL30D, color="blue")
    plt.plot(precios.index, precios.GD30D, color="purple")
    plt.legend(["AL30D","GD30D"])
    plt.show()
    plt.plot(precios.index, precios.MEP)
    plt.plot(precios.index, precios.CCL)
    plt.legend(["MEP","CCL"])
    plt.show()
    """
    
    print("MEP= ", mephoy,"CCL= ",cclhoy)
    
    return mephoy, cclhoy
    
    
