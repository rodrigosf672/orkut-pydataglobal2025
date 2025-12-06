"""
Orkut community scraper.

This script walks archived Orkut pages on the Wayback Machine and collects
visible community names into a flat list.

Use it gently and at your own risk:
- It is provided for research and demonstration only.
- You are responsible for following the Internet Archive terms of use,
  robots policies, and any laws or institutional guidelines that apply to you.
- I am not liable for how you run, modify, or reuse this code.

Results are saved as a UTF-8 CSV file (orkut_communities.csv) because CSV is:
- Easy to inspect in spreadsheets, text editors, and notebooks.
- Portable across languages and environments for downstream analysis.

In most cases you do not need to run this scraper. Unless you want to
reproduce the archival process from scratch, you can skip this file and
start directly from the provided orkut_communities.csv.
"""

import requests
from bs4 import BeautifulSoup
import time
import csv
from urllib.parse import urljoin, urlparse

class OrkutCommunityScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.communities = []
        
    def get_page(self, url):
        """Fetch a page with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_communities_from_page(self, soup):
        """Extract community names from a page"""
        communities = []
        
        # Look for community links with the specific class
        community_links = soup.find_all('a', class_='typoSectionTitleFont')
        for link in community_links:
            name = link.get_text(strip=True)
            if name and len(name) > 2:
                communities.append(name)
        
        # Fallback: Look for community container
        if not communities:
            community_container = soup.find('div', class_='listCommunityContainer')
            if community_container:
                # Find all community links within the container
                all_links = community_container.find_all('a')
                for link in all_links:
                    # Skip pagination links
                    if 'paginationSeparator' in link.get('class', []):
                        continue
                        
                    name = link.get_text(strip=True)
                    if name and len(name) > 2 and name not in ['next >', '< previous', 'first', 'last']:
                        communities.append(name)
        
        # Fallback: Look for various patterns that might contain community names
        if not communities:
            selectors = [
                'a[href*="Community"]',
                'a[href*="community"]',
                '.community-name',
                '.community-title',
                'a[title*="community"]',
                'a[title*="Community"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    name = element.get_text(strip=True)
                    if name and len(name) > 2:
                        communities.append(name)
        
        return list(set(communities))  # Remove duplicates
    
    def find_index_letter_links(self, soup):
        """Find index letter links (A, B, C, etc.)"""
        links = []
        
        # Look for index letter links
        index_container = soup.find('div', class_='indexLettersContainer')
        if index_container:
            for link in index_container.find_all('a', class_='indexLetters'):
                href = link.get('href')
                if href:
                    full_url = urljoin(self.base_url, href)
                    links.append(full_url)
        
        return links
    
    def find_pagination_links(self, soup):
        """Find pagination links (next page)"""
        links = []
        
        # Look for pagination links
        pagination_links = soup.find_all('a', class_='paginationSeparator')
        for link in pagination_links:
            href = link.get('href')
            if href and 'next' in link.get_text().lower():
                full_url = urljoin(self.base_url, href)
                links.append(full_url)
        
        return links
    
    def scrape_letter_page(self, letter_url, letter):
        """Scrape all communities from a letter page and its pagination"""
        page_num = 1
        current_url = letter_url
        letter_communities = []
        
        while current_url:
            print(f"  Scraping {letter} - page {page_num}: {current_url}")
            
            response = self.get_page(current_url)
            if not response:
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            page_communities = self.extract_communities_from_page(soup)
            letter_communities.extend(page_communities)
            
            print(f"    Found {len(page_communities)} communities on this page")
            
            # Look for next page link
            next_links = self.find_pagination_links(soup)
            current_url = next_links[0] if next_links else None
            
            page_num += 1
            time.sleep(1)  # Be respectful to the server
            
            # Safety limit to avoid infinite loops
            if page_num > 50:
                print(f"    Reached page limit for letter {letter}")
                break
        
        return letter_communities
    
    def scrape_communities(self):
        """Main scraping method"""
        print(f"Starting to scrape communities from: {self.base_url}")
        
        # Get the main page
        response = self.get_page(self.base_url)
        if not response:
            print("Failed to fetch the main page")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find index letter links
        index_links = self.find_index_letter_links(soup)
        print(f"Found {len(index_links)} index letter links")
        
        if not index_links:
            print("No index letter links found. Trying to extract from main page...")
            main_communities = self.extract_communities_from_page(soup)
            self.communities.extend(main_communities)
            print(f"Found {len(main_communities)} communities on main page")
            return
        
        # Scrape each letter page
        for i, link in enumerate(index_links):
            letter = link.split('l-')[-1].split('.')[0] if 'l-' in link else f"page_{i+1}"
            print(f"\nScraping letter {letter} ({i+1}/{len(index_links)})")
            
            letter_communities = self.scrape_letter_page(link, letter)
            self.communities.extend(letter_communities)
            
            print(f"Total communities found for {letter}: {len(letter_communities)}")
            
            # Be respectful to the server
            time.sleep(2)
        
        # Remove duplicates and clean up
        self.communities = list(set(self.communities))
        self.communities = [name for name in self.communities if len(name.strip()) > 2]
        
        print(f"\nTotal unique communities found: {len(self.communities)}")
        
    def save_to_csv(self, filename='orkut_communities.csv'):
        """Save communities to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Community Name'])
            for community in sorted(self.communities):
                writer.writerow([community])
        print(f"Communities saved to {filename}")
    
    def print_communities(self):
        """Print all found communities"""
        print("\n=== ORKUT COMMUNITIES ===")
        for i, community in enumerate(sorted(self.communities), 1):
            print(f"{i:3d}. {community}")

def main():
    url = "https://web.archive.org/web/20141001005309/http://orkut.google.com/"
    
    scraper = OrkutCommunityScraper(url)
    scraper.scrape_communities()
    
    # Display results
    scraper.print_communities()
    
    # Save to CSV
    scraper.save_to_csv()
    
    print(f"\nScraping completed! Found {len(scraper.communities)} unique communities.")

if __name__ == "__main__":
    main()