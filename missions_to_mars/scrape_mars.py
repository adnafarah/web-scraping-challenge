
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



def scrape():
    
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Set an empty dict for saving to Mongo
    mars_data = {}

    ## Scrape 1 ##
    # The url we want to scrape
    url1 = 'https://redplanetscience.com/'
    
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url1)

    # Let it sleep for 1 second
    #time.sleep(1)

    # Return all the HTML on our page
    html = browser.html
    
    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    news_soup = soup(html, 'html.parser')

    #Use CSS selector
    list_text = news_soup.select_one('div.list_text')
    list_text.find('div', class_='content_title')
    

    ## Scrape 2 ##
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = soup(html, 'html.parser')

    img_url_rel = img_soup.find('img', class_='headerimage fade-in').get('src')
    
    ## Scrape 3 ##

    mars_facts_url = 'https://galaxyfacts-mars.com/'
    mars_facts = pd.read_html(mars_facts_url)

    # Select info we want
    mars_facts[1]
    #put into dataframe
    df1 = mars_facts[1]


    #Make top row the column names 
    new_header = df1.iloc[0] 
    df1.columns = new_header

    #convert to html string 
    mars_table = df1.to_html
    

    ## Scrape 4 ##

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

    # Build our dictionary for the headline, price, and neighborhood from our scraped data
    mars_data["news_title"] = list_text.find('div', class_='content_title').get_text()
    mars_data["news_p"] = list_text.find('div', class_='article_teaser_body').get_text()
    mars_data["featured_image_url"] = f'https://spaceimages-mars.com/{img_url_rel}'
    mars_data["mars_table"] = mars_table
    mars_data["hemispheres"] = hem_dicts 

    # Quit the browser
    browser.quit()

    # Return our dictionary
    return mars_data

