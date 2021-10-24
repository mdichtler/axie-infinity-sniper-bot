# Build Scraper for ____
import argparse

# import functionality from within the project
from scraper import Scraper
from database import Database

# user can specify chrome binary using --path parameter if not in default location
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("--path", type=str, default="C:\Program Files\Google\Chrome\Application\chrome.exe")

args = parser.parse_args()

# parse parameters from run command
bin_path = args.path

# initiate db
db = Database()


# initiate scraper
scraper = Scraper(bin_path=bin_path)
# print(scraper.get_leaderboard_urls())



# get leaderboard including urls to their axie.zone profiles that have info on their axies
leaderboard_data = scraper.get_leaderboard_urls()
# now lets scrape this for axies
# TODO: uncomment leaderboard data

for player in leaderboard_data:
    player["axies"] = scraper.get_axies_from_profile(url=player["url"])
    print(player)




# ONLY PUSH FINAL DATA
db.push_leaderboard_to_db(data=leaderboard_data)


