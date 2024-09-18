# src/scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import os
import time

from dataExtractor import extractor

class AirbnbScraper:
    def __init__(self, driver_path='geckodriver', headless=False):
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options, executable_path=driver_path)
        os.system("clear")
        self.start_time = time.time()

    def wait_for_page_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

    def scrape(self, url, starting_links, group_size=3, max_pages=15):
        try:
            self.driver.get(url)
            self.wait_for_page_load()

            print(f"Enlaces iniciales extraídos: {starting_links}")

            master_df = extractor.extract_data_in_groups(
                starting_links, group_size=group_size, max_pages=max_pages
            )

            print("\nDatos acumulados:")
            print(master_df)

            print(f"\nDimensiones del DataFrame: {master_df.shape}")

            duplicates = master_df[master_df.duplicated()]
            num_duplicates = duplicates.shape[0]
            print(f"\nDatos duplicados encontrados: {num_duplicates}")

            output_filename = "airbnb_listings.csv"
            master_df.to_csv(output_filename, index=False)

            file_path = os.path.join(os.getcwd(), output_filename)
            print(f"\nDatos exportados a: {file_path}")

        except Exception as e:
            print(f"Error durante el scraping: {e}")

        finally:
            self.driver.quit()
            elapsed_time = time.time() - self.start_time
            print(f"\nTiempo total de ejecución: {elapsed_time:.2f} segundos")
