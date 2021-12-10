
import requests
from bs4 import BeautifulSoup as BS
import json
from collections import defaultdict as ddict

def scrapeSoD() -> None:

    rows: list = []

    #Base game mons
    print("Getting base game puppet list")
    with requests.get("http://en.tpdpwiki.net/wiki/Puppetdex", timeout = 1) as page:
        page.encoding = "utf-8"
        soup: BS = BS(page.text, "html.parser")

        res = soup.find("table", {"class": "wikitable sortable"})
        for row in res.tbody.find_all("tr"):
            eles: list = []
            for ele in row.find_all("td"):
                eles.append(ele)
            if len(eles) == 0:
                continue
            rows.append({
                "id": eles[0].text.strip(),
                "name": eles[1].text.strip(),
                "type1": eles[2].text.strip(),
                "type2": eles[3].text.strip(),
                "hp": eles[4].text.strip(),
                "foatk": eles[5].text.strip(),
                "fodef": eles[6].text.strip(),
                "spatk": eles[7].text.strip(),
                "spdef": eles[8].text.strip(),
                "spd": eles[9].text.strip(),
                "bst": eles[10].text.strip(),
                "cost": eles[11].text.strip(),
                "abl1": eles[12].text.strip(),
                "abl2": eles[13].text.strip(),
                })

    #Modded mons
    print("Getting extended mod puppet list")
    with requests.get("http://en.tpdpwiki.net/wiki/Mod:Mod_Puppetdex", timeout = 1) as page:
        page.encoding = "utf-8"
        soup: BS = BS(page.text, "html.parser")

        res = soup.find("table", {"class": "wikitable sortable"})
        names: list = res.find_all("th", {"rowspan": "4"})
        for row in res.tbody.find_all("tr"):
            eles: list = []
            for ele in row.find_all("td"):
                eles.append(ele)
            if len(eles) == 0:
                continue
            rows.append({
                "id": "m" + eles[0].text.strip(),
                "name": eles[1].text.strip() + " " + names[int(eles[0].text.strip()) // 4].text.strip(),
                "type1": eles[2].text.strip(),
                "type2": eles[3].text.strip(),
                "hp": eles[4].text.strip(),
                "foatk": eles[5].text.strip(),
                "fodef": eles[6].text.strip(),
                "spatk": eles[7].text.strip(),
                "spdef": eles[8].text.strip(),
                "spd": eles[9].text.strip(),
                "bst": eles[10].text.strip(),
                "cost": eles[11].text.strip(),
                "abl1": eles[12].text.strip(),
                "abl2": eles[13].text.strip(),
                "encs": [],
                })


    encs: ddict = ddict(list)

    #Encounters (from the list of puppets by location, no modded puppets)
    print("Getting encounter data for non-modded puppets")
    with requests.get("http://en.tpdpwiki.net/wiki/List_of_puppets_by_location#SoD_1.103", timeout = 1) as page:
        page.encoding = "utf-8"
        soup: BS = BS(page.text, "html.parser")

        areas: list = soup.find_all("td", {"style": "vertical-align: top;"})
        for area in areas:
            name: str = area.table.caption.text.strip()
            for index, tr in enumerate(area.table.tbody.find_all("tr")):
                if index == 0:
                    continue
                mon, rate = tr.find_all("td")
                if "Renko" in mon.text:
                    encs["Normal Renko"].append((name, rate.text.strip()))
                elif "Maribel" in mon.text:
                    encs["Normal Maribel"].append((name, rate.text.strip()))
                else:
                    encs[mon.text.strip()].append((name, rate.text.strip()))

            if name == "Fantasy World-Blue Grass (level 69~71)":
                break

    #Encounters (modded puppets)
    print("Getting encounter data for modded puppets (this will take a while)")
    for mon in rows:
        if not mon["id"].startswith("m"):
            continue
        if not mon["name"].startswith("Normal"):
            continue
        name: str = mon["name"].split(" ")[1]
        with requests.get("http://en.tpdpwiki.net/wiki/Mod:Shard_of_Dreams_-_Extended_-/" + name, timeout = 1) as page:
            page.encoding = "utf-8"
            soup: BS = BS(page.text, "html.parser")

            locs = soup.find_all("table", {"class": "wikitable"})[4].find_all("tr")[1:]
            for loc in locs:
                place, lvl, rate = loc.find_all("td")
                encs[mon["name"]].append((place.text.strip() + " (" + lvl.text.strip() + ")", rate.text.strip()))
            
            

    for mon in rows:
            mon["encs"] = encs[mon["name"]]
            
    with open("mons.json", "w") as jf:
        json.dump(rows, jf)
            

if __name__ == "__main__":

    raise SystemExit(scrapeSoD())
