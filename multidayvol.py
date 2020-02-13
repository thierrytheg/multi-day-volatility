import os, sys
import numpy as np
import pandas as pd
from decimal import *
import time
import matplotlib.pyplot as plt
import requests
import json

sys.__stdout__=sys.stdout

KEY=''

ETF=['SPY','TLT','GLD','XLE']

plt.style.use('fivethirtyeight')

for a in ETF:

    dailyprice='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s&outputsize=compact' %(a,KEY)

    first=requests.get(dailyprice)
    info=json.loads(first.text)
    date=info['Time Series (Daily)']
    df =pd.DataFrame(columns=['Date','Price'])
    liste1={}
    for eachdate in date:
        details=date[eachdate]
        close=details['4. close']
        liste1.update({eachdate:close})
    listekey=[]
    listevalue=[]
    for key in sorted(liste1.keys()):
        df=df.append({'Price':(round(float((liste1[key])),2))},ignore_index=True)
        save=a+'.csv'
        df.to_csv(save)
        listekey.append(key)
        listevalue.append(liste1[key])



    file='%s.csv' %a
    handle=open(file,'r')
    stdv=[]
    price=[]
    newprice=[]
    for x in handle:
        line=x.strip('\n')
        lineclean=line.split(',')
        price.append(lineclean[2])



    for x in price:
        try:
            ss=np.array(Decimal(x).quantize(Decimal('.01')))
            newprice.append(ss)
        except Exception:
            pass


    y=-1
    liste=[]
    for index,price in enumerate(newprice):
        y=y+1
        z=y+5
        x=newprice[y:z]

        if len(x) != 5:
            pass
        else:
            liste.insert(0,x)
   
    for i in liste:
        stdev=np.std(i)
        stdv.insert(0,stdev)

        
    m_=[]
    for m in range(len(stdv)):
        m_.append(m)
    
    plt.subplot(((len(ETF)//4)+1),2,(ETF.index(a)+1))
    plt.title(a)
    plt.plot(m_,stdv,lw=5)
    plt.tick_params(labelbottom=False,bottom=False)

plt.tight_layout(pad=0.5)
fig=plt.gcf()
plt.show()

