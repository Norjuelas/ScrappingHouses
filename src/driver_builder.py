from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

import os


class driver_builder:

    def __init__(self, browser='firefox', headless=False):
        """
        Inicializa el DriverBuilder con las configuraciones necesarias.

        :param browser: Tipo de navegador ('firefox' o 'chrome').
        :param headless: Ejecutar el navegador en modo headless.
        """
        self.browser = browser.lower()
        self.headless = headless
        self.driver = None

    def _initialize_driver(self):
        """
        Inicializa el WebDriver basado en las configuraciones.
        :return: Instancia del WebDriver.
        """
        if self.browser == 'firefox':
            options = FirefoxOptions()
            if self.headless:
                options.add_argument('--headless')
            driver = webdriver.Firefox(options=options)
        elif self.browser == 'chrome':
            options = ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        else:
            raise ValueError(f"Navegador no soportado: {self.browser}. Usa 'firefox' o 'chrome'.")
        print(f"{self.browser.capitalize()} WebDriver inicializado.")
        return driver
    
    def get_driver(self):
        return self.driver

    def __enter__(self):
        self.driver = self._initialize_driver()
        return self.driver
                
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
            print("WebDriver cerrado.")
