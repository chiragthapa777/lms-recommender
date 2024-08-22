from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict


def create_user_item_matrix(ratings):
    user_ids = list(set([r["userId"] for r in ratings]))
    course_ids = list(set([r["courseId"] for r in ratings]))

    user_to_index = {user_id: index for index, user_id in enumerate(user_ids)}
    course_to_index = {course_id: index for index, course_id in enumerate(course_ids)}

    matrix = np.zeros((len(user_ids), len(course_ids)))

    for r in ratings:
        user_index = user_to_index[r["userId"]]
        course_index = course_to_index[r["courseId"]]
        matrix[user_index][course_index] = r["rating"]

    return matrix, user_to_index, course_to_index


def get_recommendations(userId, matrix, user_to_index, course_to_index):
    if userId not in user_to_index:
        return []

    # Calculate cosine similarity between users
    user_index = user_to_index[userId]
    user_ratings = matrix[user_index].reshape(1, -1)
    similarities = cosine_similarity(user_ratings, matrix).flatten()

    # Create a dictionary of scores for all courses
    course_scores = defaultdict(float)

    for other_user_index, similarity in enumerate(similarities):
        if other_user_index == user_index:
            continue
        for course_index, rating in enumerate(matrix[other_user_index]):
            if matrix[user_index][course_index] == 0:  # if user hasn't rated the course
                course_scores[course_index] += similarity * rating

    # Sort courses by score
    recommended_courses = sorted(
        course_scores.items(), key=lambda x: x[1], reverse=True
    )

    # Convert course indexes back to course IDs
    index_to_course = {index: course_id for course_id, index in course_to_index.items()}
    return [index_to_course[index] for index, score in recommended_courses]
