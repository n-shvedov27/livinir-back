from flask import Flask, jsonify, request
from model import Roommate, Post
from http import HTTPStatus
import json
import uuid

app = Flask(__name__)

roommates = []

with open('db.json') as f:
    db = json.load(f)

USERS_FIELD = "users"
POST_FIELD = "posts"


def user_already_exist(email: str):
    for user in db[USERS_FIELD]:
        if user['email'] == email:
            return True

    return False


@app.route('/api/v1/registration', methods=["POST"])
def registration():
    new_user_json = request.get_json()
    new_user = Roommate.deserialize(new_user_json)

    if user_already_exist(new_user.email):
        return jsonify({
            "message": "user already exist"
        }), HTTPStatus.BAD_REQUEST
    else:
        db[USERS_FIELD].append(new_user.serialize())

        with open('db.json', "w") as f:
            json.dump(db, f)

        return jsonify(new_user.serialize())


def find_user_by_email(email):
    for user in db[USERS_FIELD]:
        if user['email'] == email:
            return user


def find_user_by_id(id):
    for user in db[USERS_FIELD]:
        if user['id'] == id:
            return user


@app.route('/api/v1/login', methods=["POST"])
def login():
    user_json = request.get_json()
    email = user_json['email']
    password = user_json['password']

    user = find_user_by_email(email)

    if user is None:
        return jsonify({
            "message": "user not found"
        }), HTTPStatus.NOT_FOUND

    if user['password'] == password:
        return jsonify(user)
    else:
        return jsonify({
            "message": "invalid email or password"
        }), HTTPStatus.BAD_REQUEST


@app.route('/api/v1/post')
def get_all_posts():
    return jsonify(db[POST_FIELD])


@app.route('/api/v1/post', methods=["POST"])
def create_post():
    user_json = request.get_json()
    text = user_json['text']
    title = user_json['title']
    author_id = user_json['author_id']

    user = find_user_by_id(author_id)

    if user is None:
        return jsonify({
            "message": "user not found"
        }), HTTPStatus.NOT_FOUND

    post = Post(text, title, Roommate(
        uid=user["id"], username=user["username"], email=user["email"], password=user["password"]
    ))

    db[POST_FIELD].append(post.serialize())

    with open('db.json', "w") as f:
        json.dump(db, f)

    return jsonify(post.serialize())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
