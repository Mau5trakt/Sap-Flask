from flask import Flask, render_template, request
from flask_migrate import Migrate
from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

USER_DB = 'curso'
PASS_DB = 'curso'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

#configurar flask migrate
migrate = Migrate()
migrate.init_app(app, db)


#configuracion de flask wtf
app.config['SECRET_KEY']='llave_secreta' #tiene que ser realmente secreta


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():  # put application's code here
    #listado de personas
    personas = Persona.query.all()
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado de personas: {personas} ')
    app.logger.debug(f'Total  de personas: {total_personas} ')


    return render_template('index.html', personas=personas, total_personas=total_personas)

@app.route('/ver/<int:id>')
def ver_detalle(id):
    #recuperamos la persona segun el id proporcionado
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'ver persona: {persona}')
    return render_template('detalle.html', persona=persona)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    persona = Persona()
    personaForm = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            app.logger.debug(f'Persona a agregar: {persona}')

        #insertamos el nuevo registro
        db.session.add(persona)
        db.session.commit() #es, raro es tipo git


    return render_template('agregar.html', forma = personaForm)




if __name__ == '__main__':
    app.run()
