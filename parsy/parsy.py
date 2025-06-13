import requests
import argparse
from bs4 import BeautifulSoup

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--site', required=True, type=str, help='site to parse, http:// or https:// schema required')
    parser.add_argument('-v', '--verbosity', required=False, action='store_true', help='increase verbosity level') # args
    parser.add_argument('--html', required=False, action='store_true', help='get entire page html')

    args = parser.parse_args()

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
          
--------------------------------------------------------------------------------------''')
    
    v = args.verbosity
    site = args.site # vars
    html = args.html
    if not site.startswith(('http://', 'https://')):
        print('[!] Missing schema (http:// or https://)')
        exit()

    def get_page(url): # get page, most of the error checking here
        try:
            print(f'[#] Trying to connect to {url}' if v else '', end='\n' if v else '')
            r = requests.get(url, timeout=7)
            if r.status_code == 404:
                print('[!] 404 Not Found, please check if url you provided is valid')
                exit()
            print(f'[#] Connected succesfuly' if v else '', end='\n' if v else '')
            r.encoding = 'utf-8'
            return r.text
        
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
            headers1 = soup.find_all('h1')
            headers2 = soup.find_all('h2')
            paragraphs = soup.find_all('p')
            images = soup.find_all('img')

            filename = f"results/{site.strip('http://' if 'http://' in site else 'https://').replace('/', '-')}" # filename
            filename = filename.replace('?', '-')
            filename = filename.replace('.', '-')
            if html:
                with open(filename + '.html', 'w', encoding='utf-8') as f:
                    f.write(page_html)
                    print(f'[i] Saved page html as {f.name}')

            filename += '.txt' 
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'\nTITLE - "{title.text}"\n')

                if links:
                    f.write('\n----------------------------------------------------~<#:ALL LINKS:#>~-----------------------------------------------------\n')
                    print(f'[#] Parsing links' if v else '', end='\n' if v else '')
                    for a in links:
                        href = a.get('href')
                        text = a.text.strip()
                        f.write(f'\n{text}: {href}\n')

                else:
                    f.write('\n--------------------------------------------------~<#:NO LINKS FOUND:#>~--------------------------------------------------\n')
                    print(f'[#] No links found' if v else '', end='\n' if v else '')
                
                if headers1:
                    f.write('\n---------------------------------------------------~<#:ALL HEADERS:#>~----------------------------------------------------\n')
                    print(f'[#] Parsing headers' if v else '', end='\n' if v else '')
                    for h1 in headers1:
                        text = h1.text.strip()
                        f.write(f'\n"{text}"\n')
                    if headers2:
                        for h2 in headers2:
                            text = h2.text.strip()
                            f.write(f'\n"{text}"\n')
                else:
                    f.write('\n-------------------------------------------------~<#:NO HEADERS FOUND:#>~-------------------------------------------------\n')
                    print(f'[#] No headers found' if v else '', end='\n' if v else '') 

                if paragraphs:
                    f.write('\n--------------------------------------------------~<#:ALL PARAGRAPHS:#>~--------------------------------------------------\n')
                    print(f'[#] Parsing paragraphs' if v else '', end='\n' if v else '')
                    for p in paragraphs:
                        text = p.text.strip()
                        f.write(f'\n"{text}"\n')
                else:
                    f.write('\n------------------------------------------------~<#:NO PARAGRAPHS FOUND:#>~-----------------------------------------------\n')
                    print(f'[#] No paragraphs found' if v else '', end='\n' if v else '') 


                if images:
                    f.write('\n----------------------------------------------------~<#:ALL IMAGES:#>~----------------------------------------------------\n')
                    print(f'[#] Parsing images' if v else '', end='\n' if v else '')
                    for img in images:
                        src = img.get('src')
                        alt = img.get('alt')
                        f.write(f'\n{alt}: {src}\n')
                else:
                    f.write('\n--------------------------------------------------~<#:NO IMAGES FOUND:#>~-------------------------------------------------\n')
                    print(f'[#] No images found' if v else '', end='\n' if v else '')

                print(f'[i] Report saved as results/{filename}')
        else:
            print('[!] No html to parse, exiting')
            exit()

    parse(get_page(site))

if __name__ == '__main__':
    print('[!] Please, do not run the main script directly')