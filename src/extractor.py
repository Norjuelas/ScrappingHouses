from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# Function to wait for a specific amount of time
def wait_for_page_load(driver, seconds):
    time.sleep(seconds)

# Function to extract the data from the cards on the current page
def extract_listings():
    cards_data = []
    cards = driver.find_elements(By.CLASS_NAME, "cy5jw6o")
    for card in cards:
        try:
            link_component = card.find_element(By.CLASS_NAME, "bn2bl2p")
            location = card.find_element(By.CLASS_NAME, "t1jojoys")
            description = card.find_element(By.CLASS_NAME, "s1cjsi4j")
            image = card.find_element(By.CLASS_NAME, "itu7ddv")
            price = card.find_element(By.CLASS_NAME, "pquyp1l")
            rating = card.find_element(By.CLASS_NAME, "r4a59j5")

            data = {
                "link": link_component.get_attribute("href"),
                "location": location.text,
                "description": description.text,
                "image": image.get_attribute("src"),
                "price": price.text,
                "rating": rating.text
            }

            cards_data.append(data)

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error al extraer un card: {e}")
            continue
    return cards_data

#@Function to extract links for the next set of pages from the current page
def extract_next_links():
    try:
        wait = WebDriverWait(driver, 10)
        buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c1ackr0h")))
        links = [button.get_attribute("href") for button in buttons if button.get_attribute("href")]
        return links
    except Exception as e:
        print(f"Error al extraer los enlaces: {e}")
        return []

def extract_data_in_groups(starting_links, group_size=3, max_pages=15):
    # DataFrame acumulador grande
    master_df = pd.DataFrame()

    # Inicializar con los primeros enlaces
    links_to_process = starting_links
    page_count = 0

    while links_to_process and page_count < max_pages:
        # Abrir el grupo de pestañas en una iteración
        for link in links_to_process[:group_size]:
            driver.execute_script(f"window.open('{link}', '_blank');")
            wait_for_page_load(driver, 3)

        # Procesar las pestañas abiertas y extraer datos de la última
        for j in range(len(driver.window_handles) - 1, 0, -1):
            driver.switch_to.window(driver.window_handles[j])
            wait_for_page_load(driver, 3)

            # Extraer los datos de la pestaña actual
            cards_data = extract_listings()
            print(f"Datos extraídos de la pestaña {j}: {len(cards_data)} cards")

            if cards_data:
                df_current = pd.DataFrame(cards_data)
                master_df = pd.concat([master_df, df_current], ignore_index=True)

            # Al llegar a la última pestaña del grupo, buscar nuevos enlaces para el siguiente grupo
            if j == 1:
                new_links = extract_next_links()
                print(f"Enlaces extraídos de la pestaña {j}: {new_links}")

                # Agregar los nuevos enlaces a procesar en la siguiente iteración
                links_to_process = new_links

            # Cerrar la pestaña actual
            driver.close()

            # Incrementar el contador de páginas procesadas
            page_count += 1
            if page_count >= max_pages:
                break

        # Volver a la pestaña principal
        driver.switch_to.window(driver.window_handles[0])

    return master_df

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait_for_page_load(driver, 3)

