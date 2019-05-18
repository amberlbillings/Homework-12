from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all(class_='content_title')[0].text
    news_p = soup.find_all(class_='article_teaser_body')[0].text

    # JPL Mars Space Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_string = soup.find(class_='carousel_item')['style']
    new_img_string = image_string.replace("background-image: url('","")
    image_url = new_img_string.replace("');","")
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url

    # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find_all(class_='TweetTextSize')[0].text
    mars_weather = mars_weather.replace('\n', '')

    # Mars Facts
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)

    df = tables[0]
    df.columns = ['Parameter', 'Measure']
    df = df.set_index('Parameter', drop=True)

    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    # Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []

    for x in range(4):
        links = browser.find_link_by_partial_text('Enhanced')
        links[x].click()
        time.sleep(2)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(class_='title').text
        img_url = soup.find(class_='downloads').find('a')['href']
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        browser.back()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_data
