# manrs_bj 
manrs_bj.py est un script python(panda) Script python(Panda), vérifiant automatiquement l'existence
des RO(Route Object) et ROA(Route Origine Authorization) pour les Systèmes Autonomes(AS) du Bénin.

#Description
Nous avons dans un premier extrait la liste les numeros d'AS ainsi que les Préfixe des systèmes autonomes, depuis le dépot FTP de afrinic(http://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest) 
Ces listes sont disponibles dans asn_bj.txt(liste des ASN) et prefix_bj.txt(liste des préfixes).

A partir de ces différentes listes, nous avons déduit les préfixes ayant des RO existants dans un base IRR(grâce au widget "routing-status" de RIPE NCC)
Nous avons également déduit les préfixes ayant des ROA existants dans un base (grâce au widget "rpki-validation" de RIPE NCC).

#Execution du script:
spider de anaconda
