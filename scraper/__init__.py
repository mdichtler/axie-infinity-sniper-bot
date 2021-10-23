

from selenium import webdriver


from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, bin_path=""):
        option = webdriver.ChromeOptions()
        option.binary_location = bin_path
        self.browser = webdriver.Chrome(
            executable_path="./chromedriver", options=option
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
                                  "rank": index+1,
                                  "mmr": element.text[-9:][:4]
                                  })
            # print(index, element.text)
        return top100players
