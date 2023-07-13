import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

conn = sqlite3.connect('players.db')

headers = {"Connection":"keep-alive", "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
comps = requests.get("https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1", headers=headers).text
soup = BeautifulSoup(comps, 'html.parser')
elems = soup.find_all("td", {'class': 'hauptlink no-border-links'})
links = []
names = []
for club in elems:
    link = "https://www.transfermarkt.com" + club.a['href']
    links.append(link.replace("startseite", "alumni").replace("saison_id/2023", ""))
    name = club.a['title'].replace("&", 'and').replace(".", "").replace("-", "")
    name = name.replace("1", "One")
    names.append(name.replace(" ", ""))
names.remove("ManchesterCity")
links.remove("https://www.transfermarkt.com/manchester-city/alumni/verein/281/")
print(names, links)
for y in range(len(links)):
    r = requests.get(links[y], headers=headers).text
    r = r.encode('UTF-8')
    content = BeautifulSoup(r, 'html.parser')

    last_page_link = content.find("li", {"class": "tm-pagination__list-item--icon-last-page"})
    last_page = int(last_page_link.a['href'].split('/')[-1])
    print(last_page)
    # players = []
    id = 1
    for i in range(1, last_page + 1):
        page_link = links[y] + "page/" + str(i)
        print(page_link)
        player_page = requests.get(page_link, headers=headers).text
        player_page = player_page.encode('UTF-8')
        soup = BeautifulSoup(player_page, 'html.parser')
        a_z = soup.find_all("td", {"class" : "hauptlink"})
        a_z = list(a_z)
        for i in range(len(a_z)):
            # players.append(a_z[i].text.split('\n')[1])
            player_name = a_z[i].text.split('\n')[1]
            conn.execute(f'INSERT INTO {names[y]} (ID, NAME) VALUES ({id}, "{player_name}");')
            # print(f'Player {player_name}has been added with ID = {id}')
            id += 1
    # print(players)

# df = pd.DataFrame(players)
# df.to_csv('players.csv')
conn.commit()
conn.close()