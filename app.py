import os  # Añadimos esta importación
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Vamos a crear un diccionario para simular la base de datos
url_db = {}

# Página principal
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Acortador de URL</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f4f8;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                }
                .container {
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 100%;
                    max-width: 400px;
                }
                h1 {
                    text-align: center;
                    color: #333;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 2px solid #ddd;
                    border-radius: 4px;
                    font-size: 16px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    width: 100%;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }
                button:hover {
                    background-color: #45a049;
                }
                footer {
                    position: fixed;
                    bottom: 10px;
                    width: 100%;
                    text-align: center;
                    font-size: 14px;
                    color: #777;
                }
                footer a {
                    color: #4CAF50;
                    text-decoration: none;
                }
                footer a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Acortador de URL</h1>
                <form action="/shorten" method="POST">
                    <label for="url">Introduce una URL:</label>
                    <input type="text" name="url" id="url" required placeholder="Ejemplo: https://www.ejemplo.com">
                    <button type="submit">Acortar URL</button>
                </form>
            </div>
            <footer>
                <p>Hecho por <a href="https://github.com/anagsdp" target="_blank">Ana Gómez</a></p>
            </footer>
        </body>
        </html>
    """)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    
    short_code = 'out.' + str(len(url_db) + 1)
    
    url_db[short_code] = original_url
    
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>URL Acortada</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f4f8;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                }
                .container {
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 100%;
                    max-width: 400px;
                    text-align: center;
                }
                h1 {
                    color: #333;
                }
                .result {
                    margin-top: 20px;
                    font-size: 18px;
                }
                .result a {
                    color: #007bff;
                    text-decoration: none;
                    font-weight: bold;
                }
                .result a:hover {
                    text-decoration: underline;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    margin-top: 20px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }
                button:hover {
                    background-color: #45a049;
                }
                footer {
                    position: fixed;
                    bottom: 10px;
                    width: 100%;
                    text-align: center;
                    font-size: 14px;
                    color: #777;
                }
                footer a {
                    color: #4CAF50;
                    text-decoration: none;
                }
                footer a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>¡Tu URL ha sido acortada!</h1>
                <div class="result">
                    <p>URL acortada: <a href="/{{ short_code }}" target="_blank">/{{ short_code }}</a></p>
                    <form action="/" method="GET">
                        <button type="submit">Volver a empezar</button>
                    </form>
                </div>
            </div>
            <footer>
                <p>Hecho por <a href="https://github.com/anagsdp" target="_blank">Ana Gómez</a></p>
            </footer>
        </body>
        </html>
    """, short_code=short_code)

# Ruta para redirigir a la URL original usando el código corto
@app.route('/<short_code>')
def redirect_to_url(short_code):
    original_url = url_db.get(short_code)
    if original_url:
        return redirect(original_url)
    else:
        return 'URL no encontrada', 404

# Aquí es donde se inicia la aplicación con la configuración para Heroku
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Heroku asigna el puerto a través de la variable de entorno 'PORT'
    app.run(host='0.0.0.0', port=port, debug=True)
