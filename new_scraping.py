# coding: utf-8

# モジュールをインポート
import requests
import time
import pandas as pd
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Comment
from datetime import datetime
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

# 対象のURL
url3 = 'https://www.digitalservice.metro.tokyo.lg.jp/smarttokyo/index.html'
main_url = urlparse(url3).netloc

# 同じページを複数回訪れるのを防ぐために、訪れたリンクを保存
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

def remove_unnecessary_elements(soup):
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

def get_links_recursive(url, num):
    try:
        reqs = requests.get(url, timeout=10)  # timeoutパラメータを設定
    except requests.exceptions.Timeout:
        print(f"{url} へのアクセスがタイムアウトしました")
        return [], num
    except Exception as e:
        print(f"{url} へのアクセスに失敗しました")
        return [], num

    # URLを訪れたリンクのセットに追加
    visited_links.add(url)

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(reqs.content, 'lxml')

    # HTMLから不要な要素を削除
    remove_unnecessary_elements(soup)

    # 収集したデータを保存するためのリスト
    data = []
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

            # スクレイピング対象外の拡張子
            excluded_extensions = [".pdf", ".zip", ".doc", ".docx", ".csv", ".pptx", "xls", ".xlsx", ".jpg", ".mp4"]
            for extension in excluded_extensions:
                if extension in full_url:
                    html = ""
                    break

            else:
                try: # リンク先のURLにリクエストを送ってHTMLを取得
                    reqs_link = requests.get(full_url)
                    soup_link = BeautifulSoup(reqs_link.content, 'lxml')
                    remove_unnecessary_elements(soup_link)  # リンク先のHTMLからも不要な要素を削除
                    html = str(soup_link.main) # HTMLのmain部分を抽出
                except requests.exceptions.Timeout:
                    print(f"{full_url} へのHTML取得のリクエストがタイムアウトしました")
                    html = "error"
                except Exception as e:
                    print(f"{full_url} へのHTML取得のリクエストに失敗しました")
                    html = ""
            
            data.append([title, full_url, html, fetch_date])
            num += 1
            print(f"{num}個目のURLを発見: {full_url}")
            
            time.sleep(0.7)
    
    return data, num

# 新しいリンクが発見されなくなるまでループを続ける関数
def explore_links_until_exhausted(url):
    all_data = []
    new_links = [url]
    num = 0

    while new_links:
        current_url = new_links.pop(0)
        new_data, num = get_links_recursive(current_url, num)
        all_data.extend(new_data)

        # 新しいリンクを追加
        new_links.extend([link[1] for link in new_data])

    return all_data

# 再帰的にリンクを探す
data = explore_links_until_exhausted(url3)

# DataFrameを作成し、CSVとして出力
df = pd.DataFrame(data, columns=['Title', 'URL', 'HTML', '取得日'])
df.to_csv('digital_03.csv', index=False, encoding='utf-8')
