"""Flask app for Cupcakes"""
from crypt import methods
from email.mime import image
from flask import Flask, request, redirect, render_template, flash, jsonify
from models import db, connect_db, Cupcake
from functions import serialize_cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/api/cupcakes")
def get_cupcake_list():
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(cupcake) for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_ids_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=["POST"])
def create_new_cupcake():
    ck_flavor = request.json["flavor"]
    ck_size = request.json["size"]
    ck_rating = request.json["rating"]
    ck_image = request.json.get("image", None)

    if ck_image == "":
        ck_image = None

    cupcake = Cupcake(flavor=ck_flavor,
                      size=ck_size,
                      rating=ck_rating, image=ck_image)

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)
    return (jsonify(cupcake=serialized), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()

    serialized = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Cupcake deleted")
