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
    
    # 엽XPath: //*[@id="slide_s"]/div[1]/div[1]/div
    # 실제로는 슬라이더 내부의 div 요소들을 가리킵니다.
    xpath_query = '//*[@id="slide_s"]/div[1]/div[1]/div'
    elements = tree.xpath(xpath_query)
    
    image_url = ""
    if elements:
        # style 속성에서 background-image: url('...') 추출
        style = elements[0].get('style', '')
        match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
        if match:
            path = match.group(1)
            if path.startswith('/'):
                image_url = "https://baikuk.com" + path
            else:
                image_url = path
            print(f"Found image URL: {image_url}")
        else:
            print("No background-image found in style attribute.")
    else:
        print("Required XPath element not found.")

    # 추출 실패 시 기본 이미지 적용
    if not image_url:
        image_url = "https://via.placeholder.com/1200x800?text=Image+Not+Found"

    # 템플릿 읽기
    template_path = "index.template.html"
    if not os.path.exists(template_path):
        print(f"Template not found at {template_path}")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 치환
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = content.replace("{{IMAGE_URL}}", image_url)
    content = content.replace("{{LAST_UPDATED}}", now)

    # index.html 저장
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("Successfully updated index.html")

if __name__ == "__main__":
    scrape_baikuk()
