#!/usr/bin/env python

"""
Scrape etiquette: http://meta.stackexchange.com/questions/443/etiquette-of-screen-scraping-stack-overflow

 - Use GZIP requests
 - Identify yourself using the user-agent using an URL
 - Use JSON, RSS or an API when available
 - Be considerate, If pulling data for more than every 15, ask permission

"""


import csv
import time
import requests
from random import randint
from bs4 import BeautifulSoup


PROJECT = 'http://techcrunch.com/'
YEARS = range(2005, 2015)

custom_headers = {'content-encoding': 'gzip', 
                  'User-Agent': 'My User Agent 0.1',
                  'From': 'thinkxl@gmail.com'}

def get_years_available(url, year):
    """
    Test how many pages are available in a year
    """
    results = []
    
    def populate_results(count):
        """
        This will send a GET request to the url and check if is successful,
        it will append the url to the results list until it get a 404.
        """

        # ex: `http://techcrunch.com/2005/page/2`
        new_url = url + str(year) + '/page/' + str(count)
        r = requests.get(new_url, headers=custom_headers)
        if r.status_code == 200:
            results.append(new_url)

            # We add some sleep time to don't get mad the webmaster :) also
            # we set a variable number between 0 and 5 seconds for look less
            # like a bot.
            time.sleep(randint(0, 5))
            populate_results(count + 1)
        else:
            pass 

    populate_results(2)
    return results

def get_list_of_urls(project):
    """
    Return a list of urls based on the post title.
    """
    soup = get_content(project)
    li = soup.find_all('h2', class_='post-title')
    urls = [link.find('a').get('href') for link in li]
    print urls

def get_content(url):
   return BeautifulSoup(requests.get(url).text, headers=custom_headers)
   # return soup.find('div', class_='article-entry').find_all('p')

def main():
    # article = get_content(URL)
    # print (' ').join([p.string for p in article])
    print get_years_available(PROJECT, '2005')


if __name__ == '__main__':
    main()
