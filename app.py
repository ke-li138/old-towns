from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

# Configure application
app = Flask(__name__, template_folder='templates')

# Use database test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Use Table Oldtowns
class Oldtowns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Numeric, unique=False, nullable=False)
    lng = db.Column(db.Numeric, unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    pic = db.Column(db.String(80), unique=False, nullable=False) 
    intro = db.Column(db.String(200), unique=False, nullable=False)

    def __repr__(self):
        return '<OldTown %r>' % self.name

class Snacks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    pic = db.Column(db.String(80), unique=False, nullable=False)
    intro = db.Column(db.String(200),unique=False, nullable=False)
    def __repr__(self):
        return '<Snack %r>' % self.name

class Crafts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    pic = db.Column(db.String(80), unique=False, nullable=False)
    intro = db.Column(db.String(200),unique=False, nullable=False)
    def __repr__(self):
        return '<Craft %r>' % self.name

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    locSQL = Oldtowns.query.all()
    locs = []
    for loc in locSQL:
        location = {}
        location['name'] = loc.name
        location['lat'] = loc.lat
        location['lng'] = loc.lng
        location['pic'] = loc.pic
        locs.append(location)
    return render_template("index.html",locs=locs)

#The mainpage of old towns
@app.route("/OldTowns")
def OldTowns():
    locSQL = Oldtowns.query.all()
    locs = []
    for loc in locSQL:
        location = {}
        location['name'] = loc.name
        location['lat'] = loc.lat
        location['lng'] = loc.lng
        location['pic'] = loc.pic
        location['intro'] = loc.intro
        locs.append(location)
    return render_template("OldTowns/OldTowns.html",locs=locs)

#Specific introduction to each old town
@app.route("/OldTowns/info", methods=["POST"])
def OldTowns_info():
    locSQL = Oldtowns.query.all()
    name = request.form.get('name')
    loc = {}
    for location in locSQL:
        if name == location.name:
            loc['name'] = location.name
            loc['lat'] = location.lat
            loc['lng'] = location.lng
            loc['pic'] = location.pic
            loc['intro'] = location.intro
    return render_template("OldTowns/Model.html",loc=loc)

@app.route("/Snacks")
def snacks():
    locSQL = Snacks.query.all()
    locs = []
    for loc in locSQL:
        location = {}
        location['name'] = loc.name
        location['pic'] = loc.pic
        location['intro'] = loc.intro
        locs.append(location)
    return render_template("Snacks/Snacks.html",locs=locs)

@app.route("/Snacks/info", methods=["POST"])
def Snacks_info():
    locSQL = Snacks.query.all()
    name = request.form.get('name')
    loc = {}
    for location in locSQL:
        if name == location.name:
            loc['name'] = location.name
            loc['pic'] = location.pic
            loc['intro'] = location.intro
    return render_template("Snacks/Model.html",loc=loc)

@app.route("/Crafts")
def crafts():
    locSQL = Crafts.query.all()
    locs = []
    for loc in locSQL:
        location = {}
        location['name'] = loc.name
        location['pic'] = loc.pic
        location['intro'] = loc.intro
        locs.append(location)
    return render_template("Crafts/Crafts.html",locs=locs)

@app.route("/Crafts/info", methods=["POST"])
def Crafts_info():
    locSQL = Crafts.query.all()
    name = request.form.get('name')
    loc = {}
    for location in locSQL:
        if name == location.name:
            loc['name'] = location.name
            loc['pic'] = location.pic
            loc['intro'] = location.intro
    return render_template("Crafts/Model.html",loc=loc)

@app.route("/Me/add", methods=["POST","GET"])
def add():
    success = None
    if request.method == "GET":
        return render_template("Me/add.html")
    else:
        name = request.form.get('name')
        uploaded_file = request.files['pic']
        if not uploaded_file.filename or not name or not request.form.get('type'):
            message = "Please Enter All The Required Information!"
            success = 'success'
            return render_template("Me/add.html", message=message, success=success)
        else:
             intro = request.form.get('intro')

             # If blogs are for old towns
             if request.form.get('type') == 'OldTowns':
                if not request.form.get('lat') or not request.form.get('lng'):
                    message = "Please Enter All The Required Information!"
                    success = 'success'
                    return render_template("Me/add.html", message=message, success=success)
                else:
                    lat = float(request.form.get('lat'))
                    lng = float(request.form.get('lng'))
                    route = 'static/images/OldTowns/' + uploaded_file.filename
                    uploaded_file.save(route)
                    pic = '../../' + route
                    db.session.add(Oldtowns(name=name, lat=lat, lng=lng, intro=intro, pic=pic))
                    db.session.commit()
                    message = 'You have successfully blogged! Thanks!'
                    success = 'success'
                    return render_template("Me/add.html", message=message, success=success)

            # If blogs are for Snacks
             if request.form.get('type') == 'Snacks':
                    route = 'static/images/Snacks/' + uploaded_file.filename
                    uploaded_file.save(route)
                    pic = '../../' + route
                    db.session.add(Snacks(name=name, intro=intro, pic=pic))
                    db.session.commit()
                    message = 'You have successfully blogged! Thanks!'
                    success = 'success'
                    return render_template("Me/add.html", message=message, success=success)

            # If blogs are for Crafts
             if request.form.get('type') == 'Crafts':
                    route = 'static/images/Crafts/' + uploaded_file.filename
                    uploaded_file.save(route)
                    pic = '../../' + route
                    db.session.add(Crafts(name=name, intro=intro, pic=pic))
                    db.session.commit()
                    message = 'You have successfully blogged! Thanks!'
                    success = 'success'
                    return render_template("Me/add.html", message=message, success=success)

