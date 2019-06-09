from flask import Flask, jsonify, request, render_template, g, Blueprint
from apps.database import db, Orbit, System, Types, Body, Physic
from apps.app import create_app

# bp = Blueprint('astrarium', __name__, url_prefix="/astrarium/")

app = create_app()

def _getEngine():
    engine = db.create_engine('sqlite:///astrarium.db')
    connection = engine.connect()
    return connection

def getBody(bodyId):
    connection = _getEngine()
    query = db.select([Body]).where(Body.id == bodyId)
    ResultProxy = connection.execute(query)
    result = ResultProxy.first()
    return result;

@app.route('/orbits')
def orbits():
    connection = _getEngine()
    query = db.select([Orbit])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    results = [dict(row) for row in ResultSet]

    return jsonify({
        'results': results,
        'len': len(ResultSet)
    })

@app.route('/bodies')
def bodies():
    connection = _getEngine()
    query = db.select([Body])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    results = [dict(row) for row in ResultSet]

    return jsonify({
        'results': results,
        'len': len(ResultSet)
    })

@app.route('/systems')
def systems():
    connection = _getEngine()
    query = db.select([System])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    results = [dict(row) for row in ResultSet]

    return jsonify({
        'results': results,
        'len': len(ResultSet)
    })

@app.route('/types')
def types():
    connection = _getEngine()
    query = db.select([Types])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    results = [dict(row) for row in ResultSet]

    return jsonify({
        'results': results,
        'len': len(ResultSet)
    })

@app.route('/physics')
def physics():
    connection = _getEngine()
    query = db.select([Physic])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    results = [dict(row) for row in ResultSet]

    return jsonify({
        'results': results,
        'len': len(ResultSet)
    })
