from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from dateutil import parser

app = Flask(__name__)
app.secret_key = "algo-secreto"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comedor.db'
db = SQLAlchemy(app)

class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String, unique=True, nullable=False)
    nombre = db.Column(db.String)

class Retiro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    importe = db.Column(db.Float, nullable=False)
    empleado = db.relationship('Empleado')

@app.before_first_request
def init_db():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        dni = request.form['dni']
        importe = float(request.form['importe'])
        hoy = date.today()
        emp = Empleado.query.filter_by(dni=dni).first()
        if not emp:
            flash("DNI no registrado", "error")
            return redirect('/')
        # chequeo retiro único
        existe = Retiro.query.filter_by(empleado_id=emp.id, fecha=hoy).first()
        if existe:
            flash("Ya retiraste hoy", "error")
        else:
            retiro = Retiro(empleado_id=emp.id, fecha=hoy, importe=importe)
            db.session.add(retiro)
            db.session.commit()
            flash(f"Ok, {emp.nombre}: retiro registrado", "success")
        return redirect('/')
    return render_template('index.html')

@app.route('/registros')
def registros():
    hoy = date.today()
    lista = Retiro.query.filter_by(fecha=hoy).all()
    return render_template('registros.html', lista=lista)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
