from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars_data = mongo.db.mars_data_db.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars_data=mars_data)


# set our path to /scrape
@app.route("/scrape")
def scraper():
    # create a listings database
    mars_data_db = mongo.db.mars_data
    # call the scrape function in our scrape_mars file to save to mongo.
    mars_data_ = scrape_mars.scrape()
    # update our mars data with the data that is being scraped.
    mars_data.update({}, mars_data_, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
