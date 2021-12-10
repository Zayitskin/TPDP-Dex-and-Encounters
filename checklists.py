
import json, os.path

def createEmptyChecklist() -> None:

    if os.path.exists("checklist.json"):
        print("checklist.json already exists.")
        return
    if not os.path.exists("mons.json"):
        print("Puppet information not found. Running scraper.py.")
        from scraper import scrapeSoD
        scrapeSoD()

    with open("mons.json") as fm:
        with open("checklist.json", "w") as fc:

            cl: dict = {}
            mons: list = json.load(fm)
            for mon in mons:
                if "Normal" in mon["name"]:
                    cl[mon["name"]] = False

            json.dump(cl, fc)

if __name__ == "__main__":

    raise SystemExit(createEmptyChecklist())
            
