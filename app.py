from flask import Flask, make_response, jsonify, request
import uuid, random

app = Flask(__name__)

# Sample business data
businesses = {}

def generate_dummy_data():
    towns = ["Belfast", "Derry", "Bambridge", "Lisburn", "Newry"]
    business_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz " + str(i)
        town = towns[ random.randint(0, len(towns) - 1) ]
        rating = random.randint(1, 5)
        business_dict[id] = {
            "name": name,
            "town": town,
            "rating": rating,
            "reviews": []
        }
    return business_dict


@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    return make_response( jsonify( businesses ), 200 )

@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
def show_one_business(id):
    return make_response( jsonify( businesses[id] ), 200 )

@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    next_id = str(uuid.uuid1())
    new_business = {
        "id": next_id,
        "name": request.form["name"],
        "town": request.form["town"],
        "rating": request.form["rating"],
        "reviews": []
    }
    businesses[next_id] = new_business
    return make_response(jsonify( new_business ), 201)

@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    businesses[id]["name"] = request.form["name"]
    businesses[id]["town"] = request.form["town"]
    businesses[id]["rating"] = request.form["rating"]

    return make_response(jsonify({id : businesses[id]}), 200)

@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    del businesses[id]
    return make_response(jsonify({}), 200)

@app.route("/api/v1.0/businesses/<int:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    for business in businesses:
        if business["id"] == id:
            break
    return make_response(jsonify(business["reviews"]), 200)

@app.route("/api/v1.0/businesses/<int:b_id>/reviews",
           methods=["POST"])
def add_new_review(b_id):
    for business in businesses:
        if business["id"] == b_id:
            if len(business["reviews"]) == 0:
                new_review_id = 1
            else:
                new_review_id = \
                    business["reviews"][-1]["id"] + 1
            new_review = {
                "id": new_review_id,
                "username": request.form["username"],
                "comment": request.form["comment"],
                "stars": request.form["stars"]
            }
            business["reviews"].append(new_review)
            break
    return make_response(jsonify(new_review), 201)

@app.route( \
    "/api/v1.0/businesses/<int:b_id>/reviews/<int:r_id>",
    methods=["GET"])
def fetch_one_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    break
            break
    return make_response(jsonify(review), 200)

@app.route(
    "/api/v1.0/businesses/<int:b_id>/reviews/<int:r_id>",
    methods=["PUT"])
def edit_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    review["username"] = request.form["username"]
                    review["comment"] = request.form["comment"]
                    review["stars"] = request.form["stars"]
                    break
            break
    return make_response(jsonify(review), 200)

@app.route(
    "/api/v1.0/businesses/<int:b_id>/reviews/<int:r_id>",
    methods=["DELETE"])
def delete_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    business["reviews"].remove(review)
                    break
            break
    return make_response(jsonify({}), 200)


# Run the Flask app
if __name__ == "__main__":
    businesses = generate_dummy_data()
    app.run(debug=True)
