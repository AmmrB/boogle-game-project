from flask import Flask, render_template, jsonify, request, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

boggle_game = Boggle()

@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board
    session['score'] = 0
    session['played'] = session.get('played', 0)
    session['highest_score'] = session.get('highest_score', 0)
    return render_template('index.html', board=board, score=session['score'], played=session['played'], highest_score=session['highest_score'])

@app.route('/check-word', methods=['POST'])
def check_word():
    word = request.json['word']
    board = session['board']
    result = boggle_game.check_valid_word(board, word)
    if result == 'ok':
        session['score'] += len(word)
        if session['score'] > session['highest_score']:
            session['highest_score'] = session['score']
    return jsonify({"result": result, "score": session['score']})

@app.route('/reset', methods=['POST'])
def reset_game():
    session['board'] = boggle_game.make_board()
    session['score'] = 0
    session['played'] += 1
    return jsonify({"board": session['board'], "score": session['score'], "played": session['played'], "highest_score": session['highest_score']})

if __name__ == '__main__':
    app.run(debug=True)
