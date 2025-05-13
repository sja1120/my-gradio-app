from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 단어 목록 (영단어 퀴즈용)
words = [
    ("apple", "사과"),
    ("banana", "바나나"),
    ("cat", "고양이"),
    # 추가적으로 단어를 넣을 수 있어
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['GET'])
def quiz():
    word, meaning = random.choice(words)
    return jsonify({'word': word, 'meaning': meaning})

if __name__ == '__main__':
    app.run(debug=True)