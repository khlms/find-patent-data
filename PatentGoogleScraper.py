#! python3

import sys
import requests
from bs4 import BeautifulSoup
# import csv
# import pandas
from urllib.request import urlretrieve
from urllib.error import HTTPError
from pathlib import Path
import cv2 #convert png to jpg for gui

##TODO include pdf option


def PatentGoogleScrape(patent, UserPath=Path.cwd() / "patents"):
    '''Looks up a patent on patents.google.com via its patent number'''
    '''yields: claims (html file), description (html file), images (png and jpg)'''
    PathToPatent = UserPath / patent
    if patent == '':
        print("No patent entered, stop.")
        return
    elif PathToPatent.exists():
        print("Directory " + patent + " already exists, stop download.")
        return
    else:
        urlOrig = 'https://patents.google.com/patent/' + patent
        print("Looking up " + urlOrig)
        PatentPageOrig = requests.get(urlOrig)
        PatentSoupOrig = BeautifulSoup(PatentPageOrig.content, 'lxml')

        '''get title of html file'''
        titlehtml = PatentSoupOrig.find("title").contents
        if "Error 404 (Not Found)" in titlehtml[0]:
            print("Patent " + patent + " not found.")
            return

        '''get original language of patent'''
        LangOrig = PatentSoupOrig.find("section",{"itemprop":"application"}).find("section",{"itemprop":"metadata"}).find("span",{"itemprop":"primaryLanguage"}).contents[0]
        if LangOrig == "de":
            PatentPage = PatentPageOrig
            PatentSoup = PatentSoupOrig
        else:
            url = 'https://patents.google.com/patent/' + patent + '/en'
            print("Looking up " + url)
            PatentPage = requests.get(url)
            PatentSoup = BeautifulSoup(PatentPage.content, 'lxml')

        PathToPatent.mkdir(parents=True)
        print("Directory " + patent + " created.")
        print(PathToPatent)

        EncFind = PatentSoup.find_all("meta") # .get("charset")
        for i in EncFind:
            if i.get("charset") != None:
                enc = i.get("charset")
                break
        ## get title
        # title = PatentSoup.find("meta", {"name":"DC.title"}).get("content")
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
        #
        '''get all claims'''
        claims = PatentSoup.find("section",{"itemprop":"claims"})
        with open(PathToPatent / str(patent + "-claims.html"), "w", encoding=enc) as html_file:
            html_file.write(str(claims))

        try:
            PicturesAll = PatentSoup.find_all("li",{"itemprop":"images"})
            PicturesURLs = [picture.find("meta",{"itemprop":"full"}).get("content") for picture in PicturesAll]
            for picture in PicturesURLs:
                PathToPicture = PathToPatent / picture.split('/')[-1]
                urlretrieve(picture, PathToPicture)
                '''convert png to jpg because this somehow looks way better'''
                PicturePNG = cv2.imread(str(PathToPicture))
                cv2.imwrite(str(PathToPicture)[:-3] + 'jpg', PicturePNG)
        except FileNotFoundError as err:
            print(err)
        except HTTPError as err:
            print(err)

        description = PatentSoup.find("section",{"itemprop":"description"})
        with open(PathToPatent / str(patent + "-description.html"), "w", encoding=enc) as html_file:
            html_file.write(str(description))

        print("Done.")




if __name__ == '__main__':
    patent = input("Enter patent number: ").strip()
    PathBool = input("Do you want to enter your own path? (y/n): ").strip()
    if PathBool == "y":
        print("Correct formatting (current folder, i.e. default path):" + str(Path.cwd()))
        UserPath = input("Enter path: ").strip()
        if path.is_dir(UserPath) == False:
            print("This is not a valid path: " + UserPath)
            exit()
        else:
            PatentGoogleScrape(patent, UserPath)
    elif not PathBool == "n":
        print("\"" + PathBool + "\" is not a valid option.")
        exit()
    else:
        PatentGoogleScrape(patent)
