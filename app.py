import pytube 
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,flash

app = Flask(__name__)

# settings
app.secret_key = 'mysecretkey'
mi_diccionario = {}

#Main window
@app.route('/')
def init():
    return render_template('getLink.html')

@app.route('/uploads/')
def download_file():
    "funcion que devuelve el archivo en formato audio al usuario"
    #Obtengo el nombre del archivo y se lo abro al usuario
    filename = request.args['filename'] 
    return send_from_directory('downloads',filename)  
    
@app.route('/get/format' , methods = ['POST'])
def get_format():
    "Funcion que obtiene los formatos de audio disponibles para que el usuario elija y descargue"
    if request.method == 'POST':
        re = request.form.to_dict()
        #Obtengo formato y url
        format = re['format']
        url = re['url']
        #Obtengo el video y obtengo solo el formato que el usuario desee
        yt = pytube.YouTube(url)   
        st=yt.streams.get_by_itag(mi_diccionario[format])
        #Como el formato viene con: Audio/formato uso split para solo obtener formatos
        formato = format.split('/')
        #Para evitar sobrecargar descargas de videos, todos los videos tendran el mismo nombre
        filename = 'convertedFromYoutube' + '.' + formato[1]
        #Descargo y guardo en downloads
        st.download('downloads/',filename=filename )
        return redirect(url_for('download_file',filename=filename))

@app.route('/get/video' , methods = ['POST'])
def get_video():
    "Funcion que obtiene el video de youtube"
    if request.method == 'POST':
        re = request.form.to_dict()
        #Obtengo la url que el usuario envie
        url = re['Adress']
        #Obtengo el video solo con formatos de audio
        try:
            yt = pytube.YouTube(url)
        except: 
            #Si en la url no hay un video de youtube, notificamos al usuario
            flash("No se encontró un video valido en la url enviada")
            return render_template('getLink.html',methods=['POST'])
        
        formatos=yt.streams.filter(only_audio=True).all()
        #Obtengo el Id y el formato del Stream y los guardo en un diccionario como clave-valor
        for st in formatos:
            clave = (str(st)).split('mime_type="')
            clave = clave[1].split('"')[0]
            valor = str(st).split('itag="')
            valor = valor[1].split('"')[0]
            mi_diccionario[clave] = valor
        title = yt.title
        return render_template('getFormat.html' , formats = mi_diccionario.keys(),title = title,url = url)
    
    
if __name__ == '__main__':
    app.run(port = 3000,debug=True)