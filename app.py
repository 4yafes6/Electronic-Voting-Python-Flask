# bazı kütüphane, modül ve diğer uyugulamalar projeye dahil edildi
from flask import Flask, render_template , request , Response
import Mail2
from flask_mysqldb import MySQL
import mysql.connector
import cv2
from deepface import DeepFace

app=Flask(__name__)

# veritabanına bağlanıldı
db = mysql.connector.connect(
   host="localhost",
   user="root",
   passwd="0218",
   database='flask_db'
)
mysql = MySQL(app)

# ------------- kayıt olma başlangıç ------------- 

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route("/mailver", methods = ["GET" , "POST"])
def mail():
    #return render_template("mail.html")
    if request.method == "POST":
        TcNo = request.form.get("TcNo")
        isim = request.form.get("isim")
        soyisim = request.form.get("soyisim")
        SeriNo = request.form.get("SeriNo")
        DogumTarihi = request.form.get("DogumTarihi")
        email = request.form.get("email")
        adres = request.form.get("adres")
        sehir = request.form.get("sehir")
        ilce = request.form.get("ilce")
        sifre = request.form.get("sifre")
        sifre_tekrar = request.form.get("sifre_tekrar")
        global _TcNo
        _TcNo = TcNo
        _isim = isim
        _soyisim = soyisim
        _SeriNo = SeriNo
        _DogumTarihi = DogumTarihi
        _email = email
        _adres = adres
        _sehir = sehir
        _ilce = ilce
        _sifre = sifre
        _sifre_tekrar = sifre_tekrar
        
        #mail gönder
        kod = Mail2.Mail.gönder(_email)
        #veritabanı ekleme
        cur = db.cursor()
        cur2 = db.cursor()
        cur.execute(f"UPDATE `flask_db`.`kod1` SET `kod` = '{kod}' WHERE (`id` = '1');")
        cur2.execute(f"INSERT INTO `flask_db`.`kullanicilar` (`TcNo`, `isim`, `soyisim`, `SeriNo`, `DogumTarihi`, `email`, `adres`, `sehir`, `ilce`, `sifre`) VALUES ('{_TcNo}', '{_isim}', '{_soyisim}', '{_SeriNo}', '{_DogumTarihi}', '{_email}', '{_adres}', '{_sehir}', '{_ilce}', '{_sifre}');")
        db.commit()
        # db.close()

        return render_template('mail.html')
    else:
        return "Bir hata meydana geldi kayıt başarısız"
    
@app.route("/kod", methods = ["GET" , "POST"])
def kod():
    
    if request.method == "POST":
        kod = request.form.get("kod")
        txt_kod = kod
        
        cur = db.cursor()
        cur.execute("SELECT * FROM flask_db.kod1;") 
        
        for (id,vt_kod) in cur:
            print(id,vt_kod)
            
        vt_kod = int(vt_kod)
        txt_kod = int(txt_kod)
        
        print(vt_kod)
        print(txt_kod)
        if(txt_kod == vt_kod):
            return render_template('face.html')
        else:
            return "Kodlar aynı değil! Lütfen tekrar deneyiniz"
        
@app.route('/KayitKameraAç')
def KayitKameraAç():
    return render_template("registerface.html") # kamera aç

@app.route('/KayitKaydedildi')
def KayitKaydedildi():
    return render_template("KayitKaydedildi.html") # foto kaydet

def KayitFoto():
    camera=cv2.VideoCapture(0)
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            global kayit_filename
            kayit_filename=f'D:\\Python\\proje\\kayit\\kayit_{_TcNo}.jpg'
            cv2.imwrite(kayit_filename, img=frame)
            camera.release()
            cv2.destroyAllWindows()
            
            #veritabanı
            cur = db.cursor()
            cur.execute("SET SQL_SAFE_UPDATES = 0;")
            cur2 = db.cursor()
            cur2.execute(f"UPDATE `flask_db`.`kullanicilar` SET `KayitFoto` = '{kayit_filename}' WHERE (`TcNo` = '{_TcNo}');")
            db.commit()
            #veritabanı
            
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/KayitFotoKaydet')
def KayitFotoKaydet():
    return Response(KayitFoto(),mimetype='multipart/x-mixed-replace; boundary=frame')
        
# ------------- kayıt olma bitiş ------------- 


def generate_frames():
    camera=cv2.VideoCapture(0)
    while True:

        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
    camera.release()
    cv2.destroyAllWindows()

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


