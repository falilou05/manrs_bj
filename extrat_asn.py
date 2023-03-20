import datetime as dt
import json
import pandas as pd
import requests





def getdata(url):
    """Get data from AFRINIC file for Benin (BJ) and returns a dataframe."""
    headers = ['Registry', 'Country Code', 'Type', 'Start', 'Value', 'Date', 'Status', 'Extensions']
    c = pd.read_csv(url, delimiter='|', comment='#', names=headers, dtype=str, keep_default_na=False, na_values=[''], encoding='utf-8')[4:]
    bj_data = c[(c['Country Code'] == 'BJ') & (c['Type'] == 'asn')]
    return bj_data

def getdata2(url):
    """Get data from AFRINIC file for Benin (BJ) and returns a dataframe."""
    headers = ['Registry', 'Country Code', 'Type', 'Start', 'Value', 'Date', 'Status', 'Extensions']
    c = pd.read_csv(url, delimiter='|', comment='#', names=headers, dtype=str, keep_default_na=False, na_values=[''], encoding='utf-8')[4:]
    bj_data = c[(c['Country Code'] == 'BJ') & ((c['Type'] == 'ipv4') | (c['Type'] == 'ipv6'))]
    return bj_data
def generate_csv(df, filename):
    df.to_csv(filename, sep='|', index=False)



if __name__ == "__main__":
    url = 'http://ftp.afrinic.net/stats/afrinic/delegated-afrinic-extended-latest'
    dataBJ = getdata(url)
    df = pd.DataFrame(dataBJ)
    df = df.rename(columns={'Registry': 'Organisation', 
                            'Country Code': 'CC', 
                            'Type': 'type',
                            'Start': 'num',
                            'Value': 1,
                            'Date': 'unknow',
                            'Status': 'status',
                            'Extensions': 'identification',})
    dataBJ2 = getdata2(url)
    df2 = pd.DataFrame(dataBJ2)
    df2 = df2.rename(columns={'Registry': 'organisation', 
                            'Country Code': 'CC', 
                            'Type': 'version',
                            'Start': 'IP',
                            'Value': 'host_nb',
                            'Date': 'date',
                            'Status': 'status',
                            'Extensions': 'identification',})
    generate_csv(df, 'asn_bj.csv')
    generate_csv(df2, 'prefix_bj.csv')