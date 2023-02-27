import time
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

class Perplexity:
    def __init__(self):
        self.driver = None
        self.regex = r"\[[1-9]\]"
        self.isready = False

    def open_search_page(self):
        self.driver.get("https://www.google.com")
        self.driver.get("https://www.youtube.com")
        self.driver.get("https://www.perplexity.ai")

    def is_cloudflare_bypassed(self):
        try:
            element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.ID, 'ppl-query-input')))
            print("Bot is ready to answer your questions.")
            self.isready = True
        except:
            print('Failed to bypass cloudflare!')
            self.driver.quit()

    def start(self):
        if self.driver == None:
            self.driver = uc.Chrome()
            self.open_search_page()
            self.is_cloudflare_bypassed()
        else:
            print("Instance is already running.")
        
    def stop(self):
        if self.driver != None:
            self.driver.quit()
            self.driver = None
        else:
            print("No instances are running.")


    def ask(self,query):
        if self.isready == False:
            print("Bot is not yet ready please use .start() .")
            return None
        old_len = len(self.driver.find_elements(By.CLASS_NAME,"pt-xs"))
        self.driver.find_element(By.ID,"ppl-query-input").send_keys(query+Keys.ENTER)
        results = self.driver.find_elements(By.CLASS_NAME,"pt-xs")
        while results[-1].text == "PERPLEXITY":
            time.sleep(0.5)
        time.sleep(3)
        results = self.driver.find_elements(By.CLASS_NAME,"pt-xs")
        answer = self.parse_answer(results)
        return answer


    def parse_answer(self,results):
        results.reverse()
        answer = "Something went wrong."
        for i in results:
            y = i.text
            if "SOURCES" in y and "View List" in y:
                continue
            if "PERPLEXITY" in y and "View Detailed" in y:
                y = y.replace("PERPLEXITY","").replace("View Detailed","").strip()
            answer = y
            break
        return self.clear_text(answer)


    def clear_text(self,text):
        for x in re.findall(self.regex,text):
            text = text.replace(x,"")

        return text
        
