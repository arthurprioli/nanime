
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db'
db = SQLAlchemy(app)

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    global_rating = db.Column(db.Float, nullable=False, default=-1.0)
    streaming_platform = db.Column(db.String(100), nullable=True)

    def __init__(self, name, description, release_date, global_rating, streaming_platform):
        self.name = name
        self.description = description
        self.release_date = release_date
        self.global_rating = global_rating
        self.streaming_platform = streaming_platform

@app.route('/anime', methods=['GET'])
def get_all_anime():
    anime = Anime.query.all()
    result = []
    for a in anime:
        anime_data = {}
        anime_data['id'] = a.id
        anime_data['name'] = a.name
        anime_data['description'] = a.description
        anime_data['release_date'] = a.release_date.strftime('%Y-%m-%d')
        anime_data['global_rating'] = a.global_rating
        anime_data['streaming_platform'] = a.streaming_platform
        result.append(anime_data)
    return jsonify(result)

@app.route('/anime/<id>', methods=['GET'])
def get_anime(id):
    anime = Anime.query.get(id)
    if anime:
        anime_data = {}
        anime_data['id'] = anime.id
        anime_data['name'] = anime.name
        anime_data['description'] = anime.description
        anime_data['release_date'] = anime.release_date.strftime('%Y-%m-%d')
        anime_data['global_rating'] = anime.global_rating
        anime_data['streaming_platform'] = anime.streaming_platform
        return jsonify(anime_data)
    else:
        return jsonify({'message': 'Anime not found'})

@app.route('/anime', methods=['POST'])
def create_anime():
    data = request.get_json()
    new_anime = Anime(name=data['name'], description=data['description'], release_date=data['release_date'],
                      global_rating=data['global_rating'], streaming_platform=data['streaming_platform'])
    db.session.add(new_anime)
    db.session.commit()
    return jsonify({'message': 'Anime created successfully'})

@app.route('/anime/<id>', methods=['PUT'])
def update_anime(id):
    anime = Anime.query.get(id)
    if anime:
        data = request.get_json()
        anime.name = data['name']
        anime.description = data['description']
        anime.release_date = data['release_date']
        anime.global_rating = data['global_rating']
        anime.streaming_platform = data['streaming_platform']
        db.session.commit()
        return jsonify({'message': 'Anime updated successfully'})
    else:
        return jsonify({'message': 'Anime not found'})

@app.route('/anime/<id>', methods=['DELETE'])
def delete_anime(id):
    anime = Anime.query.get(id)
    if anime:
        db.session.delete(anime)
        db.session.commit()
        return jsonify({'message': 'Anime deleted successfully'})
    else:
        return jsonify({'message': 'Anime not found'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
