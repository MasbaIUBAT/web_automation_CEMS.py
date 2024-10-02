import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def seo_check(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the website is reachable
        soup = BeautifulSoup(response.text, 'html.parser')

        # SEO Check for meta description and title tag
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        title_tag = soup.find('title')
        if meta_desc and meta_desc.get('content'):
            print(f"✅ Meta description found in {url}: {meta_desc.get('content')}")
        else:
            print(f"⚠️ Meta description missing in {url}")

        if title_tag:
            print(f"✅ Title tag found in {url}: {title_tag.text}")
        else:
            print(f"⚠️ Title tag missing in {url}")

        # Check viewport tag for mobile-friendliness
        viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
        if viewport_tag and viewport_tag.get('content'):
            print(f"✅ Viewport tag found in {url}: {viewport_tag['content']}")
        else:
            print(f"⚠️ Viewport tag missing in {url} - important for mobile responsiveness.")

        # Check for structured data (e.g., JSON-LD)
        structured_data = soup.find('script', type='application/ld+json')
        if structured_data:
            print(f"✅ Structured data found in {url}: {structured_data.string[:100]}...")  # Show first 100 chars
        else:
            print(f"⚠️ Structured data missing in {url} - helps search engines understand content.")

        # Check for broken links
        links = soup.find_all('a')
        broken_links = []
        for link in links:
            link_url = link.get('href')
            if link_url and link_url.startswith('http'):
                link_response = requests.get(link_url, timeout=10)
                if link_response.status_code != 200:
                    broken_links.append(link_url)

        if broken_links:
            print(f"🔴 Broken Links in {url}:")
            for link in broken_links:
                print(f"  - {link}")
        else:
            print(f"🟢 All links in {url} are working correctly.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing {url}: {e}")

# Specify the website to check
website_to_check = "https://cems-solarexpo.com"

# Perform SEO checks
seo_check(website_to_check)
