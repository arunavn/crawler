from os import replace
import requests
import pdfplumber
import re
from bs4 import BeautifulSoup
import math

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