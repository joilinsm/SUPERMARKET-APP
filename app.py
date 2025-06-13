from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, db
import os

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("private_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://supermarket-app-7bf1b-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Reference to the Firebase database
ref = db.reference('items')

@app.route('/')
def index():
    return render_template('index.html')

# CREATE
@app.route('/items', methods=['POST'])
def create_item():
    try:
        data = request.get_json(force=True)
        if not data or 'name' not in data:
            raise ValueError("Missing 'name' in data")

        new_item_ref = ref.push()
        new_item_ref.set(data)
        return jsonify({"success": True, "id": new_item_ref.key}), 201
    except Exception as e:
        print("Error in POST /items:", str(e))
        return jsonify({"success": False, "error": str(e)}), 400


# READ all
@app.route('/items', methods=['GET'])
def get_items():
    try:
        items = ref.get()
        return jsonify(items) if items else jsonify({}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# READ single
@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = ref.child(item_id).get()
        return jsonify(item) if item else jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# UPDATE
@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.get_json(force=True)
        ref.child(item_id).update(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# DELETE
@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        ref.child(item_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use provided PORT or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
