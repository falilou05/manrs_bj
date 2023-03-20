#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:57:13 2020

@author: adefemi
"""


import pandas as pd
import urllib.request, json
import math
import re, requests 
from pandas import ExcelWriter

#Création d'une fonction "remplacer"
def remplacer(c1,c2,ch):
    n=len(ch)
    i=0
    while i<n:
        if c1==ch[i]:
            ch=ch[:i]+c2+ch[i+1:]
            n-=1
        i+=1
    return ch
#lecture du contenu du fichier asn_bj.txt et conversion en DF dans la variable asn_url
asn_url = pd.read_csv('asn_bj.csv',sep = "|")
#lecture du contenu du fichier prefix_bj.txt et conversion en DF dans la variable prefix
prefix = pd.read_csv('prefix_bj.csv',sep = "|")
#Création de la variable asn_name contenant l'url servant à l'identification du nom d'un ASN
asn_name="https://stat.ripe.net/data/as-overview/data.json?resource=AS"
#Création des variables rpki et rpki1 asn_name contenant l'url servant à l'identification d'un roa pour un préfixe particulier
rpki="https://stat.ripe.net/data/rpki-validation/data.json?resource="
rpki1="&prefix="
#création d'une variable string slash
slash="/"
#création d'une variable ASN servant à stocker tous les noms d'ASN
asn=[]
#création d'une variable cidr servant à stocker  la taille de tous les préfixes
cidr=[]
#création d'une variable nas_name servant à stocker tous les noms d'ASN en fonction de leur préfixes
nas_name=[]
#création d'une variable nas_num servant à stocker tous les numéros d'ASN en fonction de leur préfixes
nas_num=[]
#création d'une variable asn_rpki servant à valider l'existance d'un ROA
asn_rpki=[]
#création d'une variable asn_ro servant à valider l'existance d'un RO
asn_ro=[]
#Creation de z
z=0
#boucle servant au calcul du la taille des prefix
for i in range(0,len(prefix)):
    indice=math.log(int(prefix.iloc[i]['host_nb']),2)
    indice=32-int(indice)
    cidr.append(indice)
prefix['indice']=cidr

#Boucle servant à déterminer le nom des ASN
##Boucle J parcourant la liste de AS
for j in range(0, len(asn_url)):
    ###Composition de l'URL exemple:"https://stat.ripe.net/data/as-overview/data.json?resource=AS"+le numero D'AS
    curl="".join(asn_name+str(asn_url.iloc[j]['num']))
    ###Recupération du résultat dans la variable resp
    resp=urllib.request.urlopen(curl)
    ###le resultat étant en json, stockage de ce résultat dans la variable data
    data=json.loads(resp.read().decode())
    ###Récupération du nom d'ASN dans la variable asn
    asn.append(str(data["data"]["holder"]))
#Insertion d'une nouvelle colonne AS_NAME contenant le nom des ASN
asn_url['AS_NAME']=asn
print("Fin de la détermination du nom des ASN")
#creation d'une nouvelle liste de AS "new_asn" sans doublon
new_asn=asn_url.drop_duplicates(subset=['identification'])

#Boucle servant à classifier les préfixes par ASN
for k in range(0, len(new_asn)):
    for i in range(0,len(prefix)):
        if str(prefix.iloc[i]['identification']) == str(new_asn.iloc[k]['identification']):
            nas_name.append(str(new_asn.iloc[k]['AS_NAME']))
            nas_num.append(str(new_asn.iloc[k]['num']))
prefix['ASN_NAME']=nas_name
prefix['ASN_NB']=nas_num 


#boucle servant à déterminer les RO & ROA des AS
##Création des variable ro ro2 contenant l'url servant à l'identification du RO d'un préfixe
ro="https://stat.ripe.net/data/routing-status/data.json?resource="
ro2="%2F"
##Boucle i parcourant la liste des préfixes
for i in range(0,len(prefix)):
    ###Composition de l'URL exemple:"https://stat.ripe.net/data/rpki-validation/data.json?resource="+numéro de l'AS+la taile du préfixe
    curl2="".join(rpki+str(prefix.iloc[i]['ASN_NB'])+rpki1+str(prefix.iloc[i]['IP'])+slash+str(prefix.iloc[i]['indice']))
    ###Composition de l'URL exemple:"https://stat.ripe.net/data/routing-status/data.json?resource="+@ip+taille du préfixe
    curl3="".join(ro+str(prefix.iloc[i]['IP'])+ro2+str(prefix.iloc[i]['indice']))
    ###Recupération du résultat dans la variable res
    res=urllib.request.urlopen(curl2)
    ###Recupération du résultat dans la variable res1
    res1=urllib.request.urlopen(curl3)
    ###le resultat étant en json, stockage de ce résultat dans la variable data2
    data2=json.loads(res.read().decode())
    ###le resultat étant en json, stockage de ce résultat dans la variable data3
    data3=json.loads(res1.read().decode())
    ###check_ro recoit le attestant de l'existence d'un RO
    check_ro=data3["data"]["origins"]
    ###check_rpki recoit le attestant de l'existence d'un ROA
    check_rpki=data2["data"]["status"]
    ###si check_rpki non NULL: Alors
    if check_rpki =='valid':
        ####la variable asn_rpki prend la valeur yes
        asn_rpki.append("yes")
    else:
        ####la variable asn_rpki prend la valeur no
        asn_rpki.append("no")
    ###si check_ro non NULL: Alors
    if check_ro:
        ####la variable asn_ro prend la valeur yes
        asn_ro.append("yes")
    else:
        ####la variable asn_ro prend la valeur no
        asn_ro.append("no")
#Ajout des colonnes RPKI & RO dans la liste des prefixes
prefix['RPKI']=asn_rpki
prefix['RO']=asn_ro
#afficher la nouvelle liste
print(prefix)
#creer un fichier EXCEL manrs.xlsx
writer = ExcelWriter('manrs.xlsx')
#creer une feuille ASN contenant la liste des ASN
asn_url.to_excel(writer,'ASN')
#creer une feuille prefix contenant la liste des préfix
prefix.to_excel(writer,'prefix')
writer.save()

