from flask import *
import AsymmetricEncryption as main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Button = request.form['Button']
        if Button == 'Generate':
            return redirect(url_for('generate'))
        if Button == 'Encrypt&Decrypt':
            return redirect(url_for('EncryptANDDecrypto'))
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        Button = request.form['Button']
        if Button == 'Gen':
            Keys = main.Main.Generate_Private_Key()
            PublicKey = main.Main.Generate_Public_Pem(Keys['Public Key'])['Public Pem']
            PrivateKey = main.Main.Generate_Private_Pem(Keys['Private Key'])['Private Pem']
            return render_template('generate.html', Status=True, PublicKey=PublicKey, PrivateKey=PrivateKey)
        if Button == 'goBack':
            return redirect(url_for('index'))
    return render_template('generate.html', Status=True)

@app.route('/encrypt/and/decrypt', methods=['GET', 'POST'])
def EncryptANDDecrypto():
    if request.method == 'POST':
        Button = request.form['Button']
        if Button == 'GoBack':
            return redirect(url_for('index'))
        if Button == 'Encrypt':
            PublicKey1 = request.form['PublicKey']
            RawText = request.form['RawText']
            if 'PUBLIC' in PublicKey1:
                PublicKey = main.Main.Public_Pem(PublicKey1)['Public Key']
                EncryptedText = main.Encrypt.Encrypt_With_Public_Key(PublicKey, RawText)
            if 'PRIVATE' in PublicKey1:
                PrivateKey = main.Main.Private_Pem(PublicKey1)['Private Key']
                EncryptedText = main.Encrypt.Encrypt_With_Private_Key(PrivateKey, RawText)
            return render_template('encrypt&decrypt.html', PublicKey=PublicKey1, RawText=RawText, OUTEncryptedText=EncryptedText['Encrypted Message'], PrivateKey=request.form['PrivateKey'], EncryptedText=request.form['EncryptedText'], OUTDecryptedText=request.form['OUTDecryptedText'])
        if Button == 'Decrypt':
            PrivateKey1 = request.form['PrivateKey']
            EncryptedText = request.form['EncryptedText']
            PrivateKey = main.Main.Private_Pem(PrivateKey1)['Private Key']
            DecryptedText = main.Decrypt.Decrypt_With_Private_Key(PrivateKey, EncryptedText)
            return render_template('encrypt&decrypt.html', PrivateKey=PrivateKey1, EncryptedText=EncryptedText, OUTDecryptedText=DecryptedText['Original Message'], PublicKey=request.form['PublicKey'], RawText=request.form['RawText'], OUTEncryptedText=request.form['OUTEncryptedText'])
        
    return render_template('encrypt&decrypt.html')
