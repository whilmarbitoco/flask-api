from flask import Flask, jsonify, g, request
from models import User

app = Flask(__name__)

@app.before_request
def before_request():
    g.user = User()

@app.route("/")
def home():
    return jsonify(g.user.getAllUsers())


@app.route("/<int:id>")
def getUser(id):
    user = g.user.getUser(id)
    return jsonify(user)


@app.route("/", methods=["POST"])
def create_user():
    data = request.get_json()

    new_user = g.user.addUser(data.get("name"), data.get("username"), data.get("password"))

    if new_user:
        return jsonify({"message": "User created successfully"})
    else:
        return jsonify({"message": "Failed to create user"}), 500


@app.route("/<int:user_id>", methods=["POST"])
def edit_user(user_id):
    user = g.user.getUser(user_id)
    data = request.get_json()

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    updated_user = g.user.editUser(user_id, data.get("name"), data.get("username"), data.get("password"))

    if updated_user:
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"message": "Failed to update user"}), 500


@app.route("/<int:user_id>", methods=["DELETE"])
def del_user(user_id):
    user = g.user.getUser(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    g.user.delUser(user_id)
    return jsonify({"message": "User deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
