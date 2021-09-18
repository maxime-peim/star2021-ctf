import tarfile
from flask import Flask, flash, request, redirect, url_for, abort, send_file, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/tmp"
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(file):
    if '.' in file.filename and file.filename.rsplit('.')[1].lower() == "tar":
        return file.content_type == "application/x-tar"
    return False

@app.route("/")
def front_page():
    return '''
    <!doctype html>
    <title>Welcome</title>
    <html>
        <h1>Welcome !</h1>
        <p> I've created this little web app to backup some of your data, forever ! (Note that I will extract your data to stay organized)</p>
        <p> To do so, head over to <a href="/upload">this page</a> (tar only !)</p>
        <p> Otherwise, you might want to checkout some of the things I post, it's <a href="/files/index.html">here<a/></p>
        <br/>
        <p>Oh, and by the way, there's a flag in /etc/flag, but it's only for me</p>
    </html>
    '''


@app.route("/upload", methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            session['status'] ='No file part'
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            session['status'] = 'No selected file'
            return redirect(request.url)
        if file and allowed_file(file):
            filename = secure_filename(file.filename)
            if(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                tf = tarfile.TarFile(os.path.join(app.config['UPLOAD_FOLDER'],filename),'r')
                tf.extractall()
            except Exception as e:
                session['status'] = str(e)
                return redirect(request.url)

            session['status'] = "Success !"
            return redirect(request.url) 
        else:
            session['status'] = "Fail !"
            return redirect(request.url)
    else:
        if not session.get('status'):
            session['status']=''
        out = '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method=post enctype=multipart/form-data>
<input type=file name=file>
<input type=submit value=Upload>
</form>
''' + session.get('status')
        session['status']=''
        print(session.get('status'))
        return out

@app.route('/files/<path:filename>')
def show_file(filename):
    
    file_path = os.path.join('/var/www/html/files/', secure_filename(filename))

    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=40001)
