from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Sample data representing user ratings for courses
ratings_data = [
    {'user_id': 1, 'course_id': 101, 'rating': 5},
    {'user_id': 1, 'course_id': 102, 'rating': 3},
    {'user_id': 2, 'course_id': 101, 'rating': 4},
    {'user_id': 2, 'course_id': 103, 'rating': 5},
    {'user_id': 3, 'course_id': 101, 'rating': 3},
    {'user_id': 3, 'course_id': 102, 'rating': 4},
    {'user_id': 3, 'course_id': 103, 'rating': 2},
]

def create_user_item_matrix(ratings_data):
    # Convert the ratings data into a DataFrame
    ratings_df = pd.DataFrame(ratings_data)

    # Create a user-item matrix with users as rows and courses as columns
    user_item_matrix = ratings_df.pivot(index='user_id', columns='course_id', values='rating')

    # Fill missing values with 0 (assuming unrated courses have a rating of 0)
    user_item_matrix = user_item_matrix.fillna(0)

    return user_item_matrix

def recommend_courses(user_id, user_item_matrix):
    # Compute cosine similarity between the user and all other users
    user_similarity = cosine_similarity(user_item_matrix)

    # Get the index of the target user
    user_index = user_id - 1  # assuming user_id starts from 1

    # Predict ratings for all courses not rated by the user
    predicted_ratings = user_similarity[user_index].dot(user_item_matrix) / np.array([np.abs(user_similarity[user_index]).sum()])

    # Create a list of course recommendations
    recommendations = []
    for course_id, rating in enumerate(predicted_ratings):
        if user_item_matrix.iloc[user_index, course_id] == 0:  # Check if the user hasn't rated the course
            recommendations.append({'course_id': user_item_matrix.columns[course_id], 'predicted_rating': rating})

    # Sort recommendations by predicted rating in descending order
    recommendations = sorted(recommendations, key=lambda x: x['predicted_rating'], reverse=True)

    return recommendations

@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    # Create the user-item matrix
    user_item_matrix = create_user_item_matrix(ratings_data)

    # Generate course recommendations for the given user
    recommendations = recommend_courses(user_id, user_item_matrix)

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
