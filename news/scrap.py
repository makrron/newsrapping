"""
this file is used to scrap the news from websites,
there are a function for each website
- CoinTelegraph
"""

import requests
import re
from bs4 import BeautifulSoup

from news.New import New


def get_coin_telegraph_news(tag):
    """
    This function get the news from CoinTelegraph
    :param tag: Tag to search in CoinTelegraph
    :return:
    """
    url = "https://cointelegraph.com/tags/" + tag
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
            print(image_url)
        except TypeError:
            image_url = "No image"
        # get summary on p class "post-card-inline__text"
        summary = new.find("p", class_="post-card-inline__text").text
        # expresion regular para borrar dobles espacios
        summary = re.sub(r"^\s", "", summary)
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
                        category = "Crypto News"

        # Create news object
        n = New(title, url, image_url, summary, category, date=None)
        # Print news
        print(n.__str__())
        print("--------------------------------------------------")
        # TODO: Save news in database


def get_coinpedia_news():
    """
    This function get the news from CoinPedia
    :return:
    """
    url = "https://coinpedia.org/news/"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 '
                                                        'Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                                                    'image/avif,image/webp,*/*;q=0.8'})
    soup = BeautifulSoup(response.text, "html.parser")
    # All news are in ul with class "posts-items"
    news = soup.find_all("ul", class_="posts-items")
    # divide news in li
    news = news[0].find_all("li")
    for new in news:
        # get title on h2 class "post-title"
        title = new.find("h2", class_="post-title").text
        title = re.sub(r"^\s", "", title)
        # get url on a class "post-thumb" and href
        url = new.find("a", class_="post-thumb")["href"]
        # get image url on img class "attachment-jannah-image-large size-jannah-image-large wp-post-image entered
        # lazyloaded"
        image_url = new.find("img")["data-lazy-src"]
        # get summary on p class "post-excerpt"
        summary = new.find("p", class_="post-excerpt").text
        summary = re.sub(r"^\s", "", summary)
        # get category on div class "tag_hash_display" and span
        category_aux = new.find("div", class_="tag_hash_display").find_all("span")
        category = ""
        for cat in category_aux:
            category = category + cat.text + " "
        category = re.sub(r"^\s", "", category)
        # get date on span class "date meta-item tie-icon"
        date = new.find("span", class_="date meta-item tie-icon").text
        # Create news object
        n = New(title, url, image_url, summary, category, date)
        # Print news
        print(n.__str__())
        print("------------------------------------")
        # TODO: Save news in database


def get_ambcrypto_news():
    """
    This function get the news from AmbCrypto
    :return:
    """
    url = "https://ambcrypto.com/category/new-news/"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 '
                                                        'Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                                                    'image/avif,image/webp,*/*;q=0.8'})
    soup = BeautifulSoup(response.text, "html.parser")
    # News are on ul class "home-posts infinite-content"
    news = soup.find_all("ul", class_="home-posts infinite-content")
    # divide news in li
    news = news[0].find_all("li")
    for new in news:
        # get image url on img data-lazy-src
        image_url = new.find("img")["data-lazy-src"]
        # get news url on a href in div class "home-post-image"
        url = new.find("div", class_="home-post-image").find("a")["href"]
        # get title on h2 into div class "home-post-content"
        title = new.find("div", class_="home-post-content").find("h2").text
        # get category on a class "mvp-cd-cat left relative"
        category = new.find("a", class_="mvp-cd-cat left relative").text
        # Create news object
        n = New(title, url, image_url, summary=None, date=None, category=category)
        # Print news
        print(n.__str__())
        print("------------------------------------")


def get_cryptopolitan_news(url):
    """
    This function get the news from Cryptopolitan
    :param url: Url to get news from different categories from Cryptopolitan
    :return:
    """
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) '
                                                        'Gecko/20100101 Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/'
                                                    'xml;q=0.9,image/avif,image/webp,*/*;q=0.8'})
    soup = BeautifulSoup(response.text, "html.parser")
    # News are in article
    news = soup.find_all("article")
    for new in news:
        # get image on img class "grid-image ls-is-cached lazyloaded"
        try:
            image_url = new.find("img")["data-src"]
        except TypeError:
            image_url = None
        # get url on a class "grid-image-holder"
        try:
            url = new.find("a", class_="grid-image-holder")["href"]
        except TypeError:
            url = None
        # get title on h3 class "cp-post-title"
        try:
            title = new.find("h3", class_="cp-post-title").text
            title = re.sub(r"^\s", "", title)
            title = re.sub(r"^\n", "", title)
        except TypeError:
            title = None
        # get summary on p class "cp-excerpt"
        try:
            summary = new.find("p", class_="cp-excerpt").text
        except:
            summary = None
        # get category on div class "cat-container"
        try:
            category = new.find("div", class_="cat-container").text
        except:
            category = None
        # get date on first span into div class "cp-post-meta"
        try:
            date = new.find("div", class_="cp-post-meta").find("span").text
        except TypeError:
            date = None
        if url is not None and title is not None:
            n = New(title, url, image_url, summary, category, date)
            # Print news
            print(n.__str__())
            print("------------------------------------")
            # TODO: Save news in database


if __name__ == '__main__':
    """
    get_cryptopolitan_news("https://www.cryptopolitan.com/news/")
    get_cryptopolitan_news("https://www.cryptopolitan.com/price-prediction/")
    get_cryptopolitan_news("https://www.cryptopolitan.com/guides/")
    get_cryptopolitan_news("https://www.cryptopolitan.com/news/regulation/")
    get_cryptopolitan_news("https://www.cryptopolitan.com/news/research/")
    get_cryptopolitan_news("https://www.cryptopolitan.com/news/scam/")
    get_cryptopolitan_news("https://www.cryptopolitan.com/technology/")
    get_ambcrypto_news()
    get_coinpedia_news()
    get_coin_telegraph_news("bitcoin")
    get_coin_telegraph_news("ethereum")
    get_coin_telegraph_news("altcoin")
    get_coin_telegraph_news("blockchain")
    get_coin_telegraph_news("business")
    get_coin_telegraph_news("regulation")
    get_coin_telegraph_news("nft")
    get_coin_telegraph_news("defi")
    get_coin_telegraph_news("adoption")
    """
