import requests
from lxml import html
import os
from datetime import datetime
import re

def scrape_baikuk():
    url = "https://baikuk.com/item/view/27852"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Fetching {url}...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return

    tree = html.fromstring(response.content)
    
    # 이미지 추출을 위해 'bg_img' 클래스를 가진 요소를 찾습니다.
    # 사용자가 제공한 XPath 구조를 포함하여 더 유연하게 탐색합니다.
    xpath_query = '//*[@id="slide_s"]//div[contains(@class, "bg_img")]'
    elements = tree.xpath(xpath_query)
    
    image_urls = []
    for el in elements:
        style = el.get('style', '')
        match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
        if match:
            path = match.group(1)
            full_url = "https://baikuk.com" + path if path.startswith('/') else path
            if full_url not in image_urls: # 중복 제거 (Slick 클론 방지)
                image_urls.append(full_url)

    print(f"Found {len(image_urls)} unique images.")

    # 추출 실패 시 처리
    if not image_urls:
         image_urls = ["https://via.placeholder.com/1200x800?text=No+Images+Found"]

    # 이미지 HTML 생성 (슬라이더 구조)
    images_html = ""
    for url in image_urls:
        images_html += f'            <div class="slide"><img src="{url}" alt="매물 이미지"></div>\n'

    # 템플릿 읽기
    template_path = "index.template.html"
    if not os.path.exists(template_path):
        print(f"Template not found at {template_path}")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 치환
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = content.replace("{{IMAGES}}", images_html)
    content = content.replace("{{LAST_UPDATED}}", now)

    # index.html 저장
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("Successfully updated index.html with all images.")

if __name__ == "__main__":
    scrape_baikuk()
