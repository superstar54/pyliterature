# encoding=utf8  
from __future__ import print_function

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
"""
This module defines an module to fetch article text from
scientific journal.

Author: Xing Wang <xingwang1991@gmail.com>
"""
import spynner  
import os  
import urllib  
from bs4 import BeautifulSoup
import time
import re
import sys

WEB_SITE = [
    "nature", "science", "sciencedirect", "acs",
    "rsc", "wiley"
]


class Pyliterature():
    """
    Class for Pyliterature parser
    """

    def __init__(self, url=None, keyword = None):
        self.text = ''
        self.url_list = []
        self.keysents = ''
        self.url = url
        self.keyword = keyword
        self.wait = 0

        self.PARSER = {
            'nature':self.parse_nature,
            'science':self.parse_science,
            'sciencedirect':self.parse_sciencedirect,
            'acs':self.parse_acs,
            'rsc':self.parse_rsc,
            'wiley':self.parse_wiley
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
            html = self.load_html()
            self.text += parser(html)

        # print(text)
        # print('\n\n\n')

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
            print('Unrecognized journal. \n \
                We only support {0}'.format(WEB_SITE))  

        parser = self.PARSER[journal]
        return parser  


    def load_html(self):
        """
        load html using spynner
        """
        #
        browser = spynner.Browser()
        #
        browser.hide()
        # browser.show()
        try:
            browser.load(self.url, load_timeout=300)
            browser.wait(self.wait)
            html = browser.html
        except spynner.SpynnerTimeout:
            html = None
        else:
            html = browser.html
        browser.close()
        return html 
    

    def parse_nature(self, html):
        '''
        nature
        '''
        soup = BeautifulSoup(html, from_encoding='utf8')
        #
        text = ''
        contents = soup.find_all('div', {'class':"content"})
        for content in contents:
            pars = content.find_all('p')
            for par in pars:
                text += par.get_text()
                text += '\n'
        return text 

    def parse_science(self, html):
        '''
        science
        '''
        soup = BeautifulSoup(html, from_encoding='utf8')
        #
        text = ''
        contents = soup.find_all('div', {'class':"article fulltext-view "})
        for content in contents:
            pars = content.find_all('p')
            for par in pars:
                text += par.get_text()
                text += '\n'
        return text 

    def parse_sciencedirect(self, html):
        '''
        sciencedirect
        '''
        soup = BeautifulSoup(html, from_encoding='utf8')
        #
        text = ''
        contents = soup.find_all('div', {'class':'page_fragment'})
        for content in contents:
            pars = content.find_all('p')
            for par in pars:
                text += par.get_text()
                text += '\n'
        return text 

    def parse_acs(self, html):
        '''
        acs
        '''
        soup = BeautifulSoup(html, from_encoding='utf8')
        #
        text = ''
        contents = soup.find_all('div', {'class':'NLM_p'})
        for content in contents:
            text += content.get_text()
            text += '\n'
        return text 

    def parse_rsc(self, html):
        '''
        rsc
        '''
        soup = BeautifulSoup(html, from_encoding='utf8')
        #
        text = ''
        contents = soup.find_all('div', {'id':'wrapper'})
        for content in contents:
            pars = content.find_all('p')
            for par in pars:
                text += par.get_text()
                text += '\n'
        return text 

    def parse_wiley(self, html):
        '''
        wiley
        '''
        soup = BeautifulSoup(html, from_encoding='utf8')
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
    # science
    # url = 'http://science.sciencemag.org/content/355/6320/49.full'

    # nature
    # url = 'http://www.nature.com/nature/journal/v541/n7635/full/nature20782.html'

    # sciencedirect
    url = 'http://www.sciencedirect.com/science/article/pii/S1751616116301138'

    # ACS catalysis
    # url = 'http://pubs.acs.org/doi/full/10.1021/acscatal.6b02960'

    # ACS JACS
    # url = 'http://pubs.acs.org/doi/full/10.1021/jacs.6b10984'

    # RSC PCCP
    # url = 'http://pubs.rsc.org/en/content/articlehtml/2017/cp/c6cp08110j'

    # Wiley ange
    # url = 'http://onlinelibrary.wiley.com/doi/10.1002/ange.201503022/full'


    keyword = 'CALPHAD'
    liter = Pyliterature(url, keyword)
