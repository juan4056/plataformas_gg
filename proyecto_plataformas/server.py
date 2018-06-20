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
        return redirect(url_for('index'))

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
@app.route('/prueba', methods=['GET'])
def prueba():
    js=[{"id":1,"region":"africa","val":123},{"id":2,"region":"asia","val":123},{"id":3,"region":"hola","val":123},{"id":4,"region":"xd","val":123}]
    return Response(json.dumps(js), mimetype='application/json')

#AHORROS
@app.route('/ahorross', methods = ['GET'])
def get_messages():
    session = db.getSession(engine)
    ahorross = session.query(entities.ahorros)
    data = []
    for message in ahorross:
        data.append(message)

    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/ahorross/<id>', methods = ['GET'])
def get_message(id):
    session = db.getSession(engine)
    messages = session.query(entities.ahorros).filter(entities.ahorros.id == id)
    for message in messages:
        js = json.dumps(message, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    response = { "status": 404, "ahorros": "Not Found"}
    return Response(response, status=404, mimetype='application/json')


@app.route('/ahorross', methods = ['DELETE'])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.ahorros).filter(entities.ahorros.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return "Deleted Message"


@app.route('/ahorross', methods = ['POST'])
def create_message():
    #c =  json.loads(request.form['values'])
    c = request.get_json(silent=True)
    session = db.getSession(engine)
    user_from = session.query(entities.User).filter(entities.User.id == c["user_from_id"]).first()

    message = entities.ahorros(
        user_from = user_from,
        nombre=c['nombre'],
        cant=c['cant'],
    )
    session.add(message)
    session.commit()
    return 'Created Message'


@app.route('/ahorross', methods = ['PUT'])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated Message'

#fin



@app.route('/getahorros/<id>', methods=['GET'])
def getahorros(id):
    user_from_id=id
    session = db.getSession(engine)
    messages = session.query(entities.ahorros).filter(
        or_(
            and_(entities.ahorros.user_from_id == user_from_id)
        )
    )
    data = []
    for message in messages:
        data.append(message)

    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')
@app.route('/chats', methods = ['GET'])
def get_chats():
    sessiondb = db.getSession(engine)
    user_id = session['logged']
    chats = sessiondb.query(entities.ahorros.user_to_id).filter(entities.ahorros.user_from_id == user_id).distinct()
    data = []
    for message in chats:
        user = sessiondb.query(entities.User).filter(entities.User.id == message[0]).first()
        data.append(user)



    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')
@app.route('/current', methods = ['GET'])
def current():
    sessiondb = db.getSession(engine)
    user = sessiondb.query(entities.User).filter(entities.User.id == session['logged']).first()
    js = json.dumps(user, cls=connector.AlchemyEncoder)
    return Response(js, status=200, mimetype='application/json')


@app.route('/logged')
def logged():
    fa=session['logged']

    return Response(json.dumps(fa, cls=connector.AlchemyEncoder), mimetype='application/json')
@app.route('/Inicio')
def inicio():
    return redirect(url_for('static_content',content="inicio.html"))

@app.route('/ingreso', methods=['POST'])
def nuevoIngreso():
    name = request.form['inputIngreso']
    cant = request.form['cantidad']
    sessiondb = db.getSession(engine)
    ingreso = sessiondb.query(entities.Ingresos).filter(
        and_(entities.Ingresos.nombre == name)
    ).first()
    if ingreso == None:
        newingreso = entities.Ingresos(
            nombre=name,
            cant=cant,
        )
        sessiondb.add(newingreso)
        sessiondb.commit()
        return redirect(url_for('ingresos'))

    return "no válido"

@app.route('/Ingresos')
def ingresos():
    return render_template('Ingresos.html')

@app.route('/gasto', methods=['POST'])
def gasto():
    name = request.form['inputGasto']
    cant = request.form['cantidad']
    sessiondb = db.getSession(engine)
    gasto = sessiondb.query(entities.Gastos).filter(
        and_(entities.Gastos.nombre == name)
    ).first()
    if gasto == None:
        newgasto = entities.Gastos(
            nombre=name,
            cant=cant,
        )
        sessiondb.add(newgasto)
        sessiondb.commit()
        return redirect(url_for('gastos'))

    return "no válido"

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