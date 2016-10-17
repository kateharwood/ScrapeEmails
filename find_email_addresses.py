import urllib
from bs4 import BeautifulSoup
import re
import sys

def find_internal_urls(url, orig_url, depth=0, max_depth=2):
    page = urllib.urlopen(url)
    pageHtml = page.read()
    soup = BeautifulSoup("".join(pageHtml))
    all_page_urls = []
    a_tags = soup.findAll("a", href=True)

    if depth > max_depth:
        return []
    else:
        for a_tag in a_tags:
            if "http" not in a_tag["href"] and "/" in a_tag["href"] or "mailto" in a_tag["href"]:
                if orig_url == "http://www.jana.com":
                    if a_tag['href'] != "/":
                        url = "http:" + a_tag['href']
                else:
                    if a_tag['href'] != "/":
                        url = orig_url + a_tag['href']
            elif "http" in a_tag["href"]:
                url = a_tag["href"]
            all_page_urls.append(url)
    return all_page_urls

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Program takes one argument: the website you want to scrape (ex: waynflete.org)"
    else:
        user_url = sys.argv[1]
        user_url = "http://www." + user_url
        all_urls = find_internal_urls(user_url, user_url)
        email_list = []
        for url in all_urls:
            f = urllib.urlopen(url)
            s = f.read()
            emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)
            for email in emails:
                if email not in email_list:
                    email_list.append(email)
        print "Found these email addresses:"  
        for email in email_list:
            print email