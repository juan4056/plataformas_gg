from flask import Flask, g, render_template, flash, url_for, redirect, abort, Response
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import json
from database import connector
import models
import forms




DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'elproyectowebdeplataformasdebeserseccreto'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """"Conecta a la base de datos antes de cada request"""
    g.db = models.DATABASE
    if g.db.is_closed():
        g.db.connect()
        g.user = current_user


@app.after_request
def after_request(response):
    """"Cerramos la conexion a la base de datos"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form. validate_on_submit():
        flash('Fuiste Registrado!!!', 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('Tu nombre de Usuaruo o contraseña no existe', 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Has inciado sesión', 'success')
                return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has salido de tu sesión', 'success')
    return redirect(url_for('index'))


@app.route('/ingreso', methods=('GET', 'POST'))
@login_required
def ingreso():
    ingresos= current_user.get_ingresos().limit(100)
    form = forms.IngresoForm()
    if form.validate_on_submit():
        models.Ingreso.create(user=g.user._get_current_object(),
                              name=form.name.data.strip(),
                              content=form.content.data)
        #flash('Ingreso añadido', 'success')
    return render_template('ingreso.html', form=form, ingresos=ingresos, page= "Ingresos")


@app.route('/gasto', methods=('GET', 'POST'))
@login_required
def gasto():
    gastos = current_user.get_gastos().limit(100)
    form = forms.GastoForm()
    if form.validate_on_submit():
        models.Gasto.create(user=g.user._get_current_object(),
                            name=form.name.data.strip(),
                            content=form.content.data)
        #flash('Gasto añadido', 'success')
    return render_template('gasto.html', form=form, gastos=gastos, page="Gastos")


@app.route('/documento')
@login_required
def documentos():
    return render_template('Documentos.html')


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/stream')
def stream():
    ingresos = models.Ingreso.select().limit(100)
    gastos = models.Gasto.select().limit(100)
    return render_template('stream.html', ingresos=ingresos, gastos=gastos)


#@app.route('/resumen')
#@app.route('/resumen/<username>')
#def resumen(username=None):
    #template = 'stream.html'
    #if username and username != current_user.username:
       # user =  models.User.select().where(models.User.username**username).get()
      #  ingresos = user.ingresos.limit(100)
     #   gastos = user.gastos.limit(100)
    #else:
     #   ingresos = current_user.get_ingresos().limit(100)
    #    gastos = current_user.get_gastos().limit(100)
   #     user = current_user
  #  if username:
 #       template = 'user_stream.html'
#    return render_template(template, ingresos=ingresos, gastos=gastos, user=user)

@app.route('/datos')
def datos():
    data=[]
    data_before={}
    gastos = current_user.get_gastos().limit(100)
    ingreso=current_user.get_ingresos().limit(100)
    ingreso_total=0
    gas_total=0
    for ing in ingreso:
        ingreso_total=ingreso_total+int(ing.content)
    for gas in gastos:
        if  gas.name in data_before:
            data_before[gas.name]=data_before[gas.name]+int(gas.content)
        else:
            data_before[gas.name]=int(gas.content)
        gas_total=gas_total+int(gas.content)
    for key in data_before:
        data.append({"gasto":key, "cantidad":data_before[key]})
    if ingreso_total>gas_total:
        data.append({"gasto":"Caja","cantidad":(ingreso_total-gas_total)})
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/home')
@login_required
def home():
    gastos = current_user.get_gastos().limit(100)
    ingreso = current_user.get_ingresos().limit(100)
    ingreso_total = 0
    gas_total = 0
    case=0
    for ing in ingreso:
        ingreso_total = ingreso_total + int(ing.content)
    for gas in gastos:
        gas_total = gas_total + int(gas.content)
    if ingreso_total > gas_total:
        case=1
    elif gas_total>ingreso_total:
        case=2
    elif gas_total==ingreso_total:
        case=3
    print(ingreso_total)
    print(gas_total)
    print(case)

    return render_template('home.html', page="Inicio", case=case)


if __name__ == '__main__':
    models.initialize()
    models.User.create_user(
        username='herless',
        email='herless.alvarado@utec.edu.pe',
        password='123qwe',
    )
    app.run(debug=DEBUG)