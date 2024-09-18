# tests/test_scraper.py

import unittest
from src.scraper import AirbnbScraper
from dataExtractor.extractor import extract_next_links

class TestAirbnbScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = AirbnbScraper(headless=True)
    
    def test_extract_next_links(self):
        links = extract_next_links()
        self.assertIsInstance(links, list)
        self.assertGreater(len(links), 0)
    
    def tearDown(self):
        self.scraper.driver.quit()

if __name__ == '__main__':
    unittest.main()
