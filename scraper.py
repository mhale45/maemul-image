import requests
from lxml import html
import os
from datetime import datetime
import re

def get_item_data(item_id):
    url = f"https://baikuk.com/item/view/{item_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    item_data = {
        "id": item_id,
        "deposit": "",
        "rent": "",
        "area": "",
        "floor": "",
        "images": []
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return item_data

        tree = html.fromstring(response.content)
        
        # 상세 정보 추출 (제공된 XPath 사용)
        try:
            deposit_el = tree.xpath('/html/body/section/section/div/div/div/div[1]/div[2]/div/div[1]/h4/span[1]/span[2]')
            item_data["deposit"] = deposit_el[0].text.strip() if deposit_el else ""

            rent_el = tree.xpath('/html/body/section/section/div/div/div/div[1]/div[2]/div/div[1]/h4/span[2]/span[2]')
            item_data["rent"] = rent_el[0].text.strip() if rent_el else ""

            # 전용면적 추출 (tbody 유무 대응)
            area_xpath = '/html/body/section/section/div/div/div/div[1]/div[3]/table/tbody/tr/td[2]/div/div[2]/h4/span[2]'
            area_el = tree.xpath(area_xpath)
            if not area_el:
                area_el = tree.xpath(area_xpath.replace('/tbody', ''))
            item_data["area"] = area_el[0].text.strip() if area_el else ""

            # 층정보 추출 (span 2개 이어서 표시)
            floor_xpath_base = '/html/body/section/section/div/div/div/div[1]/div[3]/table/tbody/tr/td[3]/div/div[2]/h4'
            floor_h4_el = tree.xpath(floor_xpath_base)
            if not floor_h4_el:
                floor_h4_el = tree.xpath(floor_xpath_base.replace('/tbody', ''))
            
            if floor_h4_el:
                # h4 하위의 모든 span 텍스트를 추출하여 합침
                spans = floor_h4_el[0].xpath('.//span/text()')
                item_data["floor"] = "".join(spans).strip()
            else:
                item_data["floor"] = ""

        except Exception as e:
            print(f"Error extracting details for {item_id}: {e}")

        # 이미지 추출
        xpath_query = '//*[@id="slide_s"]//div[contains(@class, "bg_img")]'
        elements = tree.xpath(xpath_query)
        
        image_urls = []
        for el in elements:
            style = el.get('style', '')
            match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
            if match:
                path = match.group(1)
                full_url = "https://baikuk.com" + path if path.startswith('/') else path
                if full_url not in image_urls:
                    image_urls.append(full_url)
        
        item_data["images"] = image_urls
        return item_data

    except Exception as e:
        print(f"Error fetching data for {item_id}: {e}")
        return item_data

