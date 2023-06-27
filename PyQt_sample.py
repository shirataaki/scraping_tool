from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

url = "https://www.digitalservice.metro.tokyo.lg.jp/innovativeprojects/robot_showcase.html"
print(urlparse(url).netloc)
def normalize_url(url):
    # URLを6つのコンポーネントに分割
    scheme, netloc, path, params, query, fragment = urlparse(url)

    # ネットロケーションを小文字にする
    netloc = netloc.lower()

    # クエリパラメータをソートする
    query = urlencode(sorted(parse_qsl(query)))

    # 正規化されたURLを作成
    normalized_url = urlunparse((scheme, netloc, path, params, query, fragment))

    print(f"scheme = {scheme}")
    print(f"netloc = {netloc}")
    print(f"path = {path},  params = {params}")
    print(f"query = {query}, fragment = {fragment}") 

    return normalized_url, netloc

nor,net = normalize_url(url)
print(net)