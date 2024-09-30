# airbnb_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time
import os
from bs4 import BeautifulSoup


class AirbnbScraper:
    def __init__(self, base_url):
        """
        Inicializa el scraper con las configuraciones necesarias.

        :param base_url: URL principal para iniciar el scraping.
        """

        self.driver = webdriver.Firefox()
        self.base_url = base_url
        self.master_df = pd.DataFrame()
        print("WebDriver inicializado.")

    def wait_for_page_load(self, seconds=3):
        """Espera un tiempo específico para cargar la página."""
        time.sleep(seconds)

    def extract_listings(self):
        """Extrae los datos de las tarjetas en la página actual utilizando BeautifulSoup."""
        cards_data = []
        try:
            # Obtener el HTML de la página actual
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Encontrar todas las tarjetas de listado
            cards = soup.find_all('div', class_='cy5jw6o')
            print(f"Encontrados {len(cards)} cards en la página.")
            for card in cards:
                try:
                    link_component = card.find('a', class_='bn2bl2p')
                    location = card.find('div', class_='t1jojoys')
                    description = card.find('div', class_='s1cjsi4j')
                    image = card.find('img', class_='itu7ddv')
                    price = card.find('span', class_='pquyp1l')
                    rating = card.find('span', class_='r4a59j5')

                    data = {
                        "link": link_component['href'] if link_component else None,
                        "location": location.get_text(strip=True) if location else None,
                        "description": description.get_text(strip=True) if description else None,
                        "image": image['src'] if image else None,
                        "price": price.get_text(strip=True) if price else None,
                        "rating": rating.get_text(strip=True) if rating else None
                    }

                    cards_data.append(data)

                except Exception as e:
                    print(f"Error al extraer un card: {e}")
                    continue
        except Exception as e:
            print(f"Error al encontrar las cards: {e}")
        return cards_data

    def extract_next_links(self):
        """Extrae los enlaces para las próximas páginas desde la página actual."""
        try:
            wait = WebDriverWait(self.driver, 10)
            buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c1ackr0h")))
            links = [button.get_attribute("href") for button in buttons if button.get_attribute("href")]
            print(f"Enlaces extraídos: {links}")
            return links
        except TimeoutException:
            print("Tiempo de espera excedido al extraer enlaces.")
            return []
        except Exception as e:
            print(f"Error al extraer los enlaces: {e}")
            return []

    def scroll_to_bottom(self):
        """Desplaza la página hasta el final para cargar todo el contenido."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.wait_for_page_load()

    def extract_data_in_groups(self, starting_links, group_size=3, max_pages=15):
        """Extrae datos en grupos de pestañas."""
        links_to_process = starting_links.copy()
        page_count = 0

        while links_to_process and page_count < max_pages:
            current_group = links_to_process[:group_size]
            links_to_process = links_to_process[group_size:]

            for link in current_group:
                self.driver.execute_script(f"window.open('{link}', '_blank');")
                print(f"Abriendo nueva pestaña: {link}")
                self.wait_for_page_load()

            for handle in self.driver.window_handles[1:]:  # Ignorar la pestaña principal
                self.driver.switch_to.window(handle)
                print(f"Procesando pestaña: {self.driver.current_url}")
                self.wait_for_page_load()

                cards_data = self.extract_listings()
                print(f"Datos extraídos: {len(cards_data)} cards")
                
                if cards_data:
                    df_current = pd.DataFrame(cards_data)
                    self.master_df = pd.concat([self.master_df, df_current], ignore_index=True)

                # Extraer nuevos enlaces solo desde la última pestaña procesada
                if page_count == 0:
                    new_links = self.extract_next_links()
                    if new_links:
                        links_to_process.extend(new_links)

                self.driver.close()
                page_count += 1
                print(f"Páginas procesadas: {page_count}/{max_pages}")

                if page_count >= max_pages:
                    break

            self.driver.switch_to.window(self.driver.window_handles[0])
            print("Volviendo a la pestaña principal.")

        return self.master_df

    def save_to_csv(self, filename="airbnb_listings.csv"):
        """Guarda el DataFrame acumulado en un archivo CSV."""
        self.master_df.to_csv(filename, index=False)
        file_path = os.path.join(os.getcwd(), filename)
        print(f"Datos exportados a: {file_path}")

    def run(self, group_size=3, max_pages=15, output_filename="airbnb_listings.csv"):
        """Ejecuta el proceso completo de scraping."""
        start_time = time.time()
        try:
            # Abrir la página principal
            self.driver.get(self.base_url)
            print(f"Navegando a {self.base_url}")
            self.wait_for_page_load()

            # Extraer los primeros enlaces
            starting_links = self.extract_next_links()
            if not starting_links:
                print("No se encontraron enlaces iniciales. Terminando el scraping.")
                return

            # Extraer datos en grupos de pestañas
            self.master_df = self.extract_data_in_groups(starting_links, group_size, max_pages)

            # Mostrar información del DataFrame
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', 20)
            pd.set_option('display.width', 1000)
            pd.set_option('display.colheader_justify', 'center')
            print("\nDatos acumulados:")
            print(self.master_df)

            print(f"\nDimensiones del DataFrame: {self.master_df.shape}")

            # Identificar datos duplicados
            duplicates = self.master_df[self.master_df.duplicated()]
            num_duplicates = duplicates.shape[0]
            print(f"\nDatos duplicados encontrados: {num_duplicates}")

            # Guardar los datos en CSV
            self.save_to_csv(output_filename)

        finally:
            self.driver.quit()
            print("WebDriver cerrado.")

            # Calcular y mostrar el tiempo total transcurrido
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"\nTiempo total de ejecución: {elapsed_time:.2f} segundos")
