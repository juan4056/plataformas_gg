from flask import Flask,render_template,session,request, jsonify, Response, redirect,url_for
from sqlalchemy import or_, and_

from model import entities
from database import connector
import json

app = Flask(__name__)
db = connector.Manager()

cache = {}
engine = db.createEngine()

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/index')
def index():
    return render_template('login_register.html')

@app.route('/')
def i():
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    usuario=request.form['Username']
    contraseña=request.form['Password']
    sessiondb=db.getSession(engine)
    user = sessiondb.query(entities.User).filter(
        and_(entities.User.username == usuario, entities.User.password == contraseña)
    ).first()
    if user!= None:
        session['logged']=user.id
        return redirect(url_for('inicio'))
    else:
        redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    usuario = request.form['Username']
    contraseña = request.form['Password']
    nombre=request.form['Fullname']
    correo=request.form['Email']
    cel=request.form['Celular']
    sessiondb = db.getSession(engine)
    user = sessiondb.query(entities.User).filter(
        and_(entities.User.username == usuario)
    ).first()
    if user==None:
        new_user=entities.User(
            fullname = nombre,
            password = contraseña,
            username = usuario,
            email = correo,
            celular = cel,
        )
        sessiondb.add(new_user)
        sessiondb.commit()
        return redirect(url_for('inicio'))

    return "no válido"

@app.route('/users', methods = ['GET'])
def get_users():

    key = 'getUsers'
    if key not in cache.keys():
        session = db.getSession(engine)
        dbResponse = session.query(entities.User)
        cache[key] = dbResponse
        print("From DB")
    else:
        print("From Cache")

    users = cache[key]
    data = []
    for user in users:
        data.append(user)

    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/logged')
def logged():
    fa=session['logged']

    return Response(json.dumps(fa, cls=connector.AlchemyEncoder), mimetype='application/json')
@app.route('/Inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/Ingresos')
def ingresos():
    if 'success' in session:
        if session['success']:
            conn = engine.connect()
            res = conn.execute("select id, ingreso from ingresos")
            result = {'tipo': 0, 'datos': []}
            for ing in res:
                result['tipo'] = 1
                result['datos'].append({'id': ing['id'], 'nombre': ing['nombre']})
            res.close()
            conn.close()
            return json.dumps(result)
    return render_template('Ingresos.html')

@app.route('/Gastos')
def gastos():
    return render_template('Gastos.html')

@app.route('/Documentos')
def documentos():
    return render_template('Documentos.html')

@app.route('/Configuración')
def configuracion():
    return render_template('Configuración.html')

@app.route('/Salir')
def salir():
    session['logged']=0
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(debug=True)