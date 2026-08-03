import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def audit_url(url):
    print(f"[*] Auditing: {url}")
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'lxml')
        
        title = soup.find('title').text.strip() if soup.find('title') else 'N/A'
        h1 = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
        canonical = soup.find('link', rel='canonical')['href'] if soup.find('link', rel='canonical') else 'Missing'
        
        data = {
            'URL': url,
            'Status Code': response.status_code,
            'Title': title,
            'H1': h1,
            'Canonical': canonical
        }
        
        df = pd.DataFrame([data])
        df.to_csv('audit_report.csv', index=False)
        print("[+] Audit Complete! Results saved to 'audit_report.csv'.")
        
    except Exception as e:
        print(f"[-] Error auditing {url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "https://linkoster.com"
    audit_url(target)
