#! python3

import sys
import requests
from bs4 import BeautifulSoup
# import csv
# import pandas
from urllib.request import urlretrieve
from urllib.error import HTTPError
import os
from pathlib import Path


def patent_google_func(patent, UserPath=os.getcwd()):
    # Looks up a patent on patents.google.com via its patent number
    # yields: title (string), claims (html file), description (html file), images
    if patent == '':
        print("No patent entered, stop.")
        exit()
    else:
        try:
            os.makedirs(os.path.join(UserPath, patent))
            print("Directory " + patent + " created.")
            path = os.path.join(UserPath , patent)
            print(path)
        except FileExistsError:
            print("Directory " + patent + " already exists, stop.")
            exit()
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
        with open(os.path.join(path, patent + "-claims.html"), "w", encoding=enc) as html_file:
            html_file.write(str(claims))
        #
        try:
            PicturesAll = PatentSoup.find_all("li",{"itemprop":"images"})
            PicturesURLs = [picture.find("meta",{"itemprop":"full"}).get("content") for picture in PicturesAll]
            for picture in PicturesURLs:
                urlretrieve(picture, os.path.join(path, picture.split('/')[-1]))
        except FileNotFoundError as err:
            print(err)
        except HTTPError as err:
            print(err)
        #
        description = PatentSoup.find("section",{"itemprop":"description"})
        with open(os.path.join(path, patent + "-description.html"), "w", encoding=enc) as html_file:
            html_file.write(str(description))
        print("Done.")




if __name__ == '__main__':
    patent = input("Enter patent number: ").strip()
    PathBool = input("Do you want to enter your own path? (y/n): ").strip()
    if PathBool == "y":
        print("Correct formatting (current folder, default path):" + os.getcwd())
        UserPathRaw = input("Enter path: ").strip()
        if os.path.isdir(UserPathRaw) == False:
            print("This is not a valid path: " + UserPathRaw)
            exit()
        else:
            UserPath = UserPathRaw
            patent_google_func(patent, UserPath)
    elif not PathBool == "n":
        print("\"" + PathBool + "\" is not a valid option.")
        exit()
    else:
        patent_google_func(patent)
