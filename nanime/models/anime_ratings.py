from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class AnimeRatings(db.Model):
    anime_id = db.Column(db.Integer, ForeignKey("Anime.id"), primary_key=true)
    user_id = db.Column(db.Integer, ForeignKey("User.id"), primary_key=true)
    rating = db.Column(db.Integer,nullable = False)

    def __init__(self, anime_id, user_id, rating):
        self.username = username
        self.anime_id = anime_id
        self.user_id = user_id
        self.rating = rating

@app.route('/rate/<anime_id>/<user_id>')
def rate(anime_id, user_id):
    rating = AnimeRatings.query.get(anime_id, user_id)
    if data['rating'] < 0 and data['rating'] >10:
        return jsonify({message: "A nota deve estar entre 0 e 10!"})
    if rating:
        rating.rating = data['rating']
        db.session.commit()
        return jsonify({message: "Avaliação atualizada com sucesso!"})

    anime = Anime.query.get(anime_id)
    if not anime:
        return jsonify({message: "Insira um anime válido"})
    user = User.query.get(user_id)
    if not user:
        return jsonify({message: "Insira um usuário válido"})
    animeRate = new AnimeRatings(anime.id, user.id, data['rating'])
    db.session.add(animeRate)
    return jsonify({message: "Avaliação adicionada com sucesso!"})
    

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
