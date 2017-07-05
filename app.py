import os
from flask import *
import mlab
from mongoengine import *

from werkzeug.utils import secure_filename

app = Flask(__name__)

mlab.connect()

app.config["IMG_PATH"] = os.path.join(app.root_path, "images")
app.secret_key = "2fadsfsdfasdefawef"


class Flower(Document):
    image = StringField()
    title = StringField()
    price = FloatField()

# flower1 = Flower(image="http://www.interrose.co.uk/images/products/black_background/r001_happy.jpg",
#                  title="Rose",
#                  price=10000
#                 )
#
# flower2 = Flower(image="https://s-media-cache-ak0.pinimg.com/736x/78/a5/0e/78a50ef9eb93d584dbd6ba44499b7d51.jpg",
#                  title="Rose Blue",
#                  price=20000
#                 )
#
# flower3 = Flower(image="http://blog-20c0.kxcdn.com/wp-content/uploads/2016/05/black-rose-1.jpg",
#                  title="Rose Black",
#                  price=10000
#                 )

# flower1.save()
# flower2.save()
# flower3.save()
#
# flowers = [
#     {
#         "image": "http://www.interrose.co.uk/images/products/black_background/r001_happy.jpg",
#         "title": "Rose",
#         "price": 10000.0
#     },
#     {
#         "image": "https://s-media-cache-ak0.pinimg.com/736x/78/a5/0e/78a50ef9eb93d584dbd6ba44499b7d51.jpg",
#         "title": "Rose Blue",
#         "price": 20000.0
#     },
#     {
#         "image": "http://blog-20c0.kxcdn.com/wp-content/uploads/2016/05/black-rose-1.jpg",
#         "title": "Rose Black",
#         "price": 30000.0
#     }
# ]
image = "http://www.interrose.co.uk/images/products/black_background/r001_happy.jpg"
title = "Rose"
price = 10000



@app.route('/')
def index():
    return render_template("index.html", flowers=Flower.objects())

@app.route("/images/<image_name>")
def image(image_name):
    return send_from_directory(app.config["IMG_PATH"], image_name)

@app.route("/about")
def about():
    return "FAp"

@app.route("/login", methods= ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]

        if username == "admin" and password == "admin":

            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return "Invalid credentials"

@app.route("/add_flower", methods=["GET", "POST"])
def add_flower():
    if "logged_in" in session and session ["logged_in"]:

        if request.method == "GET": #FORM REQUESTED
            return render_template("add_flower.html")

        elif request.method == "POST": #USER SUBMITTED FAN
            # 1: gET DATA (title , image, price)
            form = request.form
            title = form["title"]
            price = form["price"]

            image = request.files["image"]
            filename = secure_filename(image.filename)

            image.save(os.path.join(app.config["IMG_PATH"], filename))

            print(filename)

            # 2: Save data into database
            new_flower = Flower(title= title,
                                image = "/images/{0}".format(filename),
                                price = price)
            new_flower.save()
            return  redirect(url_for("index"))

    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session ["logged_in"] = False
    return redirect(url_for("login"))

@app.route("/users/<username>")
def user(username):
    return "hello, my name is " + username + ", welcome to my page"

@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return "{0} + {1} = {2}".format(a, b, a + b)

if __name__ == '__main__':
    app.run()
