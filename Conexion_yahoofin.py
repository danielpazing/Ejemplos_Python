# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:56:05 2021

@author: Daniel 

LECTURA BASICA TICKER
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import time
import datetime
from datetime import date

import requests
import json
import yfinance as yf
import pandas_datareader as pdr


def yahoo_reciente(symbol,delta_dias=30 ):
    """
    Parameters
    ----------
    symbol : <string> ticker
    delta_dias : <entero> dias hacia el pasado desde hoy. default=30.

    Returns
    -------
    df : dataframe OHLCV, compresion DIARIA
    """
    ##### establecer time renge partiendo de HOY
    hoy=date.today()
    fecha_hoy =  hoy.isoformat()
    ini = hoy - datetime.timedelta(days=delta_dias)
    fecha_ini = ini.isoformat()

    print("Descargando.....", symbol)
    df = pdr.DataReader(symbol, 'yahoo', fecha_ini, fecha_hoy)
    return df


def yahoo_hist(symbol,fecha_ini,fecha_fin, compresion):
    """
    Parameters
    ----------
    symbol : <string> ticker
    fecha_ini, fecha_fin : <date> isoformat yyyy-mm-dd
    compresion: 1m,5m,15m,30m,60m(default),1h,1d,1wk,1mo
    para default 60m, histgoria maxima es 720 dias
    Returns
    -------
    df : dataframe OHLCV, compresion definir
    """

    print("Descargando.....", symbol)
    df = yf.download(symbol, start=fecha_ini, end=fecha_fin, interval="60m")
    return df
