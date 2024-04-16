from flask import Flask, request, jsonify

app = Flask(__name__)

books_list = [
  {
    "id": 1,
    "author": "Chinua Achebe",
    "country": "Nigeria",
    "imageLink": "images/things-fall-apart.jpg",
    "language": "English",
    "link": "https://en.wikipedia.org/wiki/Things_Fall_Apart\n",
    "pages": 209,
    "title": "Things Fall Apart",
    "year": 1958
  },
  {
    "id": 2,
    "author": "Hans Christian Andersen",
    "country": "Denmark",
    "imageLink": "images/fairy-tales.jpg",
    "language": "Danish",
    "link": "https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.\n",
    "pages": 784,
    "title": "Fairy tales",
    "year": 1836
  },
  {
    "id": 3,
    "author": "Dante Alighieri",
    "country": "Italy",
    "imageLink": "images/the-divine-comedy.jpg",
    "language": "Italian",
    "link": "https://en.wikipedia.org/wiki/Divine_Comedy\n",
    "pages": 928,
    "title": "The Divine Comedy",
    "year": 1315
  },
  {
    "id": 4,
    "author": "Unknown",
    "country": "Sumer and Akkadian Empire",
    "imageLink": "images/the-epic-of-gilgamesh.jpg",
    "language": "Akkadian",
    "link": "https://en.wikipedia.org/wiki/Epic_of_Gilgamesh\n",
    "pages": 160,
    "title": "The Epic Of Gilgamesh",
    "year": -1700
  }
]

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/books', methods=['GET', 'POST'])
def books():
  if request.method == 'GET':
    if len(books_list) > 0:
      return jsonify(books_list)
    else:
      'Nothing found', 404

  if request.method == 'POST':
    new_title = request.json['title']
    new_author = request.json['author']
    new_country = request.json['country']
    new_imageLink = request.json['imageLink']
    new_language = request.json['language']
    new_link = request.json['link']
    new_pages = request.json['pages']
    new_year = request.json['year']
    new_id = books_list[-1]['id'] + 1
    
    # new_title = request.form['title']
    # new_author = request.form['author']
    # new_country = request.form['country']
    # new_imageLink = request.form['imageLink']
    # new_language = request.form['language']
    # new_link = request.form['link']
    # new_pages = request.form['pages']
    # new_year = request.form['year']


    new_obj = {
      'id': new_id,
      'title': new_title,
      'author': new_author,
      'country': new_country,
      'imageLink': new_imageLink,
      'language': new_language,
      'link': new_link,
      'pages': new_pages,
      'year': new_year
    }
    
    print(new_obj)

    books_list.append(new_obj)
    return jsonify(books_list), 201
  
@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
  if request.method == 'GET':
    for book in books_list:
      if book['id'] == id:
        return jsonify(book)
    else:
      return 'Not found', 404
    
  if request.method == 'PUT':
    for book in books_list:
      if book['id'] == id:
        book['author'] = request.json['author']
        book['country'] = request.json['country']
        book['imageLink'] = request.json['imageLink']
        book['language'] = request.json['language']
        book['link'] = request.json['link']
        book['pages'] = request.json['pages']
        book['title'] = request.json['title']
        book['year'] = request.json['year']
        return jsonify(book)
    else: 
      return 'Not found', 404
    
  if request.method == 'DELETE':
    for book in books_list:
      if book['id'] == id:
        books_list.remove(book)
        return jsonify(books_list)
    else:
      return 'Not found', 404

@app.route('/<name>')
def hello_name(name):
  return f'Hello, {name}!'

if __name__ == '__main__':
  app.run(debug=True)