# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 12:35:54 2021

@author: danielpazing

www.logsis.com.ar

Realiza graficos de velas de un dtaframe de precios de un ticker
que tenga el formato OCLHV
sin necesidad de ninguna libreria adicional a matplotlib

"""
import matplotlib.pyplot as plt
import numpy as np


########## GRAFICADORES

def graf_velas(data):
    """
    Construye un grafico de velas directamente desde matplotlib
    Input: grafico formato open.close.high.low
    """

    data["Vardia"] = abs(data["Open"] - data["Close"])
    data["Rango"] =data["High"]-data["Low"]
    data["Pmedio"]=(data["High"]+data["Low"]+data["Open"]+data["Close"])/4
    data["Base"] = np.where(data["Open"]<data["Close"] ,data["Open"],data["Close"])
    data["Color"]= np.where(data["Open"]<data["Close"] ,"Green","Red")
    bar_pos=data.Vardia.loc[data["Open"]<data["Close"]]
    bar_neg=data.Vardia.loc[data["Open"]>data["Close"]]
    
    plt.grid(color="lightgray",linestyle='-')
    plt.bar(data.index, data["Rango"], bottom=data["Low"],width=0.1,color="black" )
    plt.bar(data.index, data["Vardia"], bottom=data["Base"],width= 1,color=data.Color )
    plt.plot(data.index, data["Pmedio"],color="black", linestyle="--",linewidth=1)
        
    return data["Pmedio"]