#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    response = make_response(
        '<h1>Zoo app</h1>',
        200
    )
    return response

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    response_body = f'''
        <h2>Animal ID: {animal.id}</h2>
        <ul><li>Name: {animal.name}</li><li>Species: {animal.species}</li></ul>
        <h3>Zookeeper</h3>
        <ul><li>Name: {animal.zookeeper.name}</li><li>Birthday: {animal.zookeeper.birthday}</li</ul>
        <h3>Enclosure</h3>
        <ul><li>Environment: {animal.enclosure.environment}</li><li>Open to Visitors: {animal.enclosure.open_to_visitors}</li></ul>

    '''
    response = make_response(response_body, 200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    response_body = f'''
        <h2>Zookeeper ID: {zookeeper.id}</h2>
        <ul><li>Name: {zookeeper.name}</li><li>Birthday: {zookeeper.birthday}</li></ul>
        <h3>Animals</h3>
    '''
    for animal in zookeeper.animals:
        response_body += f'<ul><li>Name: {animal.name}</li><li>Species: {animal.species}</li></ul>'
    
    response = make_response(response_body, 200)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    response_body = f'''
        <h2>Enclosure ID: {enclosure.id}</h2>
        <ul><li>Environment: {enclosure.environment}</li><li>Open to Visitors: {enclosure.open_to_visitors}</li></ul>
        <h3>Animals</h3>
    '''
    for animal in enclosure.animals:
        response_body += f'<ul><li>Name: {animal.name}</li><li>Species: {animal.species}</li></ul>'

    response = make_response(response_body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)