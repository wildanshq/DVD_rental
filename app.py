from flask import Flask, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw' : '123098',
    'db' : 'dvdrental',
    'host' : 'localhost',
    'port' : '5432'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)
ma = Marshmallow(app)
from model import Actor, ActorSchema, Film, FilmSchema, City, CitySchema

@app.route('/index', methods=['GET'])
def index():
    return 'Hello World'

@app.route('/actor', methods=['GET'])
def get_actors():
    try:
        actors = Actor.query.all()
        actors_schema = ActorSchema(many=True)
        return jsonify(data=actors_schema.dump(actors))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/actor/<_id>', methods=['GET'])
def call_actor_by_id(_id):
    try:
        actor = Actor.query.filter_by(actor_id=_id).first()
        actors_schema = ActorSchema()
        return jsonify(data=actors_schema.dump(actor))
    except Exception as e:
        return jsonify(eror=str(e))

@app.route('/actor/add', methods=['POST'])
def add_actor():
    body = request.json.get
    first_name = body('first_name')
    last_name = body('last_name')
    
    try: 
        actor = Actor(first_name,last_name)
        actors_schema = ActorSchema()
        db.session.add(actor)
        db.session.commit()
        return jsonify(actors_schema.dump(actor))
    except Exception as e:
        return jsonify(eror=str(e))

@app.route('/actor/<_id>', methods=['PUT'])
def update_actor(_id):
    body = request.json.get
    first_name = body('first_name')
    last_name = body('last_name')
    
    try: 
        actor = Actor.query.filter_by(actor_id=_id).first()
        actor.first_name = first_name
        actor.last_name = last_name
        actors_schema = ActorSchema()
        db.session.commit()
        return jsonify(actors_schema.dump(actor))
    except Exception as e:
        return jsonify(eror=str(e))

@app.route('/actor/<_id>', methods=['DELETE'])
def remove_actor(_id):
    try:
        actor = Actor.query.filter_by(actor_id=_id).first()
        db.session.delete(actor)
        db.session.commit()
        return jsonify(actor_id=_id)
    except Exception as e:
        return jsonify(eror=str(e))

@app.route('/city', methods=['GET'])
def call_city():
    try:
        citys = City.query.all()
        citys_schema = CitySchema(many=True)
        return jsonify(citys_schema.dump(citys))
    except Exception as e:
        return jsonify(eror=str(e))

@app.route('/city/<_id>', methods=['GET'])
def call_city_by_id(_id):
    try:
        citys = City.query.filter_by(city_id=_id).first()
        citys_schema = CitySchema()
        return jsonify(citys_schema.dump(citys))
    except Exception as e:
        return jsonify(eror=str(e))    

@app.route('/city/add', methods=['POST'])
def add_city():
    body = request.json
    city = body.get('city')
    country_id = body.get('country_id')
    
    try:
        city = City(city,country_id)
        city_schema = CitySchema()
        db.session.add(city)
        db.session.commit()
        return jsonify(city_schema.dump(city))
    except Exception as e:
        return jsonify(eror=str(e))  

@app.route('/city/<_id>', methods=['PUT'])
def update_city(_id):
    body = request.json.get
    city = body('city')
    country_id = body('country_id')
    try:
        field = City.query.filter_by(city_id=_id).first()
        city_schema = CitySchema()
        field.city = city
        field.country_id = country_id
        db.session.commit()
        return jsonify(city_schema.dump(field))
    except Exception as e:
        return jsonify(eror=str(e))

@app.route('/city/<_id>', methods=['DELETE'])
def remove_city(_id):
    try:
        city = City.query.filter_by(city_id=_id).first()
        city_schema = CitySchema()
        db.session.delete(city)
        db.session.commit()
        return jsonify(data=city_schema.dump(city))
    except Exception as e:
        return jsonify(eror=str(e))

@app.route('/film/<_id>', methods=['GET'])
def get_film_by_id(_id):
    try:
        film = Film.query.filter_by(film_id=_id).first()
        film.film_actors = [item.actor_id for item in film.film_actor]
        return jsonify(film_schema.dump(film))
    except Exception as e:
        return jsonify(error=str(e))


if __name__ == '__main__':
    app.run(debug=True)