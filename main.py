# Build Scraper for ____
import argparse

# import functionality from within the project
import json

from scraper import Scraper
from database import Database

# user can specify chrome binary using --path parameter if not in default location
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("--path", type=str, default=f"C:\Program Files\Google\Chrome\Application\chrome.exe")

args = parser.parse_args()

# parse parameters from run command
bin_path = args.path

# initiate db
db = Database()

# initiate scraper
scraper = Scraper(bin_path=bin_path)

# get leaderboard including urls to their axie.zone profiles that have info on their axies
leaderboard_data = scraper.get_leaderboard_urls()
# PUSH leaderboard data
db.push_leaderboard_to_db(data=leaderboard_data)
# now lets scrape this for axies and get their prices from the API if the exist
for player in leaderboard_data:
    player["axies"] = scraper.get_axies_from_profile(url=player["url"])
    for axie in player["axies"]:
        axie["market_data"] = scraper.find_axie_by_parts(axie_query=axie)
        try:
            for on_sale_axie in axie["market_data"]["results"]:
                on_sale_axie["matching_player"] = player["player"]
                on_sale_axie["player_rank"] = player["rank"]
                on_sale_axie["player_mmr"] = player["mmr"]
                on_sale_axie["player_url"] = player["url"]
                on_sale_axie["matching_axie_name"] = axie["name"]
                on_sale_axie["axie_zone_score"] = axie["axiezone_metascore"]
                db.push_on_sale_axies(axie=on_sale_axie)
        except Exception as e:
            print(e)
            pass
