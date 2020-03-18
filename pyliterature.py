#-*- coding: utf-8 -*-
"""
This module defines an module to fetch article text from
scientific journal.

Author: Xing Wang <xingwang1991@gmail.com>
"""
import os  
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
options = Options()
options.headless = True


WEB_SITE = [
    "nature", "science", "sciencedirect", "acs",
    "rsc", "wiley", "none"
]

class Pyliterature():
    """
    Class for Pyliterature parser
    """

    def __init__(self, url=None, keyword = None, wait = 0):
        self.text = ''
        self.doi = None
        self.database = None

        self.url_list = []
        self.keysents = ''
        self.url = url
        self.keyword = keyword
        self.wait = wait

        self.PARSER = {
            'nature':self.parse_nature,
            'science':self.parse_science,
            'sciencedirect':self.parse_sciencedirect,
            'acs':self.parse_acs,
            'rsc':self.parse_rsc,
            'wiley':self.parse_wiley,
            'none':None,
            }


    def read_database(self, filename):
        """
        load(html) is very slow, it's better to read text in a database
        """
        self.database = filename

        if not os.path.exists('{0}'.format(self.database)):
            os.mkdir('{0}'.format(self.database))
            open('{0}/text.dat'.format(self.database), 'w').close()
            open('{0}/url_list.dat'.format(self.database), 'w').close()
            return
        # read url list
        with open('{0}/url_list.dat'.format(self.database)) as file:
            lines = file.read().splitlines() 
            for line in lines:
                self.url_list.append(line)
        file.close()
        # read text
        with open('{0}/text.dat'.format(self.database)) as file:
            lines = file.read().splitlines() 
            for line in lines:
                self.text += line
        file.close()

    def save_database(self):
        """
        save all the text and url in a database
        """
        if self.database == None:
            self.database = self.keyword
        if not os.path.exists('{0}'.format(self.database)):
            os.mkdir('{0}'.format(self.database))
            open('{0}/text.dat'.format(self.database), 'w').close()
            open('{0}/url_list.dat'.format(self.database), 'w').close()
        #
        with open('{0}/text.dat'.format(self.database), 'w') as file:
            file.write(self.text)
            # file.write('\n')
        file.close()
        with open('{0}/url_list.dat'.format(self.database), 'w') as file:
            for url in self.url_list:
                file.write(url)
                file.write('\n')
        file.close()

    def parser(self):
        if self.url:
            self.url_list.append(self.url)
            parser = self.check_journal()
            if not parser:
                return 0
            html = self.load_html()
            soup = BeautifulSoup(html, "lxml")
            text = parser(soup)
            self.text += text

        #
        if self.keyword:
            self.keysents = self.parse_keyword(self.text, self.keyword)
            # for keysent in keysents:
                # print(keysent)
                # print('\n')


    def check_journal(self):
        """
        check journal according to the url
        """
        if 'sciencemag' in self.url:
            journal = 'science'
        elif 'nature' in self.url:
            journal = 'nature'
        elif 'sciencedirect' in self.url:
            # sciencedirect drop down the page to generate the whole page source
            self.url += '#ack001'
            self.wait = 5
            journal = 'sciencedirect'
        elif 'pubs.acs' in self.url:
            journal = 'acs'
        elif 'pubs.rsc' in self.url:
            journal = 'rsc'
        elif 'wiley' in self.url:
            journal = 'wiley'
        else:
            journal = 'none'
            print('Unrecognized journal. \n \
                We only support {0}'.format(WEB_SITE))  

        parser = self.PARSER[journal]
        return parser  


    def load_html(self):
        """
        load html using spynner
        """
        driver = webdriver.Firefox(options = options)
        driver.get(self.url)
        print('waiting for page...')
        time.sleep(self.wait)
        page_source = driver.page_source
        driver.close()

        return page_source 
    

    def parse_nature(self, soup):
        '''
        nature
        '''
        #
        text = ''
        contents = soup.find_all('div', {'class':"content"})
        for content in contents:
            pars = content.find_all('p')
            for par in pars:
                text += par.get_text()
                text += '\n'
        return text 

    def parse_science(self, soup):
        '''
        science
        '''
        #
        text = ''
        contents = soup.find_all('div', {'class':"article fulltext-view "})
        for content in contents:
            pars = content.find_all('p')
            for par in pars:
                text += par.get_text()
                text += '\n'
        return text 

    def parse_sciencedirect(self, soup):
        '''
        sciencedirect
        '''
        # print(soup)
        #
        text = ''
        contents = soup.find_all('div', {'class':'Body u-font-serif'})
        # print(contents)
        for content in contents:
            pars = content.find_all('p')
            for par in pars:
                text += par.get_text()
                text += '\n'
        # print(text)
        return text 

    def parse_acs(self, soup):
        '''
        acs
        '''
        #
        text = ''
        contents = soup.find_all('div', {'class':'NLM_p'})
        for content in contents:
            text += content.get_text()
            text += '\n'
        return text 

    def parse_rsc(self, soup):
        '''
        rsc
        '''
        #
        text = ''
        contents = soup.find_all('div', {'id':'wrapper'})
        for content in contents:
            pars = content.find_all('p')
            for par in pars:
                text += par.get_text()
                text += '\n'
        return text 

    def parse_wiley(self, soup):
        '''
        wiley
        '''
        #
        text = ''
        contents = soup.find_all('article', {'id':'main-content'})
        for content in contents:
            pars = content.find_all('p')
            for par in pars:
                text += par.get_text()
                text += '\n'
        return text

    

    def parse_keyword(self, text, keyword):
        import nltk
        from nltk.tokenize import sent_tokenize
        sents = sent_tokenize(text)
        keysents = []
        for sent in sents:
            if keyword in sent:
                keysents.append(sent)
        return keysents



if __name__ == "__main__":
    # nature
    # url = 'http://www.nature.com/nature/journal/v541/n7635/full/nature20782.html'
    # sciencedirect
    url = 'http://www.sciencedirect.com/science/article/pii/S1751616116301138'
    # url = 'http://pubs.acs.org/doi/full/10.1021/jz5009483'
    keyword = 'CALPHAD'
    liter = Pyliterature(url, keyword)
    liter.parser()
    # print(liter.text)
    for keysent in liter.keysents:
        print(keysent)
        print('\n')
