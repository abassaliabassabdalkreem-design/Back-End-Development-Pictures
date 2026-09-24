from flask import Flask, jsonify, request

app = Flask(__name__)

pictures_list = [
    {"id": "0", "pic_url": "image1.jpg", "user_id": "1"},
    {"id": "1", "pic_url": "image2.jpg", "user_id": "2"},
]

@app.route('/health')
def health():
    return jsonify({"status": "OK"}), 200

@app.route('/count')
def count():
    return jsonify({"count": len(pictures_list)}), 200

@app.route('/picture', methods=['GET'])
def get_all_pictures():
    return jsonify(pictures_list), 200

@app.route('/picture/<id>', methods=['GET'])
def get_picture_by_id(id):
    for pic in pictures_list:
        if pic["id"] == id:
            return jsonify(pic), 200
    return jsonify({"message": "Picture not found"}), 404

@app.route('/picture', methods=['POST'])
def add_picture():
    new_pic = request.get_json()
    pictures_list.append(new_pic)
    return jsonify(new_pic), 201

@app.route('/picture/<id>', methods=['PUT'])
def update_picture(id):
    updated = request.get_json()
    for pic in pictures_list:
        if pic["id"] == id:
            pic.update(updated)
            return jsonify(pic), 200
    return jsonify({"message": "Picture not found"}), 404

@app.route('/picture/<id>', methods=['DELETE'])
def delete_picture(id):
    global pictures_list
    pictures_list = [p for p in pictures_list if p["id"] != id]
    return jsonify({"message": "Picture deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)