from flask import Flask, jsonify
import mysql.connector
import constants as secrets
import queries
from datetime import time, timedelta
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, support_credentials=True)


def get_db_connection():
    connection = mysql.connector.connect(
        host=secrets.host,
        user=secrets.username,
        password=secrets.password,
        database=secrets.database,
        port=secrets.port
    )
    return connection

def get_free_classrooms():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True) 
    cursor.execute("SET time_zone = 'America/New_York';")

    query = queries.QUERY_FREE_CLASSROOMS

    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        if row['next_lecture_time'] is not None:
            if isinstance(row['next_lecture_time'], time):
                row['next_lecture_time'] = row['next_lecture_time'].strftime("%H:%M:%S")
            elif isinstance(row['next_lecture_time'], timedelta):
                row['next_lecture_time'] = str(row['next_lecture_time'])

    cursor.close()
    connection.close()

    return result

@cross_origin(supports_credentials=True)
@app.route('/api/free-classrooms', methods=['GET'])
def free_classrooms():
    free_classrooms_data = get_free_classrooms()
    return jsonify(free_classrooms_data)

@cross_origin(supports_credentials=True)
@app.route('/')
def default_landing():
    return 'NoLecture-Revisited API'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)