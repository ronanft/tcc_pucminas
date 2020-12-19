#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install scrapy
# !pip install OleFileIO_PL
# !pip install urllib


# In[2]:


import scrapy
from urllib.parse import urlencode
import ast
from datetime import datetime
import OleFileIO_PL
import pandas as pd
import pickle
from datetime import datetime


# In[3]:


class CepeaSpider(scrapy.Spider):
    
    name = "cepea"
       
    def __new__(cls, name, cod, dt_ini = '01/01/1990', dt_fim = datetime.today().strftime('%d/%m/%Y')):
        instance = object.__new__(cls)
        
        # start_urls
        instance.params = {
        'tabela_id' : cod,
        'data_inicial' : dt_ini,
        'periodicidade' : 1,
        'data_final' : dt_fim,
        }
        instance.start_urls = [
            'https://www.cepea.esalq.usp.br/br/consultas-ao-banco-de-dados-do-site.aspx?' + urlencode(instance.params),
        ]
        
        # Arquivos e pastas
        instance.folder = '../files/'
        marca_data = datetime.today().strftime('%Y-%m-%d')
        instance.fname = f'{name}.{marca_data}.p'
        instance.arquivo = instance.folder + instance.fname
        return instance
    
    def parse(self, response):
        final_url = ast.literal_eval(response.text)
        arquivo = final_url['arquivo'].replace("\\", "")
        yield scrapy.Request(
            url = arquivo,
            callback = self.save
        )

    def save(self, response):
        ole = OleFileIO_PL.OleFileIO(response.body)
        df = pd.read_excel(ole.openstream('Workbook'), skiprows=3)
        df = df.set_index("Data")
        with open(self.arquivo, 'wb') as handle:
            pickle.dump(df, handle)


# In[ ]:


import yaml
from scrapy.crawler import CrawlerProcess
import time

# Load Settings
name = CepeaSpider.name
with open(f"{name}.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

# Run spider
for k, v in config.items():
    time.sleep(5)
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.0)'
    })
    process.crawl(CepeaSpider, name=k, cod=v)

process.start()

