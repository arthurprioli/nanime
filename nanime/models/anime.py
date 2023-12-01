
from flask import Flask, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
from flask import render_template
from . import user

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
    image_url = db.Column(db.String(200), nullable=True)  # Add the image URL field

    def __init__(self, name, description, release_date, global_rating, streaming_platform, image_url):
        self.name = name
        self.description = description
        self.release_date = release_date
        self.global_rating = global_rating
        self.streaming_platform = streaming_platform
        self.image_url = image_url

class UserAnimeList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), nullable = False)

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
        anime_data['image_url'] = a.image_url  # Fix: Add image_url to the response
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
        anime_data['image_url'] = anime.image_url
        return jsonify(anime_data)
    else:
        return jsonify({'message': 'Anime not found'})

@app.route('/anime', methods=['POST'])
def create_anime():
    data = request.get_json()
    new_anime = Anime(name=data['name'], description=data['description'], release_date=data['release_date'],
                      global_rating=data['global_rating'], streaming_platform=data['streaming_platform'],
                      image_url=data['image_url'])  # Fix: Add image_url to the Anime() call
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

@app.route('/anime/<anime_name>', methods=['GET'])
def search_anime(anime_name):
    print(anime_name)
    print("blablabla")
    anime = Anime.query.filter_by(name=anime_name).first()
    if anime:
        return render_template("home.html", anime = anime)
    else:
        # Search from Jikan API
        response = requests.get(f'https://api.jikan.moe/v4/anime?q={anime_name}')
        if response.status_code == 200:
            anime_data = response.json()
            if anime_data['results']:
                anime_info = anime_data['results'][0]
                name = anime_info['title']
                description = anime_info['synopsis']
                release_date = anime_info['start_date']
                global_rating = anime_info['score']
                streaming_platform = anime_info['url']
                image_url = anime_info['images']['jpg']['image_url']
                
                new_anime = Anime(name=name, description=description, release_date=release_date,
                                  global_rating=global_rating, streaming_platform=streaming_platform,
                                  image_url=image_url)
                create_anime(new_anime) 
                return render_template("home.html", anime = new_anime)
            else:
                return render_template("home.html", anime = new_anime)
        else:
            return render_template("home.html", anime = new_anime)


@app.route('/add_anime/<int:user_id>/<int:anime_id>', methods=['POST'])
def add_anime(user_id, anime_id):
    user = User.query.get(user_id)
    anime = Anime.query.get(anime_id)

    if user and anime:
        user_anime_entry = UserAnimeList(user_id=user.id, anime_id=anime.id)
        db.session.add(user_anime_entry)
        db.session.commit()
    
    return redirect(url_for('users', user_id=user.id))

