from flask import Flask, render_template, url_for, flash, redirect, request, get_flashed_messages, jsonify
import sqlite3
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY Created DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/Review/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?,?)', 
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('review'))
    return render_template('create.html')

@app.route('/Review/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/Review/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('review'))

@app.route('/Map', methods=('GET',))
def map():
    return render_template('map.html')

@app.route('/Chat', methods=('GET',))
def chat():
    return render_template('chat.html')

@app.route('/Review', methods=('GET',))
def review():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY Created DESC').fetchall()
    conn.close()
    return render_template('review.html', posts=posts)

# api stuff
@app.route('/api')
def home():
    return "Welcome to the Flask API!"

@app.route('/api/data', methods=['GET'])
def get_data():
    data={
        'message': 'Hello from the Flask API!',
        'status' : 'success'
    }
    return jsonify(data)

@app.route('/api/post', methods=['POST'])
def post_data():
    data = request.get_json()
    response = {
        'received_data': data,
        'message':'Data received successfully!',
        'status' : 'success'
    }
    return jsonify(response)
