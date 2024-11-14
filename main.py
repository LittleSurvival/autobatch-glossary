import json
import requests
import time
import re
from pathlib import Path

class GlossaryBatchInput:
    
    def __init__(self, link, authtoken, delay, glossary = { }) -> None:
        self.link = link
        self.token = authtoken
        self.glossary = glossary
        self.delay = delay
        
        self.pass_page = []
        self.pass_novel = []
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.cookies = {
            '_ga': 'GA1.1.1043814632.1724884493',
            '_ga_QD8MZ90XFJ': 'GS1.1.1731564012.149.1.1731564856.0.0.0',
        }

    def find_favorite_novel(self):
        page = 0
        total_page = 500
        novel_links = []
        
        print(f'Loading Novels...')
        
        while(page < total_page):
            api_link = self.format_favorite_link(self.link, page)
            response = requests.get(api_link, headers=self.headers)
            
            if response.status_code == 200:
                result = response.json()
                total_page = int(result.get('pageNumber'))
                
                for item in result.get('items'):
                    novel = {
                        'id': f"{item.get('providerId')}/{item.get('novelId')}",
                        'name': f"{item.get('titleJp')}"
                    }
                    novel_links.append(novel)
                    print(f'Find Novel > {novel["id"]} - {novel['name']}')
            else:
                self.pass_page.append(api_link)
                print(f'Failed to load page {page}...Pass')
        
            page += 1
            time.sleep(self.delay)
        
        print(f'Finish Scan...{len(novel_links)} novels is found')
        
        return novel_links
    
    def input_glossary(self):
        novels = self.find_favorite_novel()
        
        for novel in novels:
            api_id = novel['id']
            api_link = f'https://books.fishhawk.top/api/novel/{api_id}/glossary'
            response = requests.put(api_link, json=self.glossary, headers=self.headers, cookies=self.cookies)
            
            
            
            if response.status_code == 200:
                print(f'Input Glossary for Novel {novel['name']}({api_id})')
            else:
                print(f'Failed to Input Glossary for Novel {novel['name']}({api_id})')
                print(f'Info : {response.status_code} - {response.text}')
            
            time.sleep(self.delay)
                
        
    def format_favorite_link(self, link, page):
        link = link.rstrip('/')
        parts = link.split('/')
        if len(parts) >= 4 and 'books' in parts[2]:
            return f"https://{parts[2]}/api/user/favored-web/{parts[-1]}?page={page}&pageSize=30&sort=update"  
        else: 
            return "Invalid input: URL format is incorrect."        

############################
#Global Part
############################

def readSettings():
    settings_file = Path('settings.json')
    glossary_file = Path('glossary.txt')

    default_settings = {
        'authtoken': '',
        'link': '',
        'delay': 3
    }

    if not settings_file.is_file():
        with open(settings_file, 'w') as f:
            json.dump(default_settings, f, indent=3)
    
    if not glossary_file.is_file():
        glossary_file.touch()

    with open(settings_file, 'r') as f:
        try:
            settings = json.load(f)
        except json.JSONDecodeError:
            settings = default_settings.copy()
            with open(settings_file, 'w') as fw:
                json.dump(settings, fw, indent=3)
        else:
            for key in default_settings:
                if key not in settings:
                    settings[key] = default_settings[key]
            settings = {k: settings[k] for k in default_settings}
            with open(settings_file, 'w') as fw:
                json.dump(settings, fw, indent=3)
    
    with open(glossary_file, 'r') as f:
        lines = f.readlines()
    
    
    glossary = fix_json_format(''.join(line.replace('"','\'').strip() for line in lines if line.strip())) 
    return settings, glossary

def fix_json_format(s):
    s = s.replace("'", '"')
    s = s.strip('{}').strip()
    
    pattern = r'"(.*?)"\s*:\s*"(.*?)"'
    matches = re.findall(pattern, s)
    
    data = {key.strip(): value.strip() for key, value in matches}
    return data

def main():
    settings, glossary_input = readSettings()
    
    authtoken = settings['authtoken']
    link = settings['link']
    delay = int(settings['delay'])
    glossary = glossary_input
    
    if not authtoken or not link:
        print('請先輸入AuthToken和Link...結束')
        exit(0)
    
    check = input(f'此工具目前僅能直接覆蓋術語表, 可能造成不可逆的損害 ( 共{len(glossary)}個術語 ) 請問您要繼續嗎 (Y/N) : ')
    
    if len(glossary) == 0:
        check = input(f'這是把術語表清掉的意思, 你確定你沒瘋? (Y/N) : ')
    
    if check.lower() == 'y':
        batcher = GlossaryBatchInput(link, authtoken, delay, glossary)
        batcher.input_glossary()
    

if __name__ == "__main__":
    main()