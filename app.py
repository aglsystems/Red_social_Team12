import hashlib
from flask import Flask,render_template,request,jsonify, redirect, session
#Importa la libreria de SQLITE
import sqlite3
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
FOLDER_IMAGES = 'static/img/'
# SESSION_TYPE = 'filesystem'
# app.config.from_object(__name__)
# session(app)
app.secret_key = os.urandom(24)

# Endpoint para cargar formulario Usuarios
@app.route("/",methods=["get"])
def home():
    return render_template("login.html")

# Procesa los datos que vienen del formulario usuarios
# Acepta el método post para recepción de datos
@app.route("/usuarios/procesar", methods=["post"])
def procesar():
    if 'btnGuardar' in request.form:
        # Captura los datos del estudiante desde el formulario enviado por la vista
        
        cuenta = request.form["nombre_cuenta"]
        usuario = request.form["nombre_usuario"]
        apellido = request.form["apellido_usuario"]

        # Se obtiene la imagen
        foto = request.files["foto_usuario"]
        #Obtiene el nombre del archivo
        nom_archivo = foto.filename
        # Crea la ruta
        ruta = FOLDER_IMAGES + secure_filename(nom_archivo)
        #Guarda el archivo en disco duro
        foto.save(ruta)

        # Se conecta a la BD
        with sqlite3.connect("pogona.db") as con:
            # Crea un apuntador para manipular la BD
            cur = con.cursor()
            # Ejecuta la sentencia SQL para guardar los datos
            cur.execute("INSERT INTO pogona (nombre_cuenta,perfil_cuenta,nombre_usuario,foto_usuario) VALUES (?,?,?,?)",[nombre,direccion, telefono,nom_archivo])
            # Guardar en BD
            con.commit()
        return "Guardado!! <a href='/usuarios'>Ir atrás </a>"
    elif 'btnConsultar' in request.form:
        id = request.form["txtId"]
        with sqlite3.connect("pogona.db") as con:
            # Crea un apuntador para manipular la BD
            cur = con.cursor()
            cur.execute("SELECT * FROM usuarios WHERE id = ?",[id])
            row = cur.fetchone()
            if row:
                return jsonify(row[1])
            else:
                return "Usuario no existe"
    elif 'btnListar' in request.form:
        with sqlite3.connect("pogona.db") as con:
            # Convierte el registro en un diccionario
            con.row_factory = sqlite3.Row
            # Crea un apuntador para manipular la BD
            cur = con.cursor()
            cur.execute("SELECT * FROM usuarios")
            row = cur.fetchall()
            return render_template("lista-usuarios.html", alumnos=row)

# API para loguear
@app.route("/login", methods=["post"])
def login():
    error = []
    # Captura los datos enviados
    username = request.form["nombre_cuenta"]
    password = request.form["clave_cuenta"]

    # Validaciones
    if not username or not password:
        error.append("Username/Password son requeridos")
    
    if len(username) > 50:
        error.append("Username excede longitud máxima")
    
    clave = hashlib.sha256(password.encode())
    pwd = clave.hexdigest()

    #Conexión a BD
    with sqlite3.connect("pogona.db") as con:
        # Convierte el registro en un diccionario
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # FORMA INCORRECTA DE REALIZAR UNA CONSULTA SQL (NO CONCATENAR)
        #cur.execute("SELECT 1 FROM usuario5784 WHERE username ='" + username + "' AND password ='" + password +"'")

        # Sentencias preparadas
        cur.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?",[username, pwd])
        row =cur.fetchone()
        if row:
            # session["usuario"] = row["username"]
            #session["perfil"] = row["username"]
            return redirect("usuarios")
        else:
            error = "Usuario o password no existe"

    
    return render_template("login.html", error = error)


@app.route("/usuarios")
def usuario():
    # if session["perfil"] == "admin" or session["perfil"] == "super-admin":
    # if "usuario" in session:
    return render_template("usuarios.html")

    # return render_template("login.html",error= ["Usuario inválido!"])
"""
Endpoint para registra un usuario en la BD
Metodo : post
return : string
"""
@app.route("/usuario/crear",methods=["post"])
def usuario_crear():
    # Captura los datos del usuario
    user = request.form["nombre_cuenta"]
    password = request.form["clave_cuenta"]
    confirm = request.form["txtConfirmar"]
    #Validaciones
    if (password != confirm):
        return "Password no coincide"
    
    if not user:
        return "Debe digitar un username"

    if not password:
        return "Debe digitar un password"
    # Aplica la función hash (haslib) al password
    clave = hashlib.sha256(password.encode())
    # Convierte el password a hexadecimal tipo string
    pwd = clave.hexdigest()
    # Se conecta a la BD
    with sqlite3.connect("pogona.db") as con:
        cur = con.cursor()
        # Consultar si ya existe Usuario
        if siExiste(user):
            return "YA existe el Usuario!"
        #Crea el nuevo Usuario
        cur.execute("INSERT INTO usuarios (nombre_cuenta, clave_cuenta) VALUES (?,?);",[user, pwd])
        con.commit()
        return "Usuario Creado"    

