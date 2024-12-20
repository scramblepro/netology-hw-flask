from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

# Простая структура для хранения данных
ads = {}
ad_id_counter = 1


# Создать объявление (POST)
@app.route('/ads', methods=['POST'])
def create_ad():
    global ad_id_counter
    data = request.json

    # Проверка обязательных полей
    if not all(key in data for key in ['title', 'description', 'owner']):
        return jsonify({"error": "Missing required fields"}), 400

    ad = {
        "id": ad_id_counter,
        "title": data['title'],
        "description": data['description'],
        "created_at": datetime.now().isoformat(),
        "owner": data['owner']
    }
    ads[ad_id_counter] = ad
    ad_id_counter += 1
    return jsonify(ad), 201


# Получить объявление по ID (GET)
@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    ad = ads.get(ad_id)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404
    return jsonify(ad)


# Удалить объявление по ID (DELETE)
@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    if ad_id not in ads:
        return jsonify({"error": "Ad not found"}), 404
    del ads[ad_id]
    return jsonify({"message": "Ad deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
