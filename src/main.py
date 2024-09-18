
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from  dataExtractor import extractor

# Set up the WebDriver
driver = webdriver.Firefox()
os.system("clear")

# Marcar el tiempo de inicio
start_time = time.time()

try:
    # Open the main webpage
    driver.get("https://www.airbnb.com.co/s/Bogot%C3%A1--Colombia/homes")
    
    # Wait for the page to load completely
    extractor.wait_for_page_load(driver, 3)
    
    # Extraer los primeros enlaces de los botones de la página principal
    starting_links = extractor.extract_next_links()
    print(f"Enlaces iniciales extraídos: {starting_links}")

    # Navegar y extraer datos en grupos de pestañas
    master_df = extractor.extract_data_in_groups(starting_links, group_size=3, max_pages=15)

    # Mostrar el DataFrame acumulado
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', 20)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    print("\nDatos acumulados:")
    print(master_df)

    # Mostrar las dimensiones del DataFrame
    print(f"\nDimensiones del DataFrame: {master_df.shape}")

    # Identificar datos duplicados (duplicados completos)
    duplicates = master_df[master_df.duplicated()]
    num_duplicates = duplicates.shape[0]
    print(f"\nDatos duplicados encontrados: {num_duplicates}")

    # Exportar a CSV
    output_filename = "airbnb_listings.csv"
    master_df.to_csv(output_filename, index=False)

    # Mostrar la ruta del archivo CSV
    file_path = os.path.join(os.getcwd(), output_filename)
    print(f"\nDatos exportados a: {file_path}")

finally:
    driver.quit()

    # Calcular y mostrar el tiempo total transcurrido
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTiempo total de ejecución: {elapsed_time:.2f} segundos")
"""
# src/main.py

from scraper import AirbnbScraper
from dataExtractor.extractor import extract_next_links

def main():
    url = "https://www.airbnb.com.co/s/Bogot%C3%A1--Colombia/homes"
    starting_links = extract_next_links()
    
    scraper = AirbnbScraper(headless=True)
    scraper.scrape(url, starting_links, group_size=3, max_pages=15)

if __name__ == "__main__":
    main()
