from bs4 import BeautifulSoup
import requests
import re
import threading


DOMAIN = "[url of enrolled course]"
URL_AUTOMOBILES = "[url of enrolled course]"

LINKS = []
PHONES = []

def make_request(url):
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.text
        else:
            print("\tError: Unable to reach the server!")
            return None

    except Exception as error:
        print("\tError making request!")
        print(error)
        return None

def parse_html(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        return soup
    
    except Exception as error:
        print("\tError parsing HTML!")
        print(error)
        return None

def find_links(soup_obj):
    try:
        container = soup_obj.find("div", class_="ui three doubling link cards")
        cards = container.find_all("a")
    except Exception:
        print("Error: Could not find link container.") 
        return []

    found_links = []
    for card in cards:
        try: 
            link = card["href"]
            found_links.append(link)
        except KeyError:
            pass
    
    return found_links

def find_phones(soup_obj):
    try:
        description = soup_obj.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
    except Exception:
        print("Error: Description not found!")
        return None

    phones_found = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", description)

    if phones_found:
        return phones_found

def discover_phones():
    while True:
        try:
            link = LINKS.pop(0)
        except IndexError:
            return None

        ad_html = make_request(DOMAIN + link)

        if ad_html:
            ad_soup = parse_html(ad_html)

            if ad_soup:
                found_list = find_phones(ad_soup)

                if found_list:
                    for phone in found_list:
                        PHONES.append(phone)

def save_phones(phone_list):
    try:
        with open("phones.csv", "a") as file:
            for phone in phone_list:
                formatted_phone = "{}{}{}\n".format(phone[0], phone[1], phone[2])
                file.write(formatted_phone)
        print("File saved successfully!")

    except Exception as error:
        print("Error saving file!")
        print(error)

if __name__ == "__main__":
    print("Starting crawler...")
    main_page_html = make_request(URL_AUTOMOBILES)

    if main_page_html:
        main_soup = parse_html(main_page_html)

        if main_soup:
            LINKS = find_links(main_soup)
            print(f"Found {len(LINKS)} links. Starting threads...")

            THREADS = []
            for _ in range(10):
                t = threading.Thread(target=discover_phones)
                THREADS.append(t)

            for t in THREADS:
                t.start()

            for t in THREADS:
                t.join()

            print(f"Extraction finished. Saving {len(PHONES)} entries...")
            save_phones(PHONES)
