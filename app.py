from flask import Flask, request, render_template, redirect
import shorten as sh
import sqlite3
from urllib.parse import urlparse

app = Flask(__name__)
host = 'http://localhost:5000/'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('url')

        if urlparse(original_url).scheme == '':
            url = 'https://' + original_url
        else:
            url = original_url
        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute('INSERT INTO WEB_URL (URL) VALUES (?)',[url])
            encoded_string = sh.encode_url(res.lastrowid)
        return render_template('index.html', short_url= host+encoded_string, o_url=url)
    return render_template('index.html')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    decoded = sh.decode_url(short_url)
    url = host  # fallback if no URL is found
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        res = cursor.execute('SELECT URL FROM WEB_URL WHERE ID=?', [decoded])
        try:
            short = res.fetchone()
            if short is not None:
                url = short[0]
        except Exception as e:
            print(e)
    return redirect(url)


if __name__ == '__main__':
    app.run(debug=True)
