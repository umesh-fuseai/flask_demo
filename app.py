from flask import Flask, render_template, abort, jsonify, request, redirect, url_for
from model import db, save_json

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('home.html', message="This is value passed", cards=db)


@app.route('/card/<int:index>')
def card_route(index):
    try:
        selected_card = db[index]
        return render_template('view_card.html', card=selected_card, index=index, max_index=len(db) - 1)
    except IndexError:
        abort(404)


@app.route('/card/add', methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {
            'question': request.form['question'],
            'answer': request.form['answer']
        }
        db.append(card)
        save_json()
        return redirect(url_for('card_route', index=len(db)-1))
    else:
        return render_template('add_card.html')


@app.route('/api/card/<int:index>')
def api_card_route(index):
    try:
        selected_card = db[index]
        return selected_card
    except IndexError:
        return {}


@app.route('/api/cards')
def api_all_card_route():
    return jsonify(db)
