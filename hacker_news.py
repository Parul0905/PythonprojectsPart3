import csv
import requests
from bs4 import BeautifulSoup

HN_URL="https://news.ycombinator.com/"
CSV_FILE="hn_top20.csv"

def fetch_top_posts():
    try:
        response=requests.get(HN_URL,timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error occured {e}")
        return []
    soup=BeautifulSoup(response.text,'html.parser')
    post_links=soup.select('span.titleline > a')
    print(post_links)

    posts = []
    for link in post_links[:20]:
        title = link.text.strip()
        url = link.get('href').strip()
        posts.append({'title': title, 'url': url})
    return posts

def save_to_csv(posts):
    if not posts:
        print('Nothing to save')
        return
    with open(CSV_FILE, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url"])
        writer.writeheader()
        writer.writerows(posts)
    print(f"✅ Saved Hacker news to {CSV_FILE}")

def main():
    print('Scraping HN portal...')
    posts = fetch_top_posts()
    print('Collected all hacker data')
    save_to_csv(posts)

if __name__=="__main__":
    main()


