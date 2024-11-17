import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrape_whatsapp_data(base_url, scrape_type, limit):
    visited = set()
    results = []

    def explore_page(url):
        if url in visited or len(results) >= limit:
            return
        visited.add(url)

        try:
            # Fetch the webpage
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Scrape the specific data
            if scrape_type == "group_links":
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    if 'chat.whatsapp.com' in href:
                        full_url = urljoin(base_url, href)
                        if full_url not in results:
                            print(f"Found: {full_url}")
                            results.append(full_url)
                            if len(results) >= limit:
                                return

            elif scrape_type == "phone_links":
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    if 'wa.me' in href:
                        full_url = urljoin(base_url, href)
                        if full_url not in results:
                            print(f"Found: {full_url}")
                            results.append(full_url)
                            if len(results) >= limit:
                                return

            # Explore links within the same domain
            for a_tag in soup.find_all('a', href=True):
                href = urljoin(base_url, a_tag['href'])
                if urlparse(base_url).netloc == urlparse(href).netloc:
                    explore_page(href)

        except Exception as e:
            print(f"Error processing {url}: {e}")

    # Start exploration from the base URL
    explore_page(base_url)
    return results

# Main Program
if __name__ == "__main__":
    print("What do you want to scrape?")
    print("1. WhatsApp Group Links (chat.whatsapp.com)")
    print("2. WhatsApp Phone Links (wa.me)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        scrape_type = "group_links"
    elif choice == "2":
        scrape_type = "phone_links"
    else:
        print("Invalid choice. Exiting.")
        exit()

    website_url = input("Enter the website URL to scrape: ").strip()
    limit = int(input("Enter the maximum number of results to scrape: ").strip())
    output_file = input("Enter the filename to save results (e.g., output.txt): ").strip()

    # Scrape data
    scraped_data = scrape_whatsapp_data(website_url, scrape_type, limit)

    # Save to file
    with open(output_file, "w") as file:
        for item in scraped_data:
            file.write(item + "\n")

    print(f"\nScraping complete. Results saved to {output_file}.")
