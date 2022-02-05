import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json

file_name = './data/amazon.csv'
with open(file_name, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    rows = []
    for row in reader:
        rows.append(row)

urls = []
for row in rows:
    asin = row[2]
    country = row[3]
    url = f"https://www.amazon.{country}/dp/{asin}"
    urls.append(url)

options = Options()
options.headless = False
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.maximize_window()

start_time = time.time()
data = []
count = 0
section_start_time = time.time()
time_data = ''
for url in urls:
    time.sleep(1)
    count += 1
    if count % 100 == 0:
        time_text = f"count: {count}, time: {time.time() - start_time}"
        print(time_text)
        time_data += time_text + '\n'

    # print(f'Scraping url: {url}')
    browser.get(url)
    browser.set_page_load_timeout(10)

    # get data
    try:
        title_text = ''
        try:
            title = browser.find_element(By.ID, 'productTitle')
            title_text = title.text
        except Exception as e:
            print(f"{url} not available")
            continue

        image_text = ''
        try:
            image_container = browser.find_element(By.ID, 'main-image-container')
            image = image_container.find_element(By.TAG_NAME, 'img')
            image_text = image.get_attribute('src')
        except Exception as e:
            pass

        details_text = ''
        try:
            details_container = browser.find_element(By.ID, 'detailBullets_feature_div')
            details_text = details_container.text
        except:
            pass

        price_text = ''
        try:
            price_section = browser.find_element(By.ID, 'corePriceDisplay_desktop_feature_div')
            price = price_section.find_element(By.CLASS_NAME, 'a-price-whole')
            price_symbol = price_section.find_element(By.CLASS_NAME, 'a-price-symbol')
            price_text = price_symbol.text + price.text
        except Exception as e:
            # print('Price whole not found')
            try:
                price = browser.find_element(By.CSS_SELECTOR, '.olp-new').text
                if 'New from' in price:
                    price = price.split('New from')[1]
                elif 'Neuf à partir de' in price:
                    price = price.split('Neuf à partir de')[1].strip()
                    parts = price.split(' ')
                    price = parts[1] + parts[0]
                price_text = price.strip()
            except Exception as e:
                pass
        item = {
            'url': url,
            'title': title_text,
            'price': price_text,
            'image': image_text,
            'details': details_text,
        }
        print(item)
        data.append(item)
    except Exception as e:
        print(f"{url} not available")

print(f"count: {count}, time: {time.time() - start_time}")
browser.close()

json_object = json.dumps(data, indent=4)
with open('out.json', 'w') as f:
    f.write(json_object)

print(time_data)