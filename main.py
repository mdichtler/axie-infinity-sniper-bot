# Build Scraper for ____
import argparse

# import functionality from within the project
from scraper import Scraper


# user can specify chrome binary using --path parameter if not in default location
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("--path", type=str, default="C:\Program Files\Google\Chrome\Application\chrome.exe")

args = parser.parse_args()

# parse parameters from run command
bin_path = args.path

# initiate scraper
scraper = Scraper(url="https://exchange.pancakeswap.finance/#/swap", bin_path=bin_path)
