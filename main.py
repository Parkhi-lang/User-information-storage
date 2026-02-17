from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
users = {}
current_id = 1


# ----------------------------
# GET - Get all users
# ----------------------------
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


# ----------------------------
# GET - Get single user
# ----------------------------
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[user_id])


# ----------------------------
# POST - Create new user
# ----------------------------
@app.route('/users', methods=['POST'])
def create_user():
    global current_id

    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email required"}), 400

    users[current_id] = {
        "id": current_id,
        "name": data["name"],
        "email": data["email"]
    }

    current_id += 1

    return jsonify(users[current_id - 1]), 201


# ----------------------------
# PUT - Update user
# ----------------------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    users[user_id]["name"] = data.get("name", users[user_id]["name"])
    users[user_id]["email"] = data.get("email", users[user_id]["email"])

    return jsonify(users[user_id])


# ----------------------------
# DELETE - Delete user
# ----------------------------
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    deleted_user = users.pop(user_id)

    return jsonify({
        "message": "User deleted successfully",
        "user": deleted_user
    })


if __name__ == '__main__':
    app.run(debug=True)
