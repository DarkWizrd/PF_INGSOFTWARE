from flask import Flask, render_template
from sentiments import second
app = Flask(__name__)
# Blueprint para llamar al segundo archivo de Python en el proyecto.
app.register_blueprint(second)
@app.route('/')# Definición de la ruta para la página principal (es la pagina que se ejecuta cuando se inicia la app)
@app.route('/home')# Definición de la ruta para la página de inicio
def home():
    return render_template('home.html')  # Incluye return para renderer la plantilla

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=10000, debug=False)
   # Debug=False, ahora esta en producción
   #app.run(debug=True)