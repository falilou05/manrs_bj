#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 23:51:05 2023

@author: shellbulls
"""

import pandas as pd
import urllib.request, json
from pandas import ExcelWriter


#url = 'http://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest'
asn_url = pd.read_csv('asn_bj.csv',sep = "|")
asn_name="https://stat.ripe.net/data/as-overview/data.json?resource=AS"
curl_ressources="https://stat.ripe.net/data/as-routing-consistency/data.json?resource=AS"
rpki="https://stat.ripe.net/data/rpki-validation/data.json?resource="
rpki1="&prefix="
slash="/"
asn=[]
cidr=[]
nas_name=[]
nas_num=[]
asn_rpki=[]
asn_ro=[]
prefixx=[]
prefixx2=[]
prefixxx=[]
z=0
update_asn=[]
update_asn_num=[]
#Boucle servant à déterminer le nom des ASN
for j in range(0, len(asn_url)):
    curl="".join(asn_name+str(asn_url.iloc[j]['num']))
    #print(curl)
    resp=urllib.request.urlopen(curl)
    data=json.loads(resp.read().decode())
    asn.append(str(data["data"]["holder"]))
asn_url['AS_NAME']=asn

prefixxx=pd.DataFrame()
for k in range(0, len(asn_url)):
    curl2="".join(curl_ressources+str(asn_url.iloc[k]['num']))
    resp2=urllib.request.urlopen(curl2)
    data2=json.loads(resp2.read().decode())
    #print(len(data2["data"]["prefixes"]))
    prefix=pd.DataFrame.from_dict(data2["data"]["prefixes"], orient='columns')
    
    for i in range(0, len(data2["data"]["prefixes"])):
        prefixx.append(str(prefix.iloc[i]["prefix"]))
        prefixx2.append(str(prefix.iloc[i]["irr_sources"]))
        update_asn.append(str(asn_url.iloc[k]['AS_NAME']))
        update_asn_num.append(str(asn_url.iloc[k]['num']))
prefixxx['ASN']=update_asn_num
prefixxx['AS']=update_asn
prefixxx['prefix']=prefixx
prefixxx['IRR']=prefixx2
print(prefixxx)


ro="https://stat.ripe.net/data/routing-status/data.json?resource="
ro2="%2F"
for i in range(0,len(prefixxx)):
    curl2="".join(rpki+str(prefixxx.iloc[i]['ASN'])+rpki1+str(prefixxx.iloc[i]['prefix']))
    curl3="".join(ro+str(prefixxx.iloc[i]['prefix']))
    res=urllib.request.urlopen(curl2)
    res1=urllib.request.urlopen(curl3)
    data2=json.loads(res.read().decode())
    data3=json.loads(res1.read().decode())
    #print(data2["data"]["validating_roas"]["0"]["origin"])
    check_ro=data3["data"]["first_seen"]
    check_rpki=data2["data"]["status"]
    #print(check_rpki)
    if check_rpki =='valid':
        asn_rpki.append("yes")
    else:
        asn_rpki.append("no")
    if check_ro:
        asn_ro.append(data3["data"]["first_seen"]["origin"])
    else:
        asn_ro.append("no")
prefixxx['RPKI']=asn_rpki
prefixxx['ASN_OWNER']=asn_ro
print("I am here now")
writer = ExcelWriter('manrs_new1.xlsx')
prefixxx.to_excel(writer,'prefix')
asn_url.to_excel(writer,'ASN')
writer.save()

