from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests

# App config
#DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)

def unshorten_url(url):
    try:
        return requests.head(url, allow_redirects=True).url
    except:
        return url

class ReusableForm(Form):
    s_url = TextField('URL:', validators=[validators.required()])
    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf()) ])
        self.process(blankData)

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        s_url = request.form['s_url']
        print s_url

        if form.validate():
            url = unshorten_url(s_url)
            print url
            flash(url)
        else:
            flash('All the forms are required.')
    return render_template('unshorten.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
