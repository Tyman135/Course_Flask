from flask import Flask, jsonify, request
from db import db
from orm.models import Author, Quotes
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/flask_bd'
app.json.ensure_ascii = False
db.init_app(app)

# with app.app_context():
    # db.create_all()
migrate = Migrate(app, db)

@app.get("/authors")
def get_authors():
    authors = db.session.execute(db.select(Author)).scalars().all()
    return jsonify([a.to_dict() for a in authors])

@app.post("/authors")
def create_author():
    data = request.json
    author = Author(name=data["name"], surname=data.get("surname"))
    db.session.add(author)
    db.session.commit()
    return jsonify(author.to_dict()), 201

@app.delete("/authors/<int:author_id>")
def delete_author(author_id):
    author = db.session.get(Author, author_id)
    if not author: return jsonify(error="Not found"), 404
    db.session.delete(author)
    db.session.commit()
    return jsonify(message="Author and their quotes deleted"), 200

@app.get("/quotes")
def get_all_quotes():
    quotes = db.session.execute(db.select(Quotes)).scalars().all()
    return jsonify([q.to_dict() for q in quotes])

@app.get("/authors/<int:author_id>/quotes")
def get_author_quotes(author_id):
    author = db.session.get(Author, author_id)
    if not author: return jsonify(error="Author not found"), 404
    return jsonify([q.to_dict() for q in author.quotes])

@app.post("/authors/<int:author_id>/quotes")
def create_quote(author_id):
    author = db.session.get(Author, author_id)
    if not author: return jsonify(error="Author not found"), 404
    new_quote_data = request.json
    q = Quotes(author, new_quote_data["text"])
    db.session.add(q)
    db.session.commit()
    return jsonify(q.to_dict()), 201

@app.delete("/quotes/<int:quote_id>")
def delete_quote(quote_id):
    q = db.session.get(Quotes, quote_id)
    if not q: return jsonify(error="Quote not found"), 404
    db.session.delete(q)
    db.session.commit()
    return jsonify(message="Quote deleted"), 200

if __name__ == "__main__":
    app.run(debug=True)
