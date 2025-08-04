from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comedor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# activar FK en SQLite para que ondelete CASCADE funcione
@app.before_serving
def _activate_fks():
    db.engine.execute('PRAGMA foreign_keys=ON')

class Empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    # ...otros campos...
    retiros = db.relationship(
        'Retiro',
        backref='empleado',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class Retiro(db.Model):
    __tablename__ = 'retiro'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # ...otros campos...
    empleado_id = db.Column(
        db.Integer,
        db.ForeignKey('empleado.id', ondelete='CASCADE'),
        nullable=False
    )

@app.route('/')
def lista_empleados():
    empleados = Empleado.query.all()
    return render_template('lista.html', empleados=empleados)

@app.route('/empleados/delete/<int:id>', methods=['POST'])
def borrar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    db.session.delete(empleado)
    db.session.commit()
    return redirect(url_for('lista_empleados'))

# ...el resto de tus rutas...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
