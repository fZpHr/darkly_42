import requests
from bs4 import BeautifulSoup
from collections import deque
import os

visited = set()
to_visit = deque()
os.makedirs('found', exist_ok=True)

def crawl(start_url):
    to_visit.append(start_url)
    readme_count = 0
    path_count = 0
    
    while to_visit:
        url = to_visit.popleft()
        if url in visited:
            continue
            
        path_count += 1
        print(f"Path {path_count}: {url}")
        visited.add(url)
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href not in ['.', '..']:
                    full_url = url + href if url.endswith('/') else url + '/' + href
                    if 'README' in full_url:
                        readme = requests.get(full_url)
                        if len(readme.content) != 34:
                            readme_count += 1
                            print(f"\nDownloading README {readme_count} from: {full_url}")
                            print(f"Size: {len(readme.content)} bytes")
                            with open(f'found/README_{readme_count}', 'wb') as f:
                                f.write(readme.content)
                    
                    if full_url not in visited:
                        to_visit.append(full_url)
                        
        except Exception as e:
            print(f"Error on {url}: {e}")
    
    print(f"\nTotal paths: {path_count}")
    print(f"Total READMEs > 34 bytes: {readme_count}")

base_url = "http://10.11.249.0/.hidden/"
crawl(base_url)