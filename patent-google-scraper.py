#! python3

import sys
import requests
from bs4 import BeautifulSoup
# import csv
# import pandas
from urllib.request import urlretrieve
from urllib.error import HTTPError


patent = input("Enter the patent number: ").strip()

if patent == '':
    print("no patent entered")
    exit()
else:
    url = 'https://patents.google.com/patent/' + patent
    print("Looking up " + url)
    try:
        PatentPage = requests.get(url)
        PatentSoup = BeautifulSoup(PatentPage.content, 'lxml')
    except:
        print("Patent" + patent + " not found.")
        exit()
    EncFind = PatentSoup.find_all("meta") # .get("charset")
    for i in EncFind:
        if i.get("charset") != None:
            enc = i.get("charset")
            break
    title = PatentSoup.find("meta", {"name":"DC.title"}).get("content")
    ## alternative:
    # title = PatentSoup.find("span", {"itemprop": "title"}).get_text(strip=True)
    #
    ## get list of claims
    # claims = [PatentSoup.find("div", {"class":"claim", "num":"00001"})] + [claim for claim in PatentSoup.find_all("div", {"class": "claim-dependent"})]
    # claims = [PatentSoup.find("div", {"class":"claim", "num":"00001"})] + PatentSoup.find_all("div", {"class": "claim-dependent"})
    #
    ## csv-output using csv:
    # str_claims = ','.join(claim.get_text(strip=False).strip() for claim in claims)
    # print(str_claims)
    # with open ('patents.csv', 'w') as csvfile:
        # writer = csv.writer(csvfile, delimiter=",")
        # writer.writerow(str_claims)
    #
    ## csv-output using pandas
    # ClaimsCSV = [claim.get_text(strip=False).strip() for claim in claims]
    # df = pandas.DataFrame(ClaimsCSV)
    # df.to_csv("patents.csv", index=False, header=False)
    # get all claims
    claims = PatentSoup.find("section",{"itemprop":"claims"})
    with open(str(patent) + "-claims.html", "w", encoding=enc) as html_file:
        html_file.write(str(claims))
    #
    try:
        PicturesAll = PatentSoup.find_all("li",{"itemprop":"images"})
        PicturesURLs = [picture.find("meta",{"itemprop":"full"}).get("content") for picture in PicturesAll]
        for picture in PicturesURLs:
            urlretrieve(picture, picture.split('/')[-1])
    except FileNotFoundError as err:
        print(err)
    except HTTPError as err:
        print(err)
    #
    description = PatentSoup.find("section",{"itemprop":"description"})
    with open(str(patent) + "-description.html", "w", encoding=enc) as html_file:
        html_file.write(str(description))