@app.route("/registrar")
def registrar_usuario():
    return render_template("registrar.html")


def siExiste(user):
     # Se conecta a la BD
    with sqlite3.connect("pogona.db") as con:
        cur = con.cursor()
        # Consultar si ya existe Usuario
        cur.execute("SELECT username FROM usuarios WHERE username=?",[user])
        if cur.fetchone():
            return True
    
    return False

@app.route("/logout")
def logout():
    return redirect("/")



#end point de jhony

# Endpoint para cargar formulario Estudiantes
@app.route("/cuentaUsuario",methods=["get"])
def cuentaUsuario():
    nombreUsuario = "Johny"
    id_cuenta = "1"
    with sqlite3.connect("pogona.db") as con:
        # Convierte el registro en un diccionario
        con.row_factory = sqlite3.Row
        # Crea un apuntador para manipular la BD
        cur = con.cursor()
        cur.execute("SELECT * FROM imagenes")
        row = cur.fetchall()
        alu=row
        cur.execute("SELECT * FROM usuarios WHERE nombre_cuenta=?",[nombreUsuario])
        row = cur.fetchall()
        usu=row
    return render_template("cuentaUsuario.html", alumnos=alu, usuario=usu)

@app.route("/imagenes",methods=["get"])
def imagenes():
    nombreUsuario = "Johny"
    id_cuenta = 1
    with sqlite3.connect("pogona.db") as con:
        # Convierte el registro en un diccionario
        con.row_factory = sqlite3.Row
        # Crea un apuntador para manipular la BD
        cur = con.cursor()
        cur.execute("SELECT * FROM imagenes")
        row = cur.fetchall()
        alu=row
        cur.execute("SELECT * FROM usuarios WHERE nombre_cuenta=?",[nombreUsuario])
        row = cur.fetchall()
        usu=row
    return render_template("imagenes.html", alumnos=alu, usuario=usu)

@app.route("/cargarimagenes",methods=["get"])
def cargarimagenes():
    return render_template("CargarImagen.html")

@app.route("/cargarimagenes2",methods=["post"])
def cargarimagenes2():
    if 'btnGuardar' in request.form:
        nombreUsuario = "Johny"
        id_cuenta = 1
        # Captura los datos del estudiante desde el formulario enviado por la vista
        #nombre = request.form["txtNombre"]
        #direccion = request.form["txtDireccion"]
        #telefono = request.form["txtTelefono"]

        # Se obtiene la imagen
        foto = request.files["txtImagen"]
        #Obtiene el nombre del archivo
        nom_archivo = foto.filename
        # Crea la ruta
        ruta = FOLDER_IMAGES + secure_filename(nom_archivo)
        #Guarda el archivo en disco duro
        foto.save(ruta)
        ruta = "../" + FOLDER_IMAGES + secure_filename(nom_archivo)

        # Se conecta a la BD
        with sqlite3.connect("pogona.db") as con:
            # Crea un apuntador para manipular la BD
            cur = con.cursor()
            # Ejecuta la sentencia SQL para guardar los datos
            cur.execute("INSERT INTO imagenes (nombre_imagen, url_imagen, id_cuenta) VALUES (?,?,?)",[nom_archivo, ruta, id_cuenta])
            # Guardar en BD
            con.commit()
        return "Guardado!! <a href='/cargarimagenes'>Ir atrás </a>"
    return render_template("CargarImagen2.html")

@app.route("/eliminarimagenes",methods=["get"])
def eliminarimagenes():
    #return render_template("EliminarImagen.html")
    nombreUsuario = "Johny"
    id_cuenta = 1
    with sqlite3.connect("pogona.db") as con:
        # Convierte el registro en un diccionario
        con.row_factory = sqlite3.Row
        # Crea un apuntador para manipular la BD
        cur = con.cursor()
        cur.execute("SELECT * FROM imagenes")
        row = cur.fetchall()
        alu=row
        cur.execute("SELECT * FROM usuarios WHERE nombre_cuenta=?",[nombreUsuario])
        row = cur.fetchall()
        usu=row
    return render_template("EliminarImagen.html", alumnos=alu, usuario=usu)


# Fin end point jhony
app.run(debug=True)
