import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, bin_path=""):
        option = webdriver.ChromeOptions()
        option.binary_location = bin_path
        ua = 'cat'
        option.add_argument('--user-agent=%s' % ua)
        option.add_argument("--disable-blink-features=AutomationControlled")
        # TODO: ENSURE CHROMEDRIVER IS IN PROJECT DIRECTORY
        self.browser = webdriver.Chrome(
            executable_path="./chromedriver.exe", options=option
        )
        # self.get_leaderboard_urls()

    def get_leaderboard_urls(self):
        self.browser.get('https://axie.zone/leaderboard')

        table = self.browser.find_element(by=By.XPATH, value='/html/body/div[1]/main/div/div[4]/div/table')

        elements = table.find_elements_by_tag_name('tr')
        # remove header from table
        elements.pop(0)
        links = table.find_elements_by_tag_name('a')
        print(len(elements))
        print(len(links))
        top100players = []
        for index, element in enumerate(elements):
            top100players.append({"player": element.text,
                                  "url": links[index].get_attribute('href'),
                                  "rank": index + 1,
                                  "mmr": element.text[-9:][:4]
                                  })
        return top100players

    # TODO: remove url after deploy to not produce fake positives
    def get_axies_from_profile(self, url):
        self.browser.get(url=url)
        axies = []
        # container contains class search_result_wrapper that contain purity_parts and purity_part that has title we need
        # need to implicitly wait to ensure all data is present, API delay
        # self.browser.implicitly_wait(time_to_wait=10)
        loading = True
        while loading:
            if 'Breed count:' in self.browser.page_source:
                loading = False
                print('Loaded.')

        most_used_team = self.browser.find_element(by=By.ID, value='most_used_team_container')

        most_used_team_wrappers = most_used_team.find_elements(by=By.CLASS_NAME, value='search_result_wrapper')

        for wrapper in most_used_team_wrappers:
            axie_class = wrapper.find_element(by=By.TAG_NAME, value="a").get_attribute('class')
            axie_class = axie_class.replace('search_result ', '').replace(' ', '').capitalize()
            print("Axie Class: " + axie_class)
            axie_info = wrapper.text.splitlines()
            axie = {
                "name": axie_info[0],
                "breed_count": axie_info[1].replace('Breed count: ', ''),
                "axiezone_metascore": axie_info[3].replace('Meta Score:', ''),
                "is_on_sale": axie_info[5],
                "type": 'most_used',
                "class": axie_class
            }
            purity_parts = wrapper.find_elements(by=By.CLASS_NAME, value='purity_part')

            for part in purity_parts:
                part = part.find_element_by_css_selector("*")
                key, value = self.__axie_parts_to_json(part=part.get_attribute('title'))
                axie[key] = value

            axies.append(axie)
        return axies

    def find_axie_by_parts(self, axie_query):
        parts = []
        valid_parts = ["ears", "back", "mouth", "eyes", "horn", "tail"]
        for key in axie_query:
            if key in valid_parts:
                build_part = key + "-" + axie_query[key]["ability"].replace(' ', '-').lower()
                if build_part[-1] == "-":
                    build_part = build_part[:-1]
                parts.append(build_part)
        print(parts)
        return self.__query_axie_API(parts=parts, axie_class=[axie_query["class"]])

    def __query_axie_API(self, parts=[], axie_class=None):
        body = {
            "operationName": "GetAxieBriefList",
            "variables": {
                "from": 0,
                "size": 24,
                "sort": "PriceAsc",
                "auctionType": "Sale",
                "owner": None,
                "criteria": {
                    "region": None,
                    "parts": parts,  # this will contain parts provided by the main function
                    "bodyShapes": None,
                    "classes": axie_class,
                    "stages": None,
                    "numMystic": None,
                    "pureness": None,
                    "title": None,
                    "breedable": None,
                    "breedCount": None,
                    "hp": [],
                    "skill": [],
                    "speed": [],
                    "morale": []
                }
            },
            "query": "query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
        }
        r = None
        try:
            r = requests.post(url='https://graphql-gateway.axieinfinity.com/graphql', headers={
                "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50SWQiOjc2NzI1NzUsImFjdGl2YXRlZCI6dHJ1ZSwicm9uaW5BZGRyZXNzIjoiMHgzM2I5NzhkNTc2Y2I3OTM1Y2ZjNTVmZjY4NjIzZjI2N2I2ZDJiMWFiIiwiZXRoQWRkcmVzcyI6bnVsbCwiaWF0IjoxNjM1MDA2NTI2LCJleHAiOjE2MzU2MTEzMjYsImlzcyI6IkF4aWVJbmZpbml0eSJ9.OpgBnGUGVWi29ytmqpPD-W4H1VhHZkRPAXq62sJlP6o"},
                              json=body)
            print(r.json())
        except Exception as e:
            pass
        try:
            if r.json()["data"]["axies"]["total"] > 0:
                print('Found matching axie: ', r.json()["data"]["axies"]["results"][0]["id"])
            return r.json()["data"]["axies"]
        except Exception as e:
            return {"error": e}

    def __axie_parts_to_json(self, part):
        key = None
        value = None
        if 'Eyes:' in part:
            key = 'eyes'
            value = part.replace('Eyes: ', '').split('[')
        elif 'Ears:' in part:
            key = 'ears'
            value = part.replace('Ears: ', '').split('[')
        elif 'Back:' in part:
            key = 'back'
            value = part.replace('Back: ', '').split('[')
        elif 'Mouth:' in part:
            key = 'mouth'
            value = part.replace('Mouth: ', '').split('[')
        elif 'Horn:' in part:
            key = 'horn'
            value = part.replace('Horn: ', '').split('[')
        elif 'Tail:' in part:
            key = 'tail'
            value = part.replace('Tail: ', '').split('[')
        else:
            key = 'error',
            value = 'Data received: ' + str(part)

        if value is not None:
            value = {"ability": value[0], "type": value[1].replace(']', '')}

        return key, value
