from flask import Blueprint, jsonify

from api.factory import mongo

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/gamelog/games', methods=['GET'])
def games():
    try:
        results = mongo.db.gamelog.find()
        data = []
        for result in results:
            for key, value in result.items():
                if key == '_id':
                    continue
                else:
                    data.append({key: value})
        return jsonify(data)
    except Exception as e:
        return jsonify({'erro': 'Interno'}), 500


@api_bp.route('/gamelog/games/<id>', methods=['GET'])
def games_one(id):
    try:
        results = mongo.db.gamelog.find_one_or_404({'game_{}'.format(id): {'$exists': True}})
        for key, value in results.items():
            if key == 'game_{}'.format(id):
                return jsonify({key: value})
        return jsonify({'erro': 'Id not found'}), 404
    except Exception as e:
        return jsonify({'erro': 'Interno'}), 500
