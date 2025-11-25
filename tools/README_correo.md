# Correo Tools (Documentación)

## Descripción General
Se describe la documentación para poder hacer uso del script `correo_tools.py`, el cual hace uso del script `auth.py`.
Este script facilita al asistente inteligente el envío de correos electrónicos via Gmail a cualquier destinatario.

## 1. Instalación de programas necesarios
### 1.1. Descargar e instalar python del sitio oficial
    https://www.python.org/
Verificamos que python esté instalado usando el siguiente comando en la consola de línea de comandos:

    python --version
    
Si nos sale la versión significa que está instalado correctamente.

### 1.2. Descargar e instalar Visual Studio Code del sitio oficial
    https://code.visualstudio.com/


## 2. Preparación del entorno
### 2.1. Clonar el respositorio del backend usando GIT o descargándolo como .zip desde
    https://github.com/adminLTR/Proyecto-automatizacion

### 2.2. Configuración de Google Cloud (Proyecto Existente)
Para que el script funcione en tu máquina local, necesitas descargar el archivo de credenciales del proyecto compartido:

2.2.1. Ve a la sección de **Credenciales** en la consola de Google Cloud del proyecto.
2.2.2. Busca el **ID de cliente de OAuth 2.0** (Tipo: Aplicación de escritorio) que ya fue creado.
2.2.3. Haz clic en el icono de descarga (⬇️) para bajar el archivo JSON.
2.2.4. **Renombra** el archivo descargado a `credentials.json`.
2.2.5. **Mueve** el archivo `credentials.json` dentro de esta carpeta `Proyecto-automatizacion\tools\`.

> **Nota:** Sin este archivo, el script fallará inmediatamente.

### 2.3. Crear un entorno virtual
2.3.1. Abrir una consola de linea de comandos (CMD en Windows) en la ruta del repositorio clonado en el dispositivo.
2.3.2. Creamos un entorno virtual en la raíz del proyecto usando el siguiente comando:

    python -m virtualenv venv

2.3.3. activamos el entorno virtual usando el siguiente comando:

    .\venv\Scripts\activate

Notaremos que entramos al entorno virtual, la consola debería verse algo así:

    (venv) ruta\a\Proyecto-automatizacion>

## 2.4. Instalar dependencias
Para instalar todas las librerías y dependencias necesarias, nos ubicamos dentro de la carpeta `Proyecto-automatizacion\tools\` y empleamos el siguiente comando asegurándonos de estar dentro del entorno virtual:

    pip install -r requirements.txt

De este modo, el script estará listo para ser usado.


# 3. Probar el script
## 3.1. Cambiar correo de destino
Para probar el envío de correos a nombre del usuario autenticado primero deberemos ir al archivo `app.py` que funciona como archivo de prueba:
    
    Proyecto-automatizacion\tools\app.py

Una vez ahí, nos dirigimos a la sección:

    @app.route('/test-email')
    def test_email():    
        resultado = tool_enviar_correo(
            service_gmail, 
            # Correo de prueba (CAMBIAR POR EL DESTINO, SOLO PARA PRUEBAS)
            destinatario="email@example.com", 
            asunto="Prueba desde el Bot de Telegram",
            cuerpo="Hola, este es un mensaje enviado automáticamente por el asistente virtual."
        )
        return jsonify({"resultado": resultado})

Y cambiamos el correo `email@example.com` por el que deseamos que sea el destinatario para después guardar los cambios de manera local.

## 3.2. Realizar prueba
3.2.1. Abrimos el una terminal, de preferencia cmd si se está en Windows, y nos dirigimos a la ruta de la carperta `Proyecto-automatizacion\tools\`, una vez ahí escribimos el siguiente comando:

    python app.py

Nos debe salir algo como:

    Autenticando servicios de Google...
    * Serving Flask app 'app'
    * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on http://127.0.0.1:5000
    Press CTRL+C to quit

> **Nota:** Si es la primera vez que hacemos esto, se nos abrirá el navegador en la pestaña de autenticación de Google pidiendo acceso y autorización de nuestra app (Bot) para acceder a su correo y calendario. Ingresamos con el correo autenticado y aceptamos todo. En caso no se abra el navegador de manera automática, la consola mostrará el enlace al que deberá acceder para realizar la autenticación.

3.2.2. Accedemos a la dirección 
    
    http://127.0.0.1:5000

Y nos debería salir una página en blanco con un texto que diga "Bot de Telegram activo". Si es asi, significa que todo marcha bien.

3.2.3. Ahora probamos el envío de correo accediendo al siguiente enlace:
    
    http://127.0.0.1:5000/test-email

La página mostrará un mensaje anunciando el envío exitoso del correo al destinatario elegido. El destinatario solo deberá revisar su bandeja de entrada y, si todo salió bien, debería ver el mensaje.

