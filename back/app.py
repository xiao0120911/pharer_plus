from flask import Flask, request, jsonify
from models import db, Player, Score
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"error": "Name are required"}), 400

    player = Player(name=name)
    db.session.add(player)
    db.session.commit()
    return jsonify({"message": "Player added successfully"}), 201

@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.json
    player_id = data.get('player_id')
    score = data.get('score')

    if not player_id or not score:
        return jsonify({"error": "Player ID and Score are required"}), 400

    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    new_score = Score(player_id=player_id, score=score)
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"message": "Score added successfully"}), 201

@app.route('/player/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    scores = Score.query.filter_by(player_id=player_id).all()
    score_list = [{"id": s.id, "score": s.score} for s in scores]

    return jsonify({
        "id": player.id,
        "name": player.name,
        "scores": score_list
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
