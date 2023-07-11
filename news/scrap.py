"""
this file is used to scrap the news from websites,
there are a function for each website
- CoinTelegraph
"""

import requests
import re
from bs4 import BeautifulSoup

from news.New import New


def get_coin_telegraph_news():
    url = "https://cointelegraph.com/tags/nft"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 '
                                                        'Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                                                    'image/avif,image/webp,*/*;q=0.8',
                                          'Referer': 'https://cointelegraph.com'})
    soup = BeautifulSoup(response.text, "html.parser")
    # All news are in li with class "posts-listing__item"
    news = soup.find_all("li", class_="posts-listing__item")
    for new in news:
        # get title on span class "post-card-inline__title"
        title = new.find("span", class_="post-card-inline__title").text
        title = re.sub(r"^\s", "", title)
        # get url on a class "post-card-inline__figure-link"
        url = "https://cointelegraph.com" + new.find("a", class_="post-card-inline__figure-link")["href"]
        try:
            # get image url on img class "lazy-image__img"
            image_url = new.find("img", class_="lazy-image__img")["src"]  # TODO: FIX THIS, IMAGE URL NEVER EXISTS
        except TypeError:
            image_url = "No image"
        # get summary on p class "post-card-inline__text"
        summary = new.find("p", class_="post-card-inline__text").text
        # get category on span class "post-card-inline__badge post-card-inline__badge_default"
        try:
            category = new.find("span", class_="post-card-inline__badge post-card-inline__badge_default").text
            category = re.sub(r"^\s", "", category)
        except AttributeError:
            try:
                category = new.find("span", class_="post-card-inline__badge post-card-inline__badge_info").text
                category = re.sub(r"^\s", "", category)
            except AttributeError:
                try:
                    category = new.find("span", class_="post-card-inline__badge post-card-inline__badge_success").text
                    category = re.sub(r"^\s", "", category)
                except AttributeError:
                    try:
                        category = new.find("span", class_="post-card-inline__badge post-card-inline__badge_").text
                        category = re.sub(r"^\s", "", category)
                    except AttributeError:
                        category = "News"

        # Create news object
        n = New(title, url, image_url, summary, category)
        # Print news
        print(n.__str__())
        print("--------------------------------------------------")
        # TODO: Save news in database


if __name__ == '__main__':
    get_coin_telegraph_news()
