#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install scrapy
# !pip install pyexcel pyexcel-xls pyexcel-xlsx


# In[2]:


import scrapy
from urllib.parse import urlencode
import ast
import pyexcel as p


# In[3]:


class CepeaSpider(scrapy.Spider):
    
    name = "cepea"
    temp_folder = '../temp/'
    folder = '../files/'
    path = f'{name}.xls'

    params = {
        'tabela_id': 23, 
        'data_inicial':'01/12/2020',
        'periodicidade':1,
        'data_final':'15/12/2020',
    }
    
    start_urls = [
        'https://www.cepea.esalq.usp.br/br/consultas-ao-banco-de-dados-do-site.aspx?' + urlencode(params),
    ]
    
    def parse(self, response):
        final_url = ast.literal_eval(response.text)
        arquivo = final_url['arquivo'].replace("\\", "")
        # print(arquivo)
        yield scrapy.Request(
            url=arquivo,
            callback=self.save_pdf
        )
    
    def save_pdf(self, response):
        self.logger.info('Saving PDF %s', self.temp_folder + self.path)
        with open(self.temp_folder + self.path, 'wb') as f:
            f.write(response.body)


# In[4]:


# %%capture
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(CepeaSpider)
process.start()


# In[7]:


get_ipython().run_cell_magic('capture', '', "p.save_book_as(file_name = CepeaSpider.temp_folder + CepeaSpider.path,\n               dest_file_name = CepeaSpider.folder + CepeaSpider.path + 'x')")

