import requests
import time
import pandas as pd
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Comment
from datetime import datetime
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

visited_links = set()


def normalize_url(url):
    # URLを6つのコンポーネントに分割
    scheme, netloc, path, params, query, fragment = urlparse(url)

    # ネットロケーションを小文字にする
    netloc = netloc.lower()

    # クエリパラメータをソートする
    query = urlencode(sorted(parse_qsl(query)))

    # 正規化されたURLを作成
    normalized_url = urlunparse((scheme, netloc, path, params, query, fragment))

    return normalized_url

def get_links_recursive(url, num, main_url, delay):
    try:
        reqs = requests.get(url)
    except Exception as e:
        print(f"{url} へのアクセスに失敗しました")
        return [], num

    visited_links.add(url)

    soup = BeautifulSoup(reqs.content, 'lxml')

    # HTMLから不要な要素を削除
    # コメントを削除
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    # scriptタグを削除
    for script in soup.find_all('script'):
        script.decompose()
    # noscript, header, asideタグを削除
    for tag in soup.find_all(['noscript', 'header', 'aside']):
        tag.extract()
    # パンくずリストを削除
    for breadcrumbs in soup.find_all('div', attrs={'class': ['p-breadcrumbs']}):
        breadcrumbs.extract()
    # div, sectionタグを削除（中身は残す）
    for tag in soup.find_all(['div', 'section']):
        tag.unwrap()

    data = [] # 収集したデータを保存するためのリスト

    for link in soup.find_all('a'):
        relative_url = link.get('href', '')
        if '#' in relative_url:
            continue
        title = link.string
        span = link.find('span')
        if span is not None:
            title = span.get_text(strip=True)
        if title is None:
            title = relative_url

        # HTMLから抽出した相対URLを絶対URLに変換し、正規化する
        full_url = normalize_url( urljoin(url, relative_url) )

        if main_url in full_url:
            if full_url in visited_links:
                continue

            visited_links.add(full_url)
            fetch_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if ".pdf" in full_url or ".doc" in full_url or ".xlsx" in full_url or ".pptx" in full_url:
                html = "" 
            else:
                html = str(soup)
            data.append([title, full_url, html, fetch_date])
            num += 1
            print(f"{num}個目のURLを発見: {full_url}")
            
            time.sleep(delay)
    
    return data, num

def explore_links_until_exhausted(url, main_url, delay):
    all_data = []
    new_links = [url]
    num = 0

    while new_links:
        current_url = new_links.pop(0)
        new_data, num = get_links_recursive(current_url, num, main_url, delay)
        all_data.extend(new_data)

        new_links.extend([link[1] for link in new_data])

    return all_data

def write_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Title', 'URL', 'HTML', '取得日'])
    df.to_csv(filename, index=False, encoding='utf-8')
