import requests
import argparse
from bs4 import BeautifulSoup

def main():
    print(r'''
        XXXXX                
     Xx+++++++xX$           
   X+;+;;;;;;;+xxX$         
  x++;;;;;;;;;;;+xX$        
 x+;+;;;;;;;;;;;++xX         _ __   __ _ _ __ ___ _   _ 
 x+;;;;;;;;;;;;;;++$$       | '_ \ / _` | '__/ __| | | |
 x+;;;;;;;;;;;;;;+x$&       | |_) | (_| | |  \__ \ |_| |
 Xx;;;;;;;;;;;;;;+XX        | .__/ \__,_|_|  |___/\__, |
  Xx+;;;;;;;;;;;+xX$        |_|                   |___/
    xx++;;;;;++xx++;xX      
      XxxxxxXXX X+;;;;X$    
                 $Xx++;+X$  
                   $Xx++;xX 
                     $XxxXX 
          
------------------------------------------------------------------------------      ''')

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--site', required=True, type=str, help='site to parse, http:// or https:// schema required')
    parser.add_argument('-v', '--verbosity', required=False, action='store_true', help='increase verbosity level (yappier script)') # args

    args = parser.parse_args()
    site = args.site # vars
    v = args.verbosity

    def get_page(url): # get page, most of the error checking here
        try:
            print(f'[#] Trying to connect to {url}' if v else '', end='\n' if v else '')
            r = requests.get(url)
            if r.status_code == 404:
                print('[!] 404 Not Found, please check if url you provided is valid')
                exit()
            print(f'[#] Connected succesfuly' if v else '', end='\n' if v else '')
            r.encoding = 'utf-8'
            return r.text
        
        except requests.exceptions.MissingSchema:
            print('[!] Missing schema, please input http:// or https:// in your url')
            exit()
        except requests.exceptions.ConnectionError:
            print(f'[!] Could not connect to {url}, please check if url you provided is valid')
            exit()
        except requests.exceptions.InvalidURL:
            print(f'[!] Invalid URL')
            exit()
        except requests.exceptions.RequestException as e:
            print(f'[!] An error occured: {e}')
            exit()

    def parse(page_html):
        if page_html:
            print(f'[#] Parsing {site}' if v else '', end='\n' if v else '')
            soup = BeautifulSoup(page_html, 'lxml')

            title = soup.find('title')
            links = soup.find_all('a')
            paragraphs = soup.find_all('p')
            images = soup.find_all('img')

            filename = f"results/{site.strip('http://' if 'http://' in site else 'https://').replace('/', '-')}" # filename
            filename = filename.replace('?', '-')
            filename = filename.replace('.', '-')
            filename += '.txt' 
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'\nTITLE - "{title.text}"\n')

                if links:
                    f.write('\n-------------------------------------------------~<#:ALL LINKS:#>~--------------------------------------------------\n')
                    print(f'[#] Parsing links' if v else '', end='\n' if v else '')
                    for link in links:
                        href = link.get('href')
                        text = link.text.strip()
                        f.write(f'\n{text}: {href}\n')

                else:
                    f.write('\n-----------------------------------------------~<#:NO LINKS FOUND:#>~-----------------------------------------------\n')
                    print(f'[#] No links found' if v else '', end='\n' if v else '')
                
                if paragraphs:
                    f.write('\n-----------------------------------------------~<#:ALL PARAGRAPHS:#>~-----------------------------------------------\n')
                    print(f'[#] Parsing paragraphs' if v else '', end='\n' if v else '')
                    for paragraph in paragraphs:
                        text = paragraph.text.strip()
                        f.write(f'\n"{text}"\n')
                else:
                    f.write('\n---------------------------------------------~<#:NO PARAGRAPHS FOUND:#>~--------------------------------------------\n')
                    print(f'[#] No paragraphs found' if v else '', end='\n' if v else '') 


                if images:
                    f.write('\n-------------------------------------------------~<#:ALL IMAGES:#>~-------------------------------------------------\n')
                    print(f'[#] Parsing images' if v else '', end='\n' if v else '')
                    for img in images:
                        src = img.get('src')
                        f.write(f'\n{src}\n')
                else:
                    f.write('\n-----------------------------------------------~<#:NO IMAGES FOUND:#>~----------------------------------------------\n')
                    print(f'[#] No images found' if v else '', end='\n' if v else '')

                print(f'[i] Report saved as {filename}')
        else:
            print('[!] No html to parse, exiting')
            exit()

    parse(get_page(site))
