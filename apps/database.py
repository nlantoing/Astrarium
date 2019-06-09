from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps.app import create_app
from apps.horizons import Horizons
import contextlib
import click

db = SQLAlchemy()

@contextlib.contextmanager
def db_context(app):
    if app is None:
        app = create_app()
    with app.app_context():
        yield

def init_db(app=None):
    """ Initialize the database """
    with db_context(app):
        db.create_all()

def create_orbit(body,bary,orbit):
    """ Generate an orbit entry"""
    entry = Orbit(
        body = body,
        barycentre = bary,
        eccentricity = orbit['eccentricity'],
        semiMajorAxis = orbit['semi_major_axis'],
        inclination = orbit['inclination'],
        longAscNode = orbit['long_of_asc_node'],
        argPeriapsis = orbit['arg_of_periapsis'],
        epochTrueAnomaly = orbit['true_anomaly']
    )
    db.session.add(entry)                        


def drop_all(app=None):
    engine = db.create_engine('sqlite:///astrarium.db')
    connection = engine.connect()
    metadata = db.MetaData()
    metadata.drop_all(engine)
    

def populate_db_hztn(app=None):
    """ Populate the database with basics data from JPL horizons telnet service """
    #TODO: Check if entries exist before adding it
    with db_context(app):
        hztn = Horizons()
        barycentres = hztn.get_barycenters()
        solarBarycenter = Body(name=barycentres[0][1])
        db.session.add(solarBarycenter)
        solarsystem = System(
            name = "Solar System",
            barycentre_id = solarBarycenter.id
        )
        db.session.add(solarsystem)
        
        #commit changes   
        db.session.commit()
        
        print("Getting Barycenters list...")
        for bary in barycentres:
            if(bary[0]):
                barycenter = Body(name=bary[1])
                db.session.add(barycenter)

                #commit changes   
                db.session.commit()
                
                print (bary[1])
                print("Getting barycenter members list...")
                members = hztn.get_barycenter_members(bary[0])
                if(len(members) > 1):
                    print("Getting satelites orbits...")
                    for body in members:
                        satelite = Body(name=body[1])
                        db.session.add(satelite)

                        #commit changes   
                        db.session.commit()
                        
                        print(body[1])
                        orbit = hztn.get_orbit(body[0],bary[0])
                        create_orbit(satelite.id, barycenter.id, orbit)
                
                print("Getting barycenter orbit...")
                orbit = hztn.get_orbit(bary[0],0)                
                create_orbit(barycenter.id, solarBarycenter.id, orbit)
            else:
                #special case : sun
                print("Getting sun orbit toward solarsystem barycenter...")
                orbit = hztn.get_orbit(10,0)
                sun = Body(name="Sun")
                db.session.add(sun)
                
                #commit changes   
                db.session.commit()
                
                create_orbit(sun.id, solarBarycenter.id, orbit)

            #commit changes   
            db.session.commit()

class System(db.Model):
    """ Star object definition """
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    barycentre_id = db.Column(db.Integer, db.ForeignKey('bodies.id'), unique=True)

class Orbit(db.Model):
    """ The 6 necessary orbital element to define an orbit """
    __tablename__ = 'orbits'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Integer, db.ForeignKey('bodies.id'))
    barycentre = db.Column(db.Integer, db.ForeignKey('bodies.id'))
    #elipse shape
    eccentricity = db.Column(db.Integer, nullable=False)
    semiMajorAxis = db.Column(db.Integer, nullable=False)
    #orientation of orbital plane
    inclination = db.Column(db.Integer, nullable=False)
    longAscNode = db.Column(db.Integer, nullable=False)
    #orientation of elipse in orbital plane
    argPeriapsis = db.Column(db.Integer, nullable=False)
    #body position at epoch (2000-Jan-01 00:00
    epochTrueAnomaly = db.Column(db.Integer)

class Types(db.Model):
    """ Types : star, barycentre, planet etc """
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    
class Body(db.Model):
    """ Contain the basic physic informations of an astronomical body  """
    __tablename__ = 'bodies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    #primaryBody = db.relationship('Body', backref='satelites')
    type = db.Column(db.Integer, db.ForeignKey('types.id') )
    physical_properties = db.Column(db.Integer, db.ForeignKey('physics.id'))

class Physic(db.Model):
    """ Physica properties """
    __tablename__ = 'physics'
    id = db.Column(db.Integer, primary_key=True)
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

if __name__ == '__main__':
    app = create_app()
    with db_context(app):
        migrate = Migrate(app,db)
        manager = Manager(app)
        manager.add_command('db',MigrateCommand)
        manager.run()
