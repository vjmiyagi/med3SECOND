import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from recco import recommend 



app = Flask(__name__)


ENV = "dev"


if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1386waxedoff@localhost/med'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Med(db.Model):
    __tablename__ = 'med_mj'
    strain_id = db.Column(db.Integer, primary_key=True)
    strain = db.Column(db.String(30), unique=True)
    species = db.Column(db.String(6))
    rate = db.Column(db.Numeric)
    effect = db.Column(db.String(46))
    flavor = db.Column(db.String(30))

    def __init__(self, strain, species, rate, effect, flavor):
        self.strain = strain
        self.species = species
        self.rate = rate
        self.effect = effect
        self.flavor = flavor


class Species(db.Model):
    __tablename__ = 'species'
    species_id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(6), unique=True)

    def __init__(self, species):
        self.species = species


class Strain(db.Model):
    __tablename__ = 'strain'
    strain_id = db.Column(db.Integer, primary_key=True)
    strain = db.Column(db.String(30), unique=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.species_id'))
    species = db.relationship('Species', backref=db.backref('species', lazy='joined'))
    rate = db.Column(db.Numeric)

    def __init__(self, strain, species, rate):
        self.strain = strain
        self.species = species
        self.rate = rate


class Effect(db.Model):
    __tablename__ = 'effect'
    effect_id = db.Column(db.Integer, primary_key=True)
    effect = db.Column(db.String(9))

    def __init__(self, effect):
        self.effect = effect


class Flavor(db.Model):
    __tablename__ = 'flavor'
    flavor_id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(12))

    def __init__(self, flavor):
        self.flavor = flavor


class StrainEffect(db.Model):
    __tablename__ = 'straineffect'
    se_id = db.Column(db.Integer, primary_key=True)
    strain_id = db.Column(db.Integer, db.ForeignKey('strain.strain_id'))
    strain = db.relationship("Strain", backref=db.backref('strain', lazy='joined'))
    effect_id = db.Column(db.Integer, db.ForeignKey('effect.effect_id'))
    effect = db.relationship("Effect", backref=db.backref('effect', lazy='joined'))

    def __init__(self, strain, effect):
        self.strain = strain
        self.effect = effect


class StrainFlavor(db.Model):
    __tablename__ = 'strainflavor'
    sf_id = db.Column(db.Integer, primary_key=True)
    strain_id = db.Column(db.Integer, db.ForeignKey('strain.strain_id'))
    strain = db.relationship("Strain", backref=db.backref('strain', lazy='joined'))
    flavor_id = db.Column(db.Integer, db.ForeignKey('flavor.flavor_id'))
    flavor = db.relationship("Flavor", backref=db.backref('flavor', lazy='joined'))

    def __init__(self, strain, flavor):
        self.strain = strain
        self.flavor = flavor


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendation',methods=['GET'])
def recommendation():    
    species = str(request.args['species'])
    flavor = str(request.args['flavor'])
    effect = str(request.args['effect'])    
    whatever = ' '.join([species, effect, flavor])
    s = recommend(whatever)

    return json.dumps(s)
