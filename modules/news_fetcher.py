import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

def scrape_agriculture_news(base_url, max_pages=5, use_original_logic=False, language="en"):
    """
    Scrape agriculture news from a given base URL.

    Args:
        base_url (str): The base URL to start scraping from.
        max_pages (int): Maximum number of pages to scrape.
        use_original_logic (bool): If True, uses the original logic (for Indian Express).
        language (str): "en" for English or "mr" for Marathi.

    Returns:
        list: List of valid news article URLs.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': base_url,
        'Accept-Language': 'en-US,en;q=0.9',
    }

    agriculture_news_urls = []

    try:
        response = requests.get(base_url, headers=headers, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        if use_original_logic:
            # Using the original method for Indian Express
            news_links = soup.find_all('a', href=True, text=lambda text: text and ('agriculture' in text.lower() or 'farming' in text.lower()))
        else:
            # Using the improved method for other sites
            news_links = soup.find_all('a', href=True, string=lambda text: text and ('agriculture' in text.lower() or 'farming' in text.lower()))

        for link in news_links[:max_pages]:
            full_url = urljoin(base_url, link['href'])
            if full_url not in agriculture_news_urls:
                agriculture_news_urls.append(full_url)

        return agriculture_news_urls

    except requests.exceptions.RequestException as e:
        if language == "mr":
            print(f"{base_url} वरून स्क्रॅप करताना त्रुटी: {e}")
        else:
            print(f"Error scraping {base_url}: {e}")
        return []

def extract_news_details(news_urls, language="en"):
    """
    Extracts titles and descriptions from the given news URLs.

    Args:
        news_urls (list): List of news article URLs.
        language (str): "en" for English or "mr" for Marathi.

    Returns:
        tuple: A tuple containing two lists - one for titles and another for descriptions.
    """
    titles = []
    descriptions = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in news_urls:
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.text.strip()
            else:
                title = "No Title Found" if language == "en" else "शिर्षक सापडले नाही"
            titles.append(title)

            # Extract description (from meta tag)
            description_tag = soup.find('meta', attrs={'name': 'description'})
            if description_tag and 'content' in description_tag.attrs:
                description = description_tag['content'].strip()
            else:
                description = "No Description Found" if language == "en" else "वर्णन सापडले नाही"
            descriptions.append(description)

        except requests.exceptions.RequestException as e:
            if language == "mr":
                titles.append("शिर्षक प्राप्त करताना त्रुटी")
                descriptions.append("वर्णन प्राप्त करताना त्रुटी")
                print(f"{url} साठी डेटा प्राप्त करताना त्रुटी: {e}")
            else:
                titles.append("Error Fetching Title")
                descriptions.append("Error Fetching Description")
                print(f"Error fetching {url}: {e}")

    return titles, descriptions

def save_news_to_csv_pandas(news_urls, titles, descriptions, filename="./assets/agriculture_news.csv", language="en"):
    """
    Saves news data (URLs, Titles, and Descriptions) to a CSV file using pandas.

    Args:
        news_urls (list): List of news article URLs.
        titles (list): List of news titles.
        descriptions (list): List of news descriptions.
        filename (str): Name of the CSV file (default: "agriculture_news.csv").
        language (str): "en" for English or "mr" for Marathi.
    """
    # Create a DataFrame
    df = pd.DataFrame({
        "Link": news_urls,
        "Title": titles,
        "Desc": descriptions
    })

    # Save to CSV
    df.to_csv(filename, index=False, encoding="utf-8")

    if language == "mr":
        print(f"बातम्या यशस्वीरित्या {filename} मध्ये जतन केल्या.")
    else:
        print(f"News data saved successfully to {filename}.")

def scrapper(language="en"):
    """
    Collects agriculture news from multiple sites, extracts details, and saves them to a CSV file.

    Args:
        language (str): "en" for English or "mr" for Marathi.
    """
    # List of agriculture news sites
    AGRICULTURE_NEWS_SITES = [
        'https://www.modernfarmer.com/',
        'https://www.livemint.com/industry/agriculture',
        'https://www.thehindu.com/topic/Agriculture/',
        'https://www.business-standard.com/industry/agriculture',
        'https://www.thehindubusinessline.com/economy/agri-business/',
        'https://icar.org.in/news-highlights',
        'https://indianexpress.com/about/agriculture/'
    ]

    # Collect news URLs
    all_agriculture_news_urls = []

    for site in AGRICULTURE_NEWS_SITES:
        news_urls = scrape_agriculture_news(site, use_original_logic=(site == 'https://indianexpress.com/about/agriculture/'), language=language)
        all_agriculture_news_urls.extend(news_urls)

    # Filter out URLs that are from the agriculture news sites
    filtered_news_urls = [url for url in all_agriculture_news_urls if not any(site in url for site in AGRICULTURE_NEWS_SITES)]

    # Extract titles and descriptions
    titles_list, descriptions_list = extract_news_details(filtered_news_urls, language=language)

    # Save to CSV using pandas
    save_news_to_csv_pandas(filtered_news_urls, titles_list, descriptions_list, language=language)
