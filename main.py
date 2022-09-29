from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from flask_alembic import Alembic





app = Flask(__name__)
app.debug = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
base = app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
alembic = Alembic()
alembic.init_app(app)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text)
    author = db.Column(db.String(50))
    description = db.Column(db.String(250))
    pos_book = db.relationship('Pos_book', backref='book')

    def __init__(self, title, author, description):
        self.title = title
        self.description = description
        self.author = author
        

class Pos_book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    def __init__(self, category):
        self.category = category    
        

class Post_book(ma.Schema):
    class Meta:
        fields = ('category')




class PostSchema(ma.Schema):
    class Meta:
        fields = ('title', 'author', 'description')




post_schema = PostSchema()
posts_schema = PostSchema(many=True)

post_book = Post_book()
posts_book = Post_book(many=True)


app.config['SQLALCHEMY_ECHO'] = True

# посмотреть все записи

@app.route('/get', methods = ['GET'])
def get_post():
    all_posts = Book.query.all()
    result = posts_schema.dump(all_posts)

    return jsonify(result)

# посмотреть одну запись

@app.route('/post_details/<id>/', methods = ['GET'])
def post_details(id):
    # добавил post_book не знаю будет ли работать
    post = Book.query.get(id)
    posti = Pos_book.query.get(id)
    return post_schema.jsonify(post), post_book.jsonify(posti)

# обновить запись

@app.route('/post_update/<id>', methods = ['PUT'])
def post_update(id):
    post = Book.query.get(id)

    title = request.json['title']
    author = request.json['author']
    description = request.json['description']
    

    post.title = title
    post.author = author
    post.description = description

    db.session.commit()
    return post_schema.jsonify(post)
# Удалить запись

@app.route('/post_delete/<id>', methods = ['DELETE'])
def post_delete(id):
    post = Book.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return post_schema.jsonify(post)

# поиск по определенному значению



# поиск по автору?
@app.route('/user/<author>')
def show_user(author):

    user = Book.query.filter_by(author=author)
    print(user)
    if user != None:
         return posts_schema.jsonify(user)


   

# Добавить запись

@app.route('/post', methods = ['POST'])
def add_post():
    title = request.json['title']
    author = request.json['author']
    description = request.json['description']
    

    my_posts = Book(title, author, description)
    db.session.add(my_posts)
    db.session.commit()

    return post_schema.jsonify(my_posts)

if __name__ == '__main__':
    app.run(debug=True)