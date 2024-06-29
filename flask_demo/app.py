from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data
books = [
    {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "isbn": "9781593276034",
        "available": True,
        "copies": 5,
        "borrowers": []
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "available": True,
        "copies": 3,
        "borrowers": []
    },
    {
        "title": "Design Patterns",
        "author": "Erich Gamma",
        "isbn": "9780201633610",
        "available": True,
        "copies": 2,
        "borrowers": []
    }
]

users = []

@app.route('/')
def index():
    return render_template('index.html', books=books, users=users)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    copies = int(request.form['copies'])
    books.append({
        "title": title,
        "author": author,
        "isbn": isbn,
        "available": copies > 0,
        "copies": copies,
        "borrowers": []
    })
    return redirect(url_for('index'))

@app.route('/update_book', methods=['POST'])
def update_book():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    for book in books:
        if book['isbn'] == isbn:
            book['title'] = title
            book['author'] = author
            break
    return redirect(url_for('index'))

@app.route('/delete_book', methods=['POST'])
def delete_book():
    isbn = request.form['isbn']
    global books
    books = [book for book in books if book['isbn'] != isbn]
    return redirect(url_for('index'))

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    users.append({"name": name})
    return redirect(url_for('index'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    name = request.form['name']
    global users
    users = [user for user in users if user['name'] != name]
    return redirect(url_for('index'))

@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    isbn = request.form['isbn']
    user_name = request.form['user_name']
    user_exists = any(user['name'] == user_name for user in users)
    if user_exists:
        for book in books:
            if book['isbn'] == isbn and book['copies'] > 0:
                book['copies'] -= 1
                book['available'] = book['copies'] > 0
                book['borrowers'].append(user_name)
                break
    else:
        return redirect(url_for('index', error="User does not exist"))
    return redirect(url_for('index'))

@app.route('/return_book', methods=['POST'])
def return_book():
    isbn = request.form['isbn']
    user_name = request.form['user_name']
    for book in books:
        if book['isbn'] == isbn and user_name in book['borrowers']:
            book['copies'] += 1
            book['available'] = True
            book['borrowers'].remove(user_name)
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
