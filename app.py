from flask import Flask, jsonify
from recommender import create_user_item_matrix, get_recommendations

app = Flask(__name__)


# def get_ratings_from_db():
#     # Connect to PostgreSQL database
#     connection = psycopg2.connect(
#         dbname="your_database_name",
#         user="your_username",
#         password="your_password",
#         host="your_host",  # e.g., 'localhost'
#         port="your_port"  # e.g., '5432'
#     )

#     cursor = connection.cursor()

#     # Execute the query to fetch ratings
#     cursor.execute("SELECT user_id, course_id, ratings FROM enrollments")

#     # Fetch all rows from the executed query
#     rows = cursor.fetchall()

#     # Close the cursor and connection
#     cursor.close()
#     connection.close()

#     # Convert rows into the required format
#     ratings = [{"userId": row[0], "courseId": row[1], "rating": row[2]} for row in rows]

#     return ratings

ratings = [
    {"userId": 1, "courseId": 101, "rating": 5},
    {"userId": 1, "courseId": 102, "rating": 3},
    {"userId": 1, "courseId": 103, "rating": 2},
    {"userId": 2, "courseId": 101, "rating": 4},
    {"userId": 2, "courseId": 103, "rating": 2},
    {"userId": 2, "courseId": 104, "rating": 5},
    {"userId": 3, "courseId": 102, "rating": 2},
    {"userId": 3, "courseId": 103, "rating": 5},
    {"userId": 3, "courseId": 104, "rating": 3},
    {"userId": 3, "courseId": 105, "rating": 4},
    {"userId": 4, "courseId": 101, "rating": 3},
    {"userId": 4, "courseId": 105, "rating": 4},
    {"userId": 4, "courseId": 106, "rating": 2},
    {"userId": 5, "courseId": 102, "rating": 4},
    {"userId": 5, "courseId": 104, "rating": 3},
    {"userId": 5, "courseId": 106, "rating": 5},
    {"userId": 6, "courseId": 101, "rating": 2},
    {"userId": 6, "courseId": 103, "rating": 4},
    {"userId": 6, "courseId": 105, "rating": 3},
    {"userId": 6, "courseId": 106, "rating": 4},
]


@app.route("/recommend/<user_id>", methods=["GET"])
def recommend(user_id):
    userId = int(user_id)
    matrix, user_to_index, course_to_index = create_user_item_matrix(ratings)
    recommended_courses = get_recommendations(
        userId, matrix, user_to_index, course_to_index
    )
    return jsonify({"userId": userId, "recommendedCourses": recommended_courses})


if __name__ == "__main__":
    app.run(debug=True)
