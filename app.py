from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Nugget(db.Model):
    __tablename__ = "nuggets"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    description = db.Column(db.String(500), unique=False)
    image = db.Column(db.String(800), unique=False)
    jewltype = db.Column(db.String(50), unique=False)
    price = db.Column(db.Float, unique=False)
    new = db.Column(db.Boolean, unique=False)

    def __init__(self, title, description, image, jewltype, price, new):
        self.title = title
        self.description = description
        self.image = image
        self.jewltype = jewltype
        self.price = price
        self.new = new


class NuggetSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description",
                  "image", "jewltype", "price", "new")


nugget_schema = NuggetSchema()
nuggets_schema = NuggetSchema(many=True)


@app.route("/")
def greeting():
    return "<h1>Hey Flask</h1>"


@app.route("/nuggets", methods=["GET"])
def get_nuggets():
    all_nuggets = Nugget.query.all()
    result = nuggets_schema.dump(all_nuggets)
    return jsonify(result.data)


@app.route("/nugget/<id>", methods=["GET"])
def get_nugget(id):
    nugget = Nugget.query.get(id)
    return nugget_schema.jsonify(nugget)


@app.route("/add-nugget", methods=["POST"])
def add_nugget():
    title = request.json["title"]
    description = request.json["description"]
    image = request.json["image"]
    jewltype = request.json["jewltype"]
    price = request.json["price"]
    new = request.json["new"]

    new_nugget = Nugget(title, description, image, jewltype, price, new)

    db.session.add(new_nugget)
    db.session.commit()

    return jsonify("ADDED!")


@app.route("/nugget/<id>", methods=["DELETE"])
def delete_nugget(id):
    nugget = Nugget.query.get(id)
    db.session.delete(nugget)
    db.session.commit()

    return jsonify("ITEM DELETED")


@app.route("/nugget/<id>", methods=["PUT"])
def update_nugget(id):
    nugget = Nugget.query.get(id)

    new_title = request.json["title"]
    new_description = request.json["description"]
    new_image = request.json["image"]
    new_jewltype = request.json["jewltype"]
    new_price = request.json["price"]
    new_new = request.json["new"]

    nugget.title = new_title
    nugget.description = new_description
    nugget.image = new_image
    nugget.jewltype = new_jewltype
    nugget.price = new_price
    nugget.new = new_new

    db.session.commit()
    return nugget_schema.jsonify(nugget)


if __name__ == "__main__":
    app.run(debug=True)
