import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def get_h2_headers(url):
    try:
        response = requests.get(url, timeout=10, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    h2_tags = soup.find_all('h2')

    headers = []
    for tag in h2_tags:
        header_text = tag.get_text(strip=True)
        if header_text and header_text.lower() != 'contents':
            headers.append(header_text)

    return headers[:10]

if __name__ == "__main__":
    print(get_h2_headers(URL))


