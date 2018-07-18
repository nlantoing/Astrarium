from flask import Flask, jsonify, request, render_template, g, Blueprint
from database import db

bp = Blueprint('astrarium', __name__, url_prefix="/astrarium/")
