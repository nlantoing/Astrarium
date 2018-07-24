from flask_sqlalchemy import SQLAlchemy
import contextlib

db = SQLAlchemy()

@contextlib.contextmanager
def db_context(app):
    if app is None:
        from app import create_app
        app = create_app()
    with app.app_context():
        yield

def init_db(app=None):
    """ Initialize the database """
    with db_context(app):
        db.create_all()

class System(db.Model):
    """ Star object definition """
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    barycentre_id = db.Column(db.Integer, db.ForeignKey('Barycentre.id'), unique=True)

class Orbit(db.Model):
    """ The 6 necessary orbital element to define an orbit """
    __tablename__ = 'orbits'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Integer, db.ForeignKey('Body.id'))
    barycentre = db.Column(db.Integer, db.ForeignKey('Barycentre.id'))
    #elipse shape
    eccentricity = db.Column(db.Integer, nullable=False)
    semiMajorAxis = db.Column(db.Integer, nullable=False)
    #orientation of orbital plane
    inclination = db.Column(db.Integer, nullable=False)
    longAscNode = db.Column(db.Integer, nullable=False)
    #orientation of elipse in orbital plane
    ArgPeriapsis = db.Column(db.Integer, nullable=False)
    #body position at epoch (2000-Jan-01 00:00
    epochTrueAnomaly = db.Column(db.Integer)

class Barycentre(db.Model):
    """ Barycentres databases """
    __tablename__ = 'barycentres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    
class Body(db.Model):
    """ Contain the basic physic informations of an astronomical body  """
    __tablename__ = 'bodies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    primaryBody = db.relationship('Body', backref='satelites')
    barycentre = db.relationship('Barycentre', backref='members') 

    #Physics and body characteristics, TODO: moveme to another table (specific to the body type : planet/stars/comets etc)
    mass = db.Column(db.Integer)
    density = db.Column(db.Integer)
    equatRadius = db.Column(db.Integer)
    meanRadius = db.Column(db.Integer)
    polarRadius = db.Column(db.Integer)
    flatterning = db.Column(db.Integer)
    volumetricMeanRadius = db.Column(db.Integer)
    escapeVelocity = db.Column(db.Integer)
    rotationPeriod = db.Column(db.Integer)
    axialTilt = db.Column(db.Integer)
    northPRightAsc = db.Column(db.Integer)
    northPDeclination = db.Column(db.Integer)
