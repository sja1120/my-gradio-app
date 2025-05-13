import tkinter as tk
from tkinter import messagebox
import random

# words.txt 파일에서 단어 불러오기
words = {}
with open("words.txt", "r", encoding="utf-8") as f:
    for line in f:
        if ":" in line:
            eng, kor = line.strip().split(":", 1)
            words[eng.strip()] = kor.strip()

# 초기 변수 설정
score = 0
total = 0
wrong_answers = []
current_word = ""

def new_quiz():
    global current_word
    current_word = random.choice(list(words.keys()))
    question_label.config(text=f"{current_word}의 뜻은?")

def check_answer():
    global score, total
    user_input = answer_entry.get().strip()
    total += 1
    if user_input == words[current_word]:
        score += 1
        result_label.config(text="정답!", fg="green")
    else:
        result_label.config(text=f"틀렸어. 정답: {words[current_word]}", fg="red")
        wrong_answers.append(f"{current_word} → {words[current_word]} (입력: {user_input})")
    update_score()
    answer_entry.delete(0, tk.END)
    new_quiz()

def update_score():
    score_label.config(text=f"점수: {score} / {total}")

def show_wrong_answers():
    if not wrong_answers:
        messagebox.showinfo("틀린 문제 복습", "틀린 문제가 없어요!")
    else:
        messagebox.showinfo("틀린 문제 복습", "\n".join(wrong_answers))

# Tkinter 윈도우 만들기
root = tk.Tk()
root.title("단어 퀴즈")
root.geometry("400x300")

question_label = tk.Label(root, text="", font=("Arial", 16))
question_label.pack(pady=10)

answer_entry = tk.Entry(root, font=("Arial", 14))
answer_entry.pack()
answer_entry.focus()

submit_button = tk.Button(root, text="제출", command=check_answer)
submit_button.pack(pady=5)

# 스페이스바와 엔터로도 제출되게 설정
root.bind("<Return>", lambda event: check_answer())
root.bind("<space>", lambda event: check_answer())

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=5)

score_label = tk.Label(root, text="점수: 0 / 0", font=("Arial", 12))
score_label.pack(pady=5)

wrong_button = tk.Button(root, text="틀린 문제 보기", command=show_wrong_answers)
wrong_button.pack(pady=5)

new_quiz()
root.mainloop()