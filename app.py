from flask import Flask, render_template, url_for, flash, redirect, request, get_flashed_messages, jsonify
import sqlite3
from werkzeug.exceptions import abort
import requests

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


OOBABOOGA_API_URL = "http://127.0.0.1:5000/v1/completions" 

HEADERS = {"Content-Type": "application/json"}

# api stuff
# @app.route('/api')
# def api():
#     return "Welcome to the Oobabooga Flask API!"

# @app.route('/api/generate', methods=['POST',])
# def generate_text():
#     try:
#         data = request.get_json()

#         prompt = data.get('prompt', '')

#         if not prompt:
#             return jsonify({'error': 'Prompt is required!'}), 400
        
#         oobabooga_response = requests.post(OOBABOOGA_API_URL, json={
#             "prompt": prompt,
#             "max_new_tokens": 100
#         })

#         if oobabooga_response.status_code != 200:
#             return jsonify({'error': 'Failed to get a response from Oobabooga API'}), 500
        
#         generated_text = oobabooga_response.json().get('results', [{}])[0].get('text', '').strip()

#         return jsonify({
#             'prompt': prompt,
#             'generated_text': generated_text
#         })
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
# if __name__ == '__main__':
#     app.run(debug=True)

@app.route('/chat', methods=['POST'])
def api():
    try:
        data = request.get_json()
        history = data.get('history', [])
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'User message is required'}), 400
        
        history.append({"role": "user", "content": user_message})

        external_data = {
            "model": "lmsys_vicuna-7b-v1.5",
            "prompt": "testmessage say hi"
            #"messages": history
        }

        response = request.post(OOBABOOGA_API_URL, headers=HEADERS, json=external_data, verify=False)

        if response.status_code !=200:
            return jsonify({'error': 'Failed to get a response from the external API'}), 500
        
        assistant_message = response.json()['choices'][0]['message']['content']

        history.append({"role": "assistant", "content": assistant_message})

        return jsonify({
            'history': history,
            'assistant_message': assistant_message
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)