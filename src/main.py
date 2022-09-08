"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BACKEND_URL_BASE = os.environ.get('')
# configuracion de jwt
app.config["JWT_SECRET_KEY"] = "dbckjbdfkjdfvbn"  # Change this!
jwt = JWTManager(app)



MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
 
url_base="https://swapi.dev/api"
 
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code



# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():

    all_users = User.query.all()
    results = []
    for user in all_users:
        results.append(user.serialize())
    return jsonify({"results":results})

    return jsonify(response_body), 200
#mandar un user y un password, 
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/people', methods=['GET'])
def get_people():
    #consultar todos los personajes
    personajes = requests.get(f'{url_base}/people?page=1&limit=1000')
    #devolver personas serializadas
    response = personajes.json()
    return jsonify(response), 200
    
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    data = requests.get(f'{url_base}/people/{people_id}')
    #consultar un id especifico y guardar esa informacion en la variable person
    #mostrar la información del id y si no se encuentra el id, arrojar un warning de que no se encuentra registrado
    persona = data.json()
    return jsonify({"result":persona}),200
    
@app.route('/planets', methods=['GET'])
def get_planet():
    # consultar todos los planetas en DB
    planetas = requests.get(f'{url_base}/planets?page=1&limit=1000')
    # devolver planetas serializados
    response = planetas.json()
    return jsonify(response), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planetid(planet_id):
    
    # consultar todos los planeta individual en DB
    planeta = requests.get(f'{url_base}/planets/{planet_id}')
    #si no se encuentra devolver alerta de que no se encuentra ese registro
    
    # devolver planeta serializado
    response = planeta.json()
    return jsonify(response), 200

@app.route('/favorite/<string:type>', methods=['POST'])
def post_favorite(type):
    #esta ruta va a se JWT requiere
    body = request.json
    user_id = body['userId']
    user_name = body['name']
    type_id = body['typeId']
    url = f'https://3000-4geeksacade-flaskresthe-lglnrq27dx0.ws-us64.gitpod.io/{type}/{type_id}'
    new_favorite = Favorite(
        name = user_name,
        url = url,
        user_id = user_id
    ) 
    db.session.add(new_favorite)
    try:
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201
    except Exception as error:
        db.session.rollback()
        return jsonify(error.args), 500   
    
@app.route('/users/favorites', methods=['GET'])
def user_favorites():
    user_id = 1
    favorites = Favorite.query.filter_by(user_id = user_id)
    result = list(map(lambda favorite:favorite.serialize(),favorites))
    return jsonify(result), 200

@app.route('/favorites/<int:favorite_id', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.filter_by(id= favorite_id).one_or_none()
    if favorite is None:
        return jsonify({"message": 'Usuario no encontrado'}), 404
    deleted = favorite.delete()
    if deleted is True:
        return jsonify([]), 204    
    return jsonify({"message":'Ocurrio un error'}), 500

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
