from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from MongoConnection import collection

def Scrapper():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    base_url = 'https://www.gollo.com/c'
    driver.get(base_url)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "items"))
        )
    except:
        print("No se encontró la lista de categorías.")

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    categories = []
    for li in soup.select("div.filter-options-content ol.items li.item a"):
        category_name = li.contents[0]
        category_url = li["href"]
        if category_name in ['Promociones', 'Lo más nuevo']:
            continue

        if 'price' in category_url:
            break

        categories.append({"name": category_name, "url": category_url})

    all_data = []
    for category in categories:
        url = category["url"] + "&product_list_limit=36"
        driver.get(url)
        driver.implicitly_wait(5)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        products = soup.find_all('div', class_='product details product-item-details')

        category_data = []
        for product in products:
            try:
                product_name = product.find('a', class_='product-item-link').getText().strip()
                current_price_tag = product.find('span', {'data-price-type': 'finalPrice'})
                original_price_tag = product.find('span', {'data-price-type': 'oldPrice'})

                current_price = int(current_price_tag['data-price-amount']) if current_price_tag else None
                original_price = int(original_price_tag['data-price-amount']) if original_price_tag else current_price
                discount = round(100 - ((current_price / original_price) * 100), 2) if original_price else 0

                product_data = {
                    'CATEGORIA': category["name"],
                    'PRODUCTO': product_name,
                    'PRECIO_ACTUAL': current_price,
                    'PRECIO_ORIGINAL': original_price,
                    'PERC_DESCUENTO': discount
                }
                category_data.append(product_data)
                all_data.append(product_data)
            except Exception as e:
                print(f"Error al procesar producto: {e}")

        # Guardar CSV por categoría
        df_category = pd.DataFrame(category_data)
        df_category.to_csv(f"output/raw_data_{category['name'].replace(' ', '_')}.csv", encoding='utf-8', index=False)

    # Guardar archivo general
    df_all = pd.DataFrame(all_data)
    df_all.to_csv(f"output/raw_data.csv", encoding='utf-8', index=False)
    df_all.to_excel(f"output/raw_data.xlsx", index=False )

    # Guardar en MongoDB
    if all_data:
        collection.insert_many(all_data)

    driver.quit()
    print("Scraping completado.")
    return df_all 
