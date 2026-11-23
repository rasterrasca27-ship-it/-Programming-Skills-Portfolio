import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Maths Quiz")
root.geometry("420x340")
root.resizable(False, False)
root.configure(bg="#e8f1f5")

# Quiz tracking variables
difficulty = ""
score = 0
question_count = 0
attempt = 1
num1 = 0
num2 = 0
operation = "+"
answer_entry = None
feedback_label = None


def clearWindow():
    for widget in root.winfo_children():
        widget.destroy()


def displayMenu():
    clearWindow()

    tk.Label(
        root,
        text="DIFFICULTY LEVEL",
        font=("Arial", 16, "bold"),
        bg="#e8f1f5",
        fg="#1f2d3d"
    ).pack(pady=(25, 5))

    tk.Label(
        root,
        text="Choose a level to start the quiz:",
        font=("Arial", 10),
        bg="#e8f1f5",
        fg="#1f2d3d"
    ).pack(pady=(0, 20))

    tk.Button(
        root,
        text="1. Easy",
        width=20,
        font=("Arial", 11),
        bg="white",
        command=lambda: startQuiz("easy")
    ).pack(pady=6)

    tk.Button(
        root,
        text="2. Moderate",
        width=20,
        font=("Arial", 11),
        bg="white",
        command=lambda: startQuiz("moderate")
    ).pack(pady=6)

    tk.Button(
        root,
        text="3. Difficult",
        width=20,
        font=("Arial", 11),
        bg="white",
        command=lambda: startQuiz("difficult")
    ).pack(pady=6)


def startQuiz(level):
    global difficulty, score, question_count
    difficulty = level
    score = 0
    question_count = 0
    displayProblem()


def randomInt(level):
    if level == "easy":
        return random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)


def decideOperation():
    return random.choice(["+", "-"])


def displayProblem():
    global question_count, attempt, num1, num2, operation, answer_entry, feedback_label

    if question_count >= 10:
        displayResults()
        return

    question_count += 1
    attempt = 1
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

    clearWindow()

    tk.Label(
        root,
        text=f"Question {question_count} / 10    |    Score: {score}",
        font=("Arial", 10, "bold"),
        bg="#e8f1f5",
        fg="#1f2d3d"
    ).pack(pady=(20, 25))

    tk.Label(
        root,
        text=f"{num1} {operation} {num2} =",
        font=("Arial", 22, "bold"),
        bg="#e8f1f5",
        fg="#1f2d3d"
    ).pack(pady=10)

    answer_entry = tk.Entry(root, font=("Arial", 14), width=12, justify="center")
    answer_entry.pack(pady=10)
    answer_entry.focus()
    answer_entry.bind("<Return>", checkAnswer)

    tk.Button(
        root,
        text="Submit Answer",
        font=("Arial", 11, "bold"),
        width=15,
        bg="#2b7de9",
        fg="white",
        command=checkAnswer
    ).pack(pady=10)

    feedback_label = tk.Label(root, text="", font=("Arial", 10), bg="#e8f1f5")
    feedback_label.pack(pady=5)


def isCorrect(user_ans):
    if operation == "+":
        correct_ans = num1 + num2
    else:
        correct_ans = num1 - num2

    if user_ans == correct_ans:
        if attempt == 1:
            messagebox.showinfo("Correct", "Correct! +10 points.")
        else:
            messagebox.showinfo("Correct", "Correct on second try! +5 points.")
        return True
    else:
        if attempt == 1:
            feedback_label.config(text="Incorrect. You have 1 more try for 5 points.", fg="red")
        else:
            messagebox.showinfo("Incorrect", f"Out of tries! The answer was {correct_ans}.")
        return False


def checkAnswer(event=None):
    global score, attempt
    raw = answer_entry.get().strip()

    try:
        user_ans = int(raw)
    except ValueError:
        feedback_label.config(text="Please enter a whole number.", fg="red")
        return

    if isCorrect(user_ans):
        if attempt == 1:
            score += 10
        else:
            score += 5
        displayProblem()
    else:
        if attempt == 1:
            attempt = 2
            answer_entry.delete(0, tk.END)
        else:
            displayProblem()


def displayResults():
    clearWindow()

    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    tk.Label(
        root,
        text="Quiz Complete!",
        font=("Arial", 18, "bold"),
        bg="#e8f1f5",
        fg="#1f2d3d"
    ).pack(pady=(30, 10))

    tk.Label(
        root,
        text=f"Final Score: {score} / 100",
        font=("Arial", 14),
        bg="#e8f1f5",
        fg="#1f2d3d"
    ).pack(pady=5)

    tk.Label(
        root,
        text=f"Grade: {grade}",
        font=("Arial", 16, "bold"),
        bg="#e8f1f5",
        fg="#1e8449" if score >= 50 else "#c0392b"
    ).pack(pady=(5, 25))

    tk.Button(
        root,
        text="Play Again",
        font=("Arial", 11, "bold"),
        width=16,
        bg="#2b7de9",
        fg="white",
        command=displayMenu
    ).pack(pady=5)

    tk.Button(
        root,
        text="Quit",
        font=("Arial", 11),
        width=16,
        bg="white",
        command=root.destroy
    ).pack(pady=5)


displayMenu()
root.mainloop()