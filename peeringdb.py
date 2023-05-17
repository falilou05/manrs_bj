# -*- coding: utf-8 -*-
import requests
import csv

# Liste des ASN à vérifier
asns = []

# URL de l'API PeeringDB
url = "https://www.peeringdb.com/api/net"

with open('asn_bj.csv', newline='') as csvfile:
    asn_reader = csv.reader(csvfile, delimiter='|')
    asns = [row[3] for row in asn_reader if row[2] == 'asn']

# Initialisation du fichier CSV
with open('asns.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ASN", "Present in PeeringDB"])

    # Vérification de chaque ASN
    for asn in asns:
        query = f"?asn={asn}"
        response = requests.get(url + query)
        present_in_db = "Yes" if response.json()["data"] else "No"
        writer.writerow([asn, present_in_db])