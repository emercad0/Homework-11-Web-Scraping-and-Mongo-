import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
from random import randint
#import tweepy

class mars_crawler(): 
        def __init__(self):
            self.crawl_this = "https://mars.nasa.gov/news/"
            self.recent_news = []
        # Open headless chromedriver
        def init_driver(self):
            print('starting chromedriver')
             #self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')
            #self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')
            executable_path = {"executable_path": "/Users/edgar_macbook/Downloads/chromedriver"}
            self.browser= Browser("chrome",**executable_path , headless=False)
            time.sleep(4)
         # Close chromedriver
        def end_driver(self): 
            print('closing the driver..')
            self.browser.quit()
            print('closed')
        # Tell the browser to get a page
        def get_page(self, url):
            print('getting page...')
            self.browser.visit(url)
            time.sleep(randint(2, 3))
        # grab what we need
        def grab_list(self):
            # Scrape page into soup
            html = self.browser.html
            self.soup = bs(html, 'html.parser')
            print('pulling the list of items...')
            for div in self.soup.find("div", class_="list_text"):
                data = self.process_elements(div)
                if data:
                       self.recent_news.append(data)
                else:
                        pass
        
        def process_elements(self, div):
            news_date = ''
            news_title = ''
            news_p = ''
            try:
                news = self.soup.find("div", class_="list_text")
                news_date = news.find("div", class_="list_date").text
                news_title = news.find("div", class_="content_title").text
                news_p = news.find("div", class_="article_teaser_body").text
            except Exception:
                    pass
                    
            if news_date and news_title:
                news_info = {
                    'Date': news.find("div", class_="list_date").text,
                    'Title': news.find("div", class_="content_title").text,
                    'Summary': news.find("div", class_="article_teaser_body").text
                }
                
                return news_info
            else:
                return False
        
        def parse(self):
            self.init_driver()
            self.get_page(self.crawl_this)
            self.grab_list()
            self.end_driver()
            
            if self.recent_news:
                return self.recent_news
            else:
                return False, False
#run crawler
mars_pull = mars_crawler()
article_list = mars_pull.parse()

#print(type(items_list))
#show our data
for news in article_list:
    print(news)


