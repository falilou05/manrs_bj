#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:57:13 2020

@author: shellbulls
"""


import pandas as pd
import urllib.request, json
import math
import re, requests 
from pandas import ExcelWriter


def remplacer(c1,c2,ch):
    n=len(ch)
    i=0
    while i<n:
        if c1==ch[i]:
            ch=ch[:i]+c2+ch[i+1:]
            n-=1
        i+=1
    return ch
#url = 'http://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest'
asn_url = pd.read_csv('asn_bj.txt',sep = "|")
prefix = pd.read_csv('prefix_bj.txt',sep = "|")
asn_name="https://stat.ripe.net/data/as-overview/data.json?resource=AS"
rpki="https://stat.ripe.net/data/rpki-validation/data.json?resource="
#https://stat.ripe.net/data/rpki-validation/data.json?resource=36924&prefix=156.38.64.0/19
rpki1="&prefix="
#afri_url.to_csv('afrinic.csv', index=False)
#df_new = pd.read_csv('afrinic.csv')
#afri = afri_url.to_json()
#print(b)
#curl="".join(rl+ip)
slash="/"
asn=[]
cidr=[]
nas_name=[]
nas_num=[]
asn_rpki=[]
asn_ro=[]
z=0
#boucle servant au calcul du mask des prefix
for i in range(0,len(prefix)):
    indice=math.log(int(prefix.iloc[i]['host_nb']),2)
    indice=32-int(indice)
    cidr.append(indice)
prefix['indice']=cidr

#Boucle servant à déterminer le nom des ASN
for j in range(0, len(asn_url)):
    curl="".join(asn_name+str(asn_url.iloc[j]['num']))
    resp=urllib.request.urlopen(curl)
    data=json.loads(resp.read().decode())
    asn.append(str(data["data"]["holder"]))
asn_url['AS_NAME']=asn
print("unique ASN")
new_asn=asn_url.drop_duplicates(subset=['identification'])
#print(new_asn)

for k in range(0, len(new_asn)):
    for i in range(0,len(prefix)):
        if str(prefix.iloc[i]['identification']) == str(new_asn.iloc[k]['identification']):
            nas_name.append(str(new_asn.iloc[k]['AS_NAME']))
            nas_num.append(str(new_asn.iloc[k]['num']))
prefix['ASN_NAME']=nas_name
prefix['ASN_NB']=nas_num 
           #print(data)
       #asn.append(str(data["data"]["holder"]))
#prefix['AS']=nas_name
#for j in range(0,len(asn_url)):
#    for i in range(0,len(prefix)):
#        if asn_url.iloc[j]['identification'] == prefix.iloc[i]['identification']:
            #as_name.append(asn_url.iloc[j]['AS_NAME'])
#            name=str(asn_url.iloc[j]['AS_NAME'])
#            nas_name.append(name)

#prefix['AS']=nas_name
            

#url="https://stat.ripe.net/data/rir/data.json?resource=37136&lod=2"

#boucle servant à déterminer les RO & ROA des AS
ro="https://stat.ripe.net/data/routing-status/data.json?resource="
ro2="%2F"
for i in range(0,len(prefix)):
    curl2="".join(rpki+str(prefix.iloc[i]['ASN_NB'])+rpki1+str(prefix.iloc[i]['IP'])+slash+str(prefix.iloc[i]['indice']))
    curl3="".join(ro+str(prefix.iloc[i]['IP'])+ro2+str(prefix.iloc[i]['indice']))
    res=urllib.request.urlopen(curl2)
    res1=urllib.request.urlopen(curl3)
    data2=json.loads(res.read().decode())
    data3=json.loads(res1.read().decode())
    #print(data2["data"]["validating_roas"]["0"]["origin"])
    check_ro=data3["data"]["origins"]
    check_rpki=data2["data"]["validating_roas"]
    if check_rpki:
        asn_rpki.append("yes")
    else:
        asn_rpki.append("no")
    if check_ro:
        asn_ro.append("yes")
    else:
        asn_ro.append("no")
prefix['RPKI']=asn_rpki
prefix['RO']=asn_ro

#new_t=tabl[1:-1] 
#b=remplacer("'",'"',new_t)


#url = "https://stat.ripe.net/data/prefix-overview/data.json?max_related=50&resource=41.222.192.58"
#response=urllib.request.urlopen(url)

#data1=json.loads(response.read().decode())
#data2=json.loads(response2.read().decode())
#tableau=str(data1["data"]["rirs"][0]["rir"])
#tableau2=str(data2["data"]["holder"])
#print(tableau)
#print("final")
#print(len(nas_name))
#print(len(prefix))
print(prefix)
writer = ExcelWriter('manrs.xlsx')
asn_url.to_excel(writer,'ASN')
prefix.to_excel(writer,'prefix')
writer.save()
#new_t=tableau[1:-1]
#b=remplacer("'",'"',new_t)
#w=json.dumps(b)
#print(w)

#print(json.dumps(new_t["data"]["rirs"][0]["rir"]))
#print(afri_url)
#for i in range(0, len(afri_url)):
 #   print(afri_url.iloc[i]['num'])
#print(data1["data"]["rirs"])
