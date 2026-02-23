from flask import render_template, request, redirect, url_for
from app import flask_app, db, DogTask, get_dog_pics

@flask_app.route("/", methods=["GET", "POST"])
def index():
    dog_breeds = [
        "affenpinscher", "dalmatian", "germanshepherd", "kelpie",
        "labrador", "husky", "otterhound", "pitbull", "pug", "rottweiler"
    ]

    # Get all saved dog images
    all_dogs = DogTask.query.all()
    pictures = [dog.image_url for dog in all_dogs]

    if request.method == "POST":
        if request.form.get("submit") == "getDogPics":
            breed_type = request.form.get("breed")
            limit = int(request.form.get("limit"))
            get_dog_pics.delay(breed_type, limit)
            return redirect(url_for("index"))
        elif request.form.get("submit") == "clearDogPics":
            db.session.query(DogTask).delete()
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("template.html", breeds=dog_breeds, link=pictures)
