
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def scrape1(browser) -> tuple:
    
    ## Scrape 1 NASA Mars News##
    # The url we want to scrape
    url1 = 'https://redplanetscience.com/'
    
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url1)
    browser.is_element_present_by_css("div.list_text", wait_time=1)  

    # Let it sleep for 1 second
    #time.sleep(1)

    # Return all the HTML on our page
    html = browser.html
    
    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    news_soup = soup(html, 'html.parser')

    #Use CSS selector
    list_text = news_soup.select_one('div.list_text')
    list_text.find('div', class_='content_title')

    # Build our dictionary for the headline, price, and neighborhood from our scraped data
    news_title = list_text.find('div', class_='content_title').get_text()
    news_paragraph = list_text.find('div', class_='article_teaser_body').get_text()
    

    # Return our dictionary
    return news_title, news_paragraph

def scrape2(browser):
    
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    #Store as variable
    featured_image_url = f'https://spaceimages-mars.com/{img_url_rel}'
       
    return featured_image_url

def scrape3(browser):
    
    ## Scrape 3 Mars Facts##

    mars_facts_url = 'https://galaxyfacts-mars.com/'
    mars_facts = pd.read_html(mars_facts_url)

    #put into dataframe
    df1 = mars_facts[0]

    #Make top row the column names 
    new_header = df1.iloc[0] 
    df1.columns = new_header

    #convert to html string 
    mars_table = df1.to_html(classes="table table-striped")        

        # Return our dictionary
    return mars_table

def scrape4(browser):

    ## Scrape 4 Mars Hemispheres ##

    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

        
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    hemispheres_all = hemisphere_soup.find_all('div', class_='description')

    titles_list = []
    img_links = []
    counter = 0

    hem_dicts = []

    for x in range(4):
        browser.find_by_css('a.product-item img')[int(counter)].click()
        hemisphere_soup = soup(html, 'html.parser')
        
        #get titles
        title = hemisphere_soup.body.find_all('h3')[int(counter)].text
        print(title)
        titles_list.append(title)
            
        #click on Sample  
        elem = browser.links.find_by_text('Sample').first
        #finding image url 
        imgurl = elem['href']
        print(imgurl)
        img_links.append(imgurl)
        browser.back()
        counter = counter + 1
        
        hem_dicts.append({'title': title,
                        'imgurl': imgurl        
        })
        

    return hem_dicts


def scrape():
    # Set an empty dict for saving to Mongo
    mars_data = {}

    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    data1 = scrape1(browser)
    data2 = scrape2(browser)
    data3 = scrape3(browser)
    # data4 = scrape4()
    print("The scraped data are")
    print(data1, data2, data3)
    browser.quit()
    mars_data = {"news_title": data1[0],
                "news_paragraph": data1[1],
                "featured_image_url": data2,
                "mars_table": data3}
    return mars_data

    

