from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.secret_key = "algo-secreto"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comedor.db'
db = SQLAlchemy(app)

class Empleado(db.Model):
    id     = db.Column(db.Integer, primary_key=True)
    dni    = db.Column(db.String, unique=True, nullable=False)
    nombre = db.Column(db.String, nullable=False)

class Retiro(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    fecha       = db.Column(db.Date, nullable=False)
    importe     = db.Column(db.Float, nullable=False)
    empleado    = db.relationship('Empleado', backref='retiros')

# <-- creamos tablas apenas arranca la app
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dni     = request.form['dni'].strip()
        importe = request.form.get('importe', type=float)
        hoy     = date.today()
        emp     = Empleado.query.filter_by(dni=dni).first()

        if not emp:
            flash("DNI no registrado", "error")
            return redirect('/')

        if Retiro.query.filter_by(empleado_id=emp.id, fecha=hoy).first():
            flash("Ya retiraste hoy", "error")
            return redirect('/')

        db.session.add(Retiro(empleado_id=emp.id, fecha=hoy, importe=importe))
        db.session.commit()
        flash(f"Ok, {emp.nombre}: retiro registrado", "success")
        return redirect('/')

    return render_template('index.html')

@app.route('/registros')
def registros():
    hoy = date.today()
    lista = (Retiro.query
             .join(Empleado)
             .filter(Retiro.fecha == hoy)
             .all())
    return render_template('registros.html', lista=lista)

@app.route('/empleados', methods=['GET', 'POST'])
def empleados():
    if request.method == 'POST':
        dni    = request.form['dni'].strip()
        nombre = request.form['nombre'].strip()

        if Empleado.query.filter_by(dni=dni).first():
            flash("Ya existe un empleado con ese DNI", "error")
        else:
            db.session.add(Empleado(dni=dni, nombre=nombre))
            db.session.commit()
            flash("Empleado registrado", "success")
        return redirect('/empleados')

    todos = Empleado.query.order_by(Empleado.id).all()
    return render_template('empleados.html', empleados=todos)

@app.route('/empleados/delete/<int:id>', methods=['POST'])
def borrar_empleado(id):
    emp = Empleado.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    flash(f"Empleado {emp.nombre} borrado", "success")
    return redirect(url_for('empleados'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
