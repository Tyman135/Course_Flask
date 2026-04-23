from flask import Flask, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False


quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
   },
   {
       "id": 6,
       "author": "Mosher's Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так."
   },

]

about_me = {
    "name": "Иван",
    "surname": "Дудыкин",
    "email": "dudykin@list.ru"
}

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.get("/quotes")
def get_quotes():
    return jsonify(quotes)

@app.route("/about")
def about():
    return about_me

if __name__ == "__main__":
    app.run(debug=True)