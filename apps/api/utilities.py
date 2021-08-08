from os import replace
import requests
import pdfplumber

def download_file(url):
    local_filename = url.split('/')[-1]
    
    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)
        
    return local_filename
def text_extractor(pdfFile, firstPageHeaderPct= 0.17, remPageHeaderPct= 0.06, bottomMarginPct= 0.07, rightMarginPct= 0.6, leftMarginPct= 0.10 ):
    extractedText= ''
    with pdfplumber.open(pdfFile) as pdf:
        pages= len(pdf.pages)
        for p in range(0,pages):
            page= pdf.pages[p]
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
                    extractedText+= t + '\n' +'#' + '-'*100 + '#'+'\n'
    return extractedText

