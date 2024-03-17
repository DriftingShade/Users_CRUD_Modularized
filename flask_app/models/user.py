from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    DB = "users_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("users_schema").query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, NOW(), NOW());"

        return connectToMySQL("users_schema").query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """UPDATE users 
                SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s
                WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return results

    @classmethod
    def delete(cls, user_id):
        query = """DELETE FROM users WHERE id = %(id)s;"""
        print(query)
        results = connectToMySQL("users_schema").query_db(query, user_id)
        print(results)
        return results

    @classmethod
    def one_user(cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s"""
        print(query)
        results = connectToMySQL("users_schema").query_db(query, data)
        print(results)
        return results[0]

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email Address", "Email Address Required")
            is_valid = False
        if len(user["fname"]) == 0:
            flash("First Name Is Required")
            is_valid = False
        if len(user["lname"]) == 0:
            flash("Last Name Is Required")
            is_valid = False
        return is_valid
