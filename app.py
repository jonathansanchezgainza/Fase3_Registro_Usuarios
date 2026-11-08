from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re

usuarios = []

class Servidor(BaseHTTPRequestHandler):

    def do_POST(self):

        if self.path == "/registro_usuario":

            longitud = int(self.headers.get("Content-Length", 0))
            datos = self.rfile.read(longitud)

            try:
                usuario = json.loads(datos)

                email = usuario.get("email", "")
                password = usuario.get("password", "")

                # Validar campos
                if not isinstance(email, str) or not isinstance(password, str):
                    self.responder(400, {"error": "Datos incorrectos ingresar los datos correctos"})
                    return

                email = email.strip()

                if not email or not password:
                    self.responder(400, {"error": "Campos obligatorios"})
                    return

                # Validar email
                patron = r'^[\w.-]+@[\w.-]+\.\w+$'

                if not re.fullmatch(patron, email):
                    self.responder(400, {"error": "Email no válido"})
                    return

                # Validar contraseña
                if (len(password) < 8 or
                    not re.search(r'[A-Z]', password) or
                    not re.search(r'[a-z]', password) or
                    not re.search(r'[0-9]', password)):

                    self.responder(400, {
                        "error": "Contraseña insegura"
                    })
                    return

                # Evitar correos duplicados
                if email in usuarios:
                    self.responder(409, {
                        "error": "El usuario ya existe"
                    })
                    return

                usuarios.append(email)

                self.responder(201, {
                    "mensaje": "Usuario registrado correctamente",
                    "email": email
                })

            except (json.JSONDecodeError, AttributeError):
                self.responder(400, {"error": "JSON inválido"})

        else:
            self.responder(404, {"error": "Ruta no encontrada"})

    def responder(self, codigo, respuesta):

        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(
            json.dumps(respuesta).encode("utf-8")
        )


servidor = HTTPServer(("localhost", 5000), Servidor)

print("Servidor iniciado en http://localhost:5000")
print("API: POST /registro_usuario")

servidor.serve_forever()
