from flask import Flask, jsonify, request
from sqlalchemy import select
from db import db
from flask_migrate import Migrate
from orm.models import Author, Quotes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/flask_bd'
app.json.ensure_ascii = False

db.init_app(app)
migrate = Migrate(app, db)


@app.get("/authors")
def get_authors():
    """Получение списка активных авторов с сортировкой"""
    sort_param = request.args.get("sort", "name")
    stmt = select(Author).where(Author.is_deleted == False)

    if sort_param == "surname":
        stmt = stmt.order_by(Author.surname)
    else:
        stmt = stmt.order_by(Author.name)

    authors = db.session.execute(stmt).scalars().all()
    return jsonify([a.to_dict() for a in authors])


@app.post("/authors")
def create_author():
    """Создание автора"""
    data = request.json
    author = Author(name=data["name"], surname=data.get("surname"))
    db.session.add(author)
    db.session.commit()
    return jsonify(author.to_dict()), 201


@app.delete("/authors/<int:author_id>")
def delete_author(author_id):
    """удаление автора и его цитат"""
    author = db.session.get(Author, author_id)
    if not author:
        return jsonify(error="Author not found"), 404

    author.is_deleted = True
    for q in author.quotes:
        q.is_deleted = True

    db.session.commit()
    return jsonify(message=f"Author {author_id} and their quotes moved to trash"), 200


@app.get("/authors/trash")
def get_trash():
    """Список всех удаленных авторов"""
    stmt = select(Author).where(Author.is_deleted == True)
    authors = db.session.execute(stmt).scalars().all()
    return jsonify([a.to_dict() for a in authors])


@app.post("/authors/<int:author_id>/restore")
def restore_author(author_id):
    """Восстановление автора и его цитат"""
    author = db.session.get(Author, author_id)
    if not author:
        return jsonify(error="Not found"), 404

    author.is_deleted = False
    for q in author.quotes:
        q.is_deleted = False

    db.session.commit()
    return jsonify(author.to_dict()), 200


@app.put("/authors/<int:author_id>")
def edit_author(author_id):
    author = db.session.get(Author, author_id)
    if not author or author.is_deleted:
        return jsonify(error="Author not found"), 404

    data = request.json
    if "name" in data:
        author.name = data["name"]
    if "surname" in data:
        author.surname = data["surname"]

    db.session.commit()
    return jsonify(author.to_dict()), 200


@app.get("/quotes")
def get_quotes():
    """Получение всех активных цитат"""
    stmt = select(Quotes).where(Quotes.is_deleted == False)
    quotes_list = db.session.execute(stmt).scalars().all()
    return jsonify([q.to_dict() for q in quotes_list])


@app.get("/authors/<int:author_id>/quotes")
def get_author_quotes(author_id):
    author = db.session.get(Author, author_id)
    if not author or author.is_deleted:
        return jsonify(error="Author not found"), 404
    active_quotes = author.quotes.filter_by(is_deleted=False).all()
    return jsonify([q.to_dict() for q in active_quotes]), 200


@app.post("/authors/<int:author_id>/quotes")
def create_quote(author_id):
    """Создание цитаты для  автора"""
    author = db.session.get(Author, author_id)
    if not author or author.is_deleted:
        return jsonify(error="Active author not found"), 404

    data = request.json
    new_quote = Quotes(author, data["text"], rating=data.get("rating", 1))
    db.session.add(new_quote)
    db.session.commit()
    return jsonify(new_quote.to_dict()), 201


@app.patch("/quotes/<int:quote_id>/like")
def like_quote(quote_id):
    """Увеличение рейтинга цитаты (+1)"""
    quote = db.session.get(Quotes, quote_id)
    if not quote or quote.is_deleted:
        return jsonify(error="Quote not found"), 404

    if quote.rating < 5:
        quote.rating += 1
        db.session.commit()
    return jsonify(quote.to_dict()), 200


@app.patch("/quotes/<int:quote_id>/dislike")
def dislike_quote(quote_id):
    """Уменьшение рейтинга цитаты (-1)"""
    quote = db.session.get(Quotes, quote_id)
    if not quote or quote.is_deleted:
        return jsonify(error="Quote not found"), 404

    if quote.rating > 1:
        quote.rating -= 1
        db.session.commit()
    return jsonify(quote.to_dict()), 200


@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id):
    quote = db.session.get(Quotes, quote_id)
    if not quote or quote.is_deleted:
        return jsonify(error="Quote not found"), 404

    data = request.json
    if "text" in data:
        quote.text = data["text"]
    if "rating" in data:
        new_rating = data["rating"]
        quote.rating = max(1, min(5, int(new_rating)))

    db.session.commit()
    return jsonify(quote.to_dict()), 200


@app.delete("/quotes/<int:quote_id>")
def delete_single_quote(quote_id):
    """Мягкое удаление одной цитаты"""
    quote = db.session.get(Quotes, quote_id)
    if not quote:
        return jsonify(error="Quote not found"), 404
    quote.is_deleted = True
    db.session.commit()
    return jsonify(message=f"Quote {quote_id} moved to trash"), 200


if __name__ == "__main__":
    app.run(debug=True)
