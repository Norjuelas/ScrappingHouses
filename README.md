# Airbnb Scraper

This project is a Python-based Airbnb scraper that allows you to extract listing information without using the official Airbnb API. The scraper retrieves key details from each listing, such as location, price, review count, and more.

## Features

- **Property data extraction:** Retrieves information like location, price, property type, review count, and availability.
- **Handles multiple requests:** Implements techniques to avoid being blocked, such as user-agent rotation and proxy handling.
- **Optimized speed:** Efficient scraping, obtaining up to 100 data points every 2 minutes without being banned.
- **Headless execution:** Runs in headless mode, enabling execution on servers without a graphical interface.
- **CSV export:** Saves extracted data to a CSV file for easy analysis and manipulation.

## Requirements

- Python 3.x
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Pandas](https://pandas.pydata.org/)
- A compatible web browser (Chrome or Firefox) and its respective driver (ChromeDriver or GeckoDriver)

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/Norjuelas/airbnb-scraper.git
    ```

2. Navigate to the project directory:

    ```bash
    cd airbnb-scraper
    ```

3. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Download the browser driver (ChromeDriver or GeckoDriver) and ensure it is in your system’s PATH or place it in the project directory.

## Usage

1. Edit the `config.yaml` file to set the search parameters you want (location, price range, etc.).
2. Run the scraping script:

    ```bash
    python airbnb_scraper.py
    ```

3. The results will be saved in a CSV file named `airbnb_listings.csv` in the project directory.

## Configuration

In the `config.yaml` file, you can customize the following parameters:

- **Location:** Define the city or region where you want to scrape.
- **Price range:** Set a minimum and maximum price range.
- **Number of results:** Set how many properties you want to fetch per search.

```yaml
location: "Bogotá"
min_price: 50
max_price: 300
results_limit: 100
```

#File Structure
-[airbnb_scraper.py:] The main script that performs the scraping.
-[config.yaml]: Configuration file where you define the search parameters.
-[requirements.txt]: A list of dependencies required to run the project.
-[airbnb_listings.csv]: The output file containing the scraped property listings.

#Contributions
Contributions are welcome! If you’d like to contribute, please open an issue or a pull request in the repository.

#License
This project is licensed under the MIT License.
