from os import replace
import requests
import pdfplumber
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
import os
import pandas as pd
import numpy as np

def download_file(url):
    local_filename = url.split('/')[-1]
    
    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)
        
    return local_filename
def text_extractor(pdfFile, firstPageHeaderPct= 0.17, remPageHeaderPct= 0.06, bottomMarginPct= 0.07, rightMarginPct= 0.6, leftMarginPct= 0.10 ):
    extractedText= ''
    urlList=[]
    rege= re.compile("http://|https://")
    
    with pdfplumber.open(pdfFile) as pdf:
        pages= len(pdf.pages)
        for p in range(0,pages):
            page= pdf.pages[p]
            for j in rege.finditer(page.extract_text()):
                s= j.start()
                u= ( page.extract_text()[s:].split('\n') )[0]
                urlList.append(u.strip())
            bottom= float(1 - bottomMarginPct) * float(page.height)
            if p == 0:
                h_height= float(firstPageHeaderPct) * float(page.height)
                pdf_head = page.crop( (0, 0 , page.width, h_height) )
                extractedText+= pdf_head.extract_text() + '\n' +'#' + '-'*100 + '#'+'\n'
            else:
                h_height= float(remPageHeaderPct) * float(page.height)
            pct_per_col= float( ( 1 - float(remPageHeaderPct) - float(remPageHeaderPct) )  / 3 )
            
#             for c in range(0,3):
#                col_text = page.crop( (float(pct_per_col)*float(c)*float(page.width), h_height , float(pct_per_col)*float(c+1)*float(page.width), page.height) )
#                extractedText+= col_text.extract_text() 
            texts_list= [None, None, None]
            first_col = page.crop( (0, h_height , float(0.33)*float(page.width), bottom) )
            texts_list[0]= first_col.extract_text()
            second_col = page.crop( (float(0.35)*float(page.width), h_height , float(0.62)*float(page.width), bottom) )
            texts_list[1]= second_col.extract_text()
            third_col = page.crop( (float(0.63)*float(page.width), h_height , page.width, bottom) )
            texts_list[2]= third_col.extract_text()
            for t in texts_list:
                if t is not None:
                    extractedText+= t #+ '\n' +'#' + '-'*100 + '#'+'\n'
    #extractedText = extractedText.replace('.\n', '. \n\n')
    
    extractedText = extractedText.replace('. \n', '. \n\n')
    extractedText = extractedText.replace('. \n\n', '. \n\n')
    
    return [extractedText, urlList]

def extract_urls(searchUrl):
    requests.adapters.DEFAULT_RETRIES = 2
    url_list= []
    try:
        response = requests.get(searchUrl)
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            url_list.append((link.get('href')))
    except:
        pass
    return url_list

def crawler( startUrlList, crawlLevel= 1 ):
    final_list= [{ 'level': 0, 'source': 0, 'url': su } for su in startUrlList  ]
    url_list, next_list= list(startUrlList), []
    for i in range(0,crawlLevel):
        for u in url_list:
            url_list_temp= extract_urls(u)
            for nurl in url_list_temp:
                if nurl != u:
                    node= { 'level': i+1, 'source': u, 'url': nurl }
                    final_list.append(node)
                    next_list.append(nurl)
        url_list= list(next_list)
    return final_list


def fill_web_form(url, in_dict, searchbuttonText= 'Search'):
    os.environ['MOZ_HEADLESS'] = '1'
    driver = webdriver.Firefox()
    driver.get(url)
    for k, v in in_dict.items():
        ele= driver.find_element_by_id(k)
        if ele.tag_name == 'input':
            driver.execute_script("document.getElementById('{0}').value = '{1}';".format(k, v))
        elif ele.tag_name == 'select' :
            v_list, sel = [], Select(ele)
            if v != '' and v is not None:
                try:
                    sel.deselect_all()
                except:
                    pass
                if not isinstance(v, list):
                    v_list= [v]
                else:
                    v_list= list(v)
                for i in v_list:
                    try:
                        sel.select_by_visible_text(i)
                    except:
                        pass
    btn= driver.find_element_by_xpath('//*[@id="ctl00_MainContent_btnSearch"]')
    btn.click()
    return driver.page_source
def extract_result_table(pageSource, url, tableID= 'Name'):
    try:
        table_data= pd.read_html(pageSource, attrs= {'id': 'gvSearchResults'})[0]
        table_data= table_data.replace(np.nan, '', regex= True )
        table_head= pd.read_html(pageSource, attrs= {'id': 'resultsHeaderTable'})[0]
        table_head, table_data= table_head.values, table_data.values
        output=[]
        for r in table_data:
            out_dict={}
            for i, d in enumerate(r):
                if d==np.nan:
                    d= ''
                out_dict[table_head[0][i]] = d
            output.append(out_dict)
    except:
        output= [{'error': 'no data found for given filters'}]
    soup = BeautifulSoup(pageSource, 'html.parser')
    url_list=[]
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            url_list.append((link.get('href')))
    for link in soup.find_all('a', attrs={'href': re.compile("^Details.aspx")}):
        url_list.append(url + '/' + (link.get('href')))
    return [output, url_list]

