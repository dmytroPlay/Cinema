from flask import Flask, render_template, request, redirect, url_for
import sqlite3  

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('films.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT,
            duration INTEGER,
            description TEXT,
            price INTEGER NOT NULL,
            image TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()



@app.route('/')
def main():
    return render_template('main.html')



@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/movies', methods=['GET'])
def movies():
    conn = get_db_connection()
    films = conn.execute(
        "SELECT * FROM films"
    ).fetchall()

    conn.close()
    
    return render_template('movies.html', movies=films)




@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == "POST":
        title = request.form.get('title', '').strip()
        genre = request.form.get('genre', '').strip()
        duration = request.form.get('duration', '').strip()
        description = request.form.get('description', '').strip()
        price =  request.form.get('price', '').strip()
        image = request.form.get('image', '').strip()


        conn = get_db_connection()
        conn.execute(
            '''INSERT INTO films (title, genre, duration, description, price, image)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (title, genre, duration, description,price, image)
        )
        conn.commit()
        conn.close()

    return render_template('add_movie.html', form={})




@app.route('/gallery')
def gallery():
    return render_template('gallery.html')




@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/delete/<int:id>', methods=['POST'])
def delete_film(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM films WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/movies')

if __name__ == '__main__':
    app.run(debug=True)