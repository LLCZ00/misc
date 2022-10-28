from flask import Flask, render_template, request, redirect, url_for
from ppc_webinfo import info_get

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        pname = request.form['pokemon']
        if pname == '':
            return redirect(url_for('error'))
        
        return redirect(url_for('info', name=pname.lower()))
    else:
        return render_template('front_page.html')


@app.route('/info/<name>')
def info(name):
    pinfo = info_get(name)

    if type(pinfo) == list:
        return render_template('info_page.html', name=pinfo[0].capitalize(),
                               ptype=pinfo[2], strong=pinfo[1]['strong'],
                               weak=pinfo[1]['weak'], inv=pinfo[1]['invulnerable'],
                               vuln=pinfo[1]['vulnerable'])
    else:
        return redirect(url_for('error'))

@app.route('/error/')
def error():
    return render_template('error_page.html')

if __name__ == '__main__':
    app.run()
