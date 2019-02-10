import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, Response

# Imports the Google Cloud client library
from werkzeug.utils import secure_filename
from google.cloud.language import types
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/shanjiang/Documents/Coding/gcloud/beginning-93f35f2187ba.json"
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

UPLOAD_FOLDER = '/Users/shanjiang/Documents/Calvin/v2/uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__, template_folder='template') #important
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):#file success upload
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            

            return redirect(url_for('proccess_texts', filename=filename))
            #return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return render_template("upload_button.html")

@app.route('/proccess_texts/<filename>')
def proccess_texts(filename):
    file_location = '/Users/shanjiang/Documents/Calvin/v2/uploads/'+filename
    fin = open(file_location, 'r')
    text = fin.read()
    text = text.decode('utf-8')

    # Instantiates a client
    client = language.LanguageServiceClient()

    document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    response = client.analyze_syntax(document=document)

    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
                'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    word_ls = []
    pos_ls = []
    for token in response.tokens:
        word_ls.append(token.text.content) 
        pos_ind = token.part_of_speech.tag
        pos_ls.append(pos_tag[pos_ind])

    length = []
    #result = dict(zip(word_ls, pos_ls))
    for x in xrange(len(word_ls)):
        length.append(x)

    #print "word:",word
    #print "syntax:",pos_tag[result]
    return render_template('proccessed_texts.html', word_ls=word_ls, pos_ls=pos_ls, length=length)
    #return Response(text, mimetype='text/plain')


if __name__ == '__main__':
   app.run(debug = True)



# display file
#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'],
#                               filename)