# ------------- giriş yapma başlangıç ----------

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/GirisKarsılastırma', methods = ["GET" , "POST"])
def GirisKarsılastırma():
    if request.method == "POST":
        giris_TcNo = request.form.get("giris_TcNo")
        giris_sifre = request.form.get("giris_sifre")
        global _giris_TcNo
        global _giris_sifre
        _giris_TcNo = giris_TcNo
        _giris_sifre = giris_sifre
        cur = db.cursor()
        cur.execute(f"select TcNo, sifre from flask_db.kullanicilar where TcNo = {_giris_TcNo} ;") 
        global g_TcNo
        global g_sifre
        for (g_TcNo,g_sifre) in cur:
            print(g_TcNo,g_sifre)
        
        g_TcNo = int(g_TcNo)
        g_sifre = str(g_sifre)

@app.route('/GirisOnay', methods = ["GET" , "POST"])
def GirisOnay():
        try:
            GirisKarsılastırma()
            if(_giris_sifre == g_sifre):
                return render_template("login_face.html")
            else:
                return "Şifre Yanlış"
        except:
            return "Böyle bir TC yok"

@app.route('/GirisKameraAç')
def GirisKameraAç():
    return render_template("loginface.html")

@app.route('/GirisKaydedildi')
def GirisKaydedildi():
    return render_template("GirisKaydedildi.html")

@app.route('/dogrula')
def fotokarsilastir():
    module_name="Facenet"
    img_kayit_path = kayit_filename
    img_kayit_path = giris_filename
    try:
        result = DeepFace.verify(img_kayit_path, img_kayit_path,module_name)
        result = str(result)
        karsılastırma = result
        if(karsılastırma == "True"):
            return "Fotoğraflar aynı, giriş başarılı"
        else:
            return "Fotoğraflar farklı, giriş başarısız"
    except Exception as e:
        print("hata: "+ str(e))

def GirisFoto():
    camera=cv2.VideoCapture(0)
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            global giris_filename
            giris_filename=f'D:\\Python\\proje\\giris\\giris_{_giris_TcNo}.jpg'
            cv2.imwrite(giris_filename, img=frame)
            camera.release()
            cv2.destroyAllWindows()
            
            #veritabanı
            cur = db.cursor()
            cur.execute("SET SQL_SAFE_UPDATES = 0;")
            cur2 = db.cursor()
            cur2.execute(f"UPDATE `flask_db`.`kullanicilar` SET `GirisFoto` = '{giris_filename}' WHERE (`TcNo` = '{_giris_TcNo}');")
            db.commit()
            #veritabanı
            
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/GirisFotoKaydet')
def GirisFotoKaydet():
    return Response(GirisFoto(),mimetype='multipart/x-mixed-replace; boundary=frame')

# ------------- giriş yapma bitiş ----------



# ------------- oy verme başlangıç ----------

@app.route('/voting')
def voting():
    return render_template('voting.html')

@app.route('/putin', methods=['GET', 'POST'])
def putin():
    if request.method == "POST":
        cur = db.cursor()
        cur.execute(f"SELECT id, Vlademir_Putin FROM flask_db.table_oy WHERE (`id` = '1');")
        
        for (id,putin_oy) in cur:
            print(id, putin_oy)
        
        putin_oy += 1
        cur2 = db.cursor()
        cur2.execute(f"UPDATE `flask_db`.`table_oy` SET `Vlademir_Putin` = '{putin_oy}' WHERE (`id` = '1');")
        db.commit()
        return render_template("successful.html")
    
@app.route('/merkel', methods=['GET', 'POST'])
def merkel():
    return render_template("successful.html")

@app.route('/macron', methods=['GET', 'POST'])
def macron():
    return render_template("successful.html")

@app.route('/results')
def results():
    return render_template('results.html')

# ------------- oy verme bitiş ----------


# ------------- ara sayfalar başlangıç ----------

# @app.route('/login_face')
# def login_face():
#     return render_template('login_face.html')

# @app.route('/success')
# def success():
#     return render_template('successful.html')

# @app.route('/facerec', methods = ["GET" , "POST"])
# def facerec():
#         return render_template('face.html')
            
# @app.route('/mail')
# def mail2():
#     return render_template('mail.html')
 
# ------------- ara sayfalar bitiş ----------

if __name__=="__main__":
    app.run(debug=True)

