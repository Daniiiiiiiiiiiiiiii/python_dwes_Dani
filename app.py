from flask import Flask, render_template, flash, request, Response, jsonify, redirect, url_for
from database import app, db, JugadorSchema
from jugador import Jugador

jugador_schema = JugadorSchema()
jugador_schema = JugadorSchema(many=True)

app.app_context().push()
db.create_all()

@app.route('/')
def home():
    jugador = Jugador.query.all()
    jugadoresLeidos = jugador_schema.dump(jugador)
    
    return render_template('index.html', jugador = jugadoresLeidos)

    # return jsonify(estudiantesLeidos)

#Method Post
@app.route('/jugadores', methods=['POST'])
def addJugador():
    nombre = request.form['nombre']
    edad = request.form['edad']
    club = request.form['club']

    if nombre and edad and club:
        nuevo_jugador = Jugador(nombre, edad, club)
        db.session.add(nuevo_jugador)
        db.session.commit()
        response = jsonify({
            'nombre' : nombre,
            'edad' : edad,
            'club' : club
        })
        return redirect(url_for('home'))
    else:
        return notFound()

#Method delete
@app.route('/delete/<id>')
def deleteJugador(id):
    jugador = Jugador.query.get(id)
    db.session.delete(jugador)
    db.session.commit()
    
    flash('Jugador ' + id + ' eliminado correctamente')
    return redirect(url_for('home'))

#Method Put
@app.route('/edit/<id>', methods=['POST'])
def editJugador(id):    
    
    nombre = request.form['nombre']
    edad = request.form['edad']
    club = request.form['club']
    
    if nombre and edad and club:
        jugador = Jugador.query.get(id)
  # return student_schema.jsonify(student)
        jugador.nombre = nombre
        jugador.edad = edad
        jugador.club = club
        
        db.session.commit()
        
        response = jsonify({'message' : 'Jugador ' + id + ' actualizado correctamente'})
        flash('Jugador ' + id + ' modificado correctamente')
        return redirect(url_for('home'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)