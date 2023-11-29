from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from .anime import Anime
from .user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class AnimeRatings(db.Model):
    anime_id = db.Column(db.Integer, ForeignKey("Anime.id"), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("User.id"), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer,nullable = False)

    def __init__(self, username, anime_id, user_id, rating):
        self.username = username
        self.anime_id = anime_id
        self.user_id = user_id
        self.rating = rating

@app.route('/rate/<anime_id>/<user_id>')
def rate(anime_id, user_id):
    rating = AnimeRatings.query.get(anime_id, user_id)
    if request.json['rating'] < 0 or request.json['rating'] > 10:
        return jsonify({"message": "A nota deve estar entre 0 e 10!"})
    if rating:
        rating.rating = request.json['rating']
        db.session.commit()
        return jsonify({"message": "Avaliação atualizada com sucesso!"})

    anime = Anime.query.get(anime_id)
    if not anime:
        return jsonify({"message": "Insira um anime válido"})
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Insira um usuário válido"})
    animeRate = AnimeRatings(anime.id, user.id, request.json['rating'])
    db.session.add(animeRate)
    return jsonify({"message": "Avaliação adicionada com sucesso!"})
    

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
