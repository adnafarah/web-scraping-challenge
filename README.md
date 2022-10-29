
# Mission to Mars

In this project, I have built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. 

There are 2 parts to this project:

 - Scraping
 - MongoDB and Flask Application


### Part  1: Scraping
The initial scraping was completed using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter (to navigate the websites). The Jupyter notebook is titled mission_to_mars.ipynb. 

The information that was scraped is as follows:

        - Mars News Site: collected the latest News Title and Paragraph Text
        - JPL Mars Space Images: scraped the Featured Image URL
        - Mars Facts: used Pandas to scrape the table containing facts about the planet including diameter, mass, etc
        - Mars Hemispheres: obtained high-resolution images for each hemisphere of Mars, along with its title



### Part 2: MongoDB and Flask Application
Used MongoDB with Flask templating to create a new HTML page that displays all the information that was scraped from the URLs above.


The Jupyter notebook was converted into a Python script called scrape_mars.py that uses a function called scrape. This function executes all the scraping code from above and returns one Python dictionary containing all the scraped data.


Next, created a route called /scrape that will import the scrape_mars.py script and calls the scrape function.

Stored the return value in Mongo as a Python dictionary.

Created a root route / that will query the Mongo database and pass the Mars data into an HTML template for displaying the data.

Created a template HTML file called index.html that will take the Mars data dictionary and display all the data in the appropriate HTML elements. 