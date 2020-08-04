


from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import re
import pandas as pd
import os


def scrape ():
    browser = init_browser ()
    
    return {
    'mars_news': mars_news (browser),
    'mars_featured_pic': mars_featured_pic (browser),
    'mars_tweet': mars_tweet(browser),
    'mars_table':mars_table(browser),
    'mars_hemispheres': mars_hemispheres(browser)
}

def init_browser ():
    executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}

    return Browser("chrome", **executable_path, headless=False)

###MARS NEWS

def mars_news (browser):

    mars_news_final = {}

    

    mars_news_url = 'https://mars.nasa.gov/news/'

    browser.visit(mars_news_url)
    
    time.sleep(5)

    mars_html = browser.html

    soup = bs(mars_html, 'html.parser')

    recent_titles = soup.find_all("div", class_ = "content_title")

    news = []
    for i in recent_titles:
        x = i.find('a')
        news.append(x)

    most_recent_title = news[1].string
    most_recent_desc = soup.find("div",class_="article_teaser_body").text

#print(most_recent_title)
#print(most_recent_desc)

    mars_news_final['title'] = most_recent_title
    mars_news_final['description'] = most_recent_desc

    return mars_news_final


###FEATURED MARS PIC

def mars_featured_pic (browser):
    mars_pic = {}


    mars_pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    mars_pic_url_short = "https://www.jpl.nasa.gov"


    browser.visit(mars_pic_url)


    img_full = browser.find_by_id('full_image')['data-fancybox-href']

    img_url = mars_pic_url_short + img_full

#print(img_url)

    mars_pic['img'] = img_url

    return mars_pic


###MARS TWEET


def mars_tweet (browser):

   
    
    mars_weather_tweet = {}
    mars_tweet_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(mars_tweet_url)
    
    time.sleep(5)



    tweet_html = browser.html

    tweet_soup = bs(tweet_html, 'html.parser')


    tweet = tweet_soup.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")


    mars = []

    for result in tweet:
        if result.find(string=re.compile("InSight")):
            mars_weather = result.find(string=re.compile("InSight"))
            mars.append(mars_weather)



#print(mars[0])

    time.sleep(5)
    mars_weather_tweet['weather'] = mars[0]

    return mars_weather_tweet



###MARS TABLE FACTS

def mars_table(browser):




    mars_facts_html = 'https://space-facts.com/mars/'

    all_tables = pd.read_html(mars_facts_html)
        
    mars_table = (all_tables[0])
    
    mars_table.columns = ['Feature', 'Data']
            
    mars_table


# In[40]:


    mars_table_html = mars_table.to_html()

    return mars_table_html

# In[ ]:


### MARS HEMISPHERE PICS AND TITLES


def mars_hemispheres (browser):

    mars_hemis = {}


    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'



    browser.visit(astro_url)



    astro_html = browser.html

    astro_soup = bs(astro_html,'html.parser')

    items = astro_soup.find_all('div', class_='item')



    hemisphere_image_urls=[]

    products = astro_soup.find('div', class_='result-list')

    hemispheres = products.find_all('div',{'class':'item'})

    for hemisphere in hemispheres:
    
        print(hemisphere)
    
        title = hemisphere.find("h3").text
    
        title = title.replace("Enhanced", "").strip()
    
        end_link = hemisphere.find("a")["href"]
    
        image_link = 'https://astrogeology.usgs.gov' + end_link
    
        browser.visit(image_link)
    
        html_hemispheres = browser.html
    
        new_soup = bs(html_hemispheres, "html.parser")
    
        downloads = new_soup.find("div", class_="downloads").find("a")["href"]
    
    
    
        hemisphere_image_urls.append({"title": title, "img_url": downloads})
    
 
    mars_hemis = hemisphere_image_urls

    return mars_hemis






