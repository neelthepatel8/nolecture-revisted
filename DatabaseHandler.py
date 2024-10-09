import mysql.connector
import json
from tqdm import tqdm

class MySQLDatabaseHandler:
    def __init__(self, host, user, password, database, port):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.cursor = self.connection.cursor()

    def insert_building(self, building_name):
        query = "INSERT INTO buildings (name) VALUES (%s)"
        self.cursor.execute(query, (building_name,))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_classroom(self, room_number, building_id):
        query = "INSERT INTO classrooms (room_number, building_id) VALUES (%s, %s)"
        self.cursor.execute(query, (room_number, building_id))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_course(self, course_id, start_time, end_time, day_of_week):
        query = """
        INSERT INTO courses (course_id, start_time, end_time, day_of_week)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (course_id, start_time, end_time, day_of_week))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_schedule(self, classroom_id, course_id):
        query = "INSERT INTO schedules (classroom_id, course_id) VALUES (%s, %s)"
        self.cursor.execute(query, (classroom_id, course_id))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def transfer_json_data_to_mysql(self, data):
        for building_name, classrooms in tqdm(data.items(), position=0):
            building_id = self.insert_building(building_name)
            for room_number, schedules in tqdm(classrooms.items(), leave=False):
                classroom_id = self.insert_classroom(room_number, building_id)
                for schedule in schedules:
                    course_id = schedule['id']
                    start_time = schedule['start']
                    end_time = schedule['end']
                    day_of_week = schedule['day']
                    course_id_db = self.insert_course(course_id, start_time, end_time, day_of_week)
                    self.insert_schedule(classroom_id, course_id_db)
        print("Data transferred to MySQL successfully.")
