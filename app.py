import os
from flask import (Flask, render_template, redirect, request, url_for, session)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# Only import env if env.py path exists
if os.path.exists("env.py"):
    import env

# Create instance of Flask
app = Flask(__name__)

# Adding
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Create an instance of pymongo
mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    items = mongo.db.items.find()
    return render_template("index.html", items=items)


@app.route("/items")
def items():
    items = list(mongo.db.items.find())
    categories = mongo.db.categories.find()
    return render_template("items.html", items=items, categories=categories)


@app.route("/filter", methods=["GET", "POST"])
def filter():
    """
    Get all checked values for category filter,
    find and display items with those categories
    """
    categories = mongo.db.categories.find()
    selected_categories = request.form.getlist("selected-categories")
    items = list(mongo.db.items.find(
        {"category": {"$in": selected_categories}}))
    return render_template("items.html", items=items, categories=categories,
                           selected_categories=selected_categories)


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
