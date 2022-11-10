from typing import List
import numpy as np
import pandas as pd
import requests
import bs4 as bs
import argparse


# call program and parse username
parser = argparse.ArgumentParser()
parser.add_argument("username", help="GitHub username")
parser.add_argument("output", help="Output file name")
args = parser.parse_args()
username = args.username


url = 'https://github.com/{}?tab=repositories'.format(username)
print(url)

soup = bs.BeautifulSoup(requests.get(url).text, 'lxml')
list = soup.find("div", {"id": "user-repositories-list"})
repos : List[bs.BeautifulSoup]= list.find_all("li")

rows = []
for r in repos:
    name = r.find("a").text.strip()

    langEle = r.find("span", {"itemprop": "programmingLanguage"})
    language = langEle.text.strip() if langEle else ""
    
    descEle = r.find("p", {"itemprop": "description"})
    description = descEle.text.strip() if descEle else ""
    
    starEle = r.find("a", {"class" : "Link--muted mr-3"})
    stars = int(starEle.text.strip().replace(",","")) if starEle else 0
        
    rows.append([name, description, language, stars])

df = pd.DataFrame(rows, columns=['name', 'description', 'language', 'stars'])
df = df.sort_values(by=['stars'], ascending=False)
if args.output:
    df.to_csv(args.output, index=False)
else: 
    df.to_csv(f'{username}_repos.csv', index=False)
print(df)