import psycopg2
import os

# ratings = [
#     {"userId": 1, "courseId": 101, "rating": 5},
#     {"userId": 1, "courseId": 102, "rating": 3},
#     {"userId": 1, "courseId": 103, "rating": 2},
#     {"userId": 2, "courseId": 101, "rating": 4},
#     {"userId": 2, "courseId": 103, "rating": 2},
#     {"userId": 2, "courseId": 104, "rating": 5},
#     {"userId": 3, "courseId": 102, "rating": 2},
#     {"userId": 3, "courseId": 103, "rating": 5},
#     {"userId": 3, "courseId": 104, "rating": 3},
#     {"userId": 3, "courseId": 105, "rating": 4},
#     {"userId": 4, "courseId": 101, "rating": 3},
#     {"userId": 4, "courseId": 105, "rating": 4},
#     {"userId": 4, "courseId": 106, "rating": 2},
#     {"userId": 5, "courseId": 102, "rating": 4},
#     {"userId": 5, "courseId": 104, "rating": 3},
#     {"userId": 5, "courseId": 106, "rating": 5},
#     {"userId": 6, "courseId": 101, "rating": 2},
#     {"userId": 6, "courseId": 103, "rating": 4},
#     {"userId": 6, "courseId": 105, "rating": 3},
#     {"userId": 6, "courseId": 106, "rating": 4},
# ]


DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")


def get_db_connection():
    print("------------------------",DB_HOST)
    connection = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
    return connection


def getAllRatings():
    conn = get_db_connection()
    cursor = conn.cursor()
    print("testtttt")
    cursor.execute(
        'SELECT "courseId" , "userId" , "rating" FROM course_enrollment where rating is not null;'
    )
    rows = cursor.fetchall()

    colnames = [desc[0] for desc in cursor.description]

    result = [dict(zip(colnames, row)) for row in rows]

    cursor.close()
    conn.close()
    return result
