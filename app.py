from flask import Flask, jsonify
from recommender import create_user_item_matrix, get_recommendations
from database import getAllRatings
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "welcome to the recommender"})

@app.route("/recommend/<user_id>", methods=["GET"])
def recommend(user_id):
    userId = int(user_id)
    matrix, user_to_index, course_to_index = create_user_item_matrix(getAllRatings())
    recommended_courses = get_recommendations(
        userId, matrix, user_to_index, course_to_index
    )
    return jsonify({"userId": userId, "recommendedCourses": recommended_courses})




if __name__ == "__main__":
    app.run(debug=True)
