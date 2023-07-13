import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('players.db')
headers = {"Connection":"keep-alive", "User-Agent":"Mozilla/5.0"}
comps = requests.get("https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1", headers=headers).content
soup = BeautifulSoup(comps, "html.parser")

elems = soup.find_all("td", {'class': 'hauptlink no-border-links'})
links = []
names = []
for club in elems:
    link = "https://www.transfermarkt.com" + club.a['href']
    links.append(link.replace("startseite", "alumni").replace("saison_id/2023", ""))
    name = club.a['title'].replace("&", 'and').replace(".", "").replace("-", "")
    name = name.replace("1", "One")
    names.append(name.replace(" ", ""))

print(links)
    
conn.close()