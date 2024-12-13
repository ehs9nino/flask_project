from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "users.txt"


# Ensure the text file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        file.write(json.dumps([]))


# Utility functions
def read_users():
    with open(DATA_FILE, "r") as file:
        return json.loads(file.read())


def write_users(users):
    with open(DATA_FILE, "w") as file:
        file.write(json.dumps(users, indent=2))


# API Endpoints

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    email = data.get("email")
    age = data.get("age")

    print(f"Received data for add: {data}")  # Debugging
    print(f"Existing users: {read_users()}")  # Debugging

    if not email or not age:
        return jsonify({"error": "Email and age are required!"}), 400

    users = read_users()
    if any(user["email"] == email for user in users):
        print(f"Duplicate user found: {email}")  # Debugging
        return jsonify({"error": "User already exists!"}), 400

    new_user = {"email": email, "age": age}
    users.append(new_user)
    write_users(users)

    print(f"User added: {new_user}")  # Debugging
    return jsonify({"message": "User added successfully!", "user": new_user}), 201


@app.route("/get_user", methods=["GET"])
def get_user():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email is required!"}), 400

    users = read_users()
    user = next((user for user in users if user["email"] == email), None)
    if not user:
        return jsonify({"error": "User not found!"}), 404

    return jsonify(user)


@app.route("/update_user", methods=["PUT"])
def update_user():
    data = request.get_json()
    email = data.get("email")
    age = data.get("age")

    print(f"Received data for update: {data}")  # Debugging
    print(f"Existing users: {read_users()}")  # Debugging

    if not email or not age:
        return jsonify({"error": "Email and age are required!"}), 400

    users = read_users()
    for user in users:
        if user["email"] == email:
            user["age"] = age
            write_users(users)
            print(f"User updated: {user}")  # Debugging
            return jsonify({"message": "User updated successfully!", "user": user})

    print(f"No user found with email: {email}")  # Debugging
    return jsonify({"error": "User not found!"}), 404


@app.route("/delete_user", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required!"}), 400

    users = read_users()
    updated_users = [user for user in users if user["email"] != email]
    if len(updated_users) == len(users):
        return jsonify({"error": "User not found!"}), 404

    write_users(updated_users)
    return jsonify({"message": "User deleted successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
