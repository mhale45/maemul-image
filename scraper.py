import requests
from lxml import html
import os
from datetime import datetime
import re

def get_images(item_id):
    url = f"https://baikuk.com/item/view/{item_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []

        tree = html.fromstring(response.content)
        
        # 이미지 추출을 위해 'bg_img' 클래스를 가진 요소를 찾습니다.
        xpath_query = '//*[@id="slide_s"]//div[contains(@class, "bg_img")]'
        elements = tree.xpath(xpath_query)
        
        image_urls = []
        for el in elements:
            style = el.get('style', '')
            match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
            if match:
                path = match.group(1)
                full_url = "https://baikuk.com" + path if path.startswith('/') else path
                if full_url not in image_urls: # 중복 제거
                    image_urls.append(full_url)

        return image_urls

    except Exception as e:
        print(f"Error fetching images for {item_id}: {e}")
        return []
