#! python3

import sys
import requests
from bs4 import BeautifulSoup
# import csv
import pandas



patent = input("Enter the patent number: ")

if patent == '':
    print("no patent entered")
    exit()
else:
    url = 'https://patents.google.com/patent/' + patent
    print("Lookin up " + url)
    try:
        PatentPage = requests.get(url)
        PatentSoup = BeautifulSoup(PatentPage.content, 'lxml')
    except:
        print("Patent" + patent + " not found.")
        exit()
    title = PatentSoup.find("meta", {"name":"DC.title"}).get("content")
    ## alternative:
    # title = PatentSoup.find("span", {"itemprop": "title"}).get_text(strip=True)
    claims = [PatentSoup.find("div", {"class":"claim", "num":"00001"}).get_text(strip=True)] + [claim.get_text(strip=True) for claim in PatentSoup.find_all("div", {"class": "claim-dependent"})]
    df = pandas.DataFrame(claims)
    df.to_csv("patents.csv", index=False, header=False)
    print(title)
    print(claims)
