Programming Skills Portfolio — CodeLab II

This repository contains my solutions for the CodeLab II Programming Skills Portfolio. Each exercise is built with Python and Tkinter to demonstrate GUI layout design, event-driven programming, file handling, and object-oriented structure.

Repository Structure

-Programming-Skills-Portfolio/
├── 01-MathsQuiz/
│   └── MathsQuiz.py
├── 02-AlexaTellMeAJoke/
│   ├── JokeApp.py
│   └── randomJokes.txt
├── 03-StudentManager/
│   ├── StudentManager.py
│   └── studentMarks.txt
└── README.md


Exercises

1. Maths Quiz (01-MathsQuiz)

A 10-question arithmetic quiz with three difficulty levels (Easy, Moderate, and Difficult).

Dynamically switches between the menu, quiz screen, and results screen inside a single window.

Generates random addition and subtraction questions scaled by difficulty.

Awards 10 points on the first attempt and 5 points on the second attempt, with input validation and final letter grading (A+ to F).




2. Alexa Tell Me a Joke (02-AlexaTellMeAJoke)

A desktop joke assistant that reads setup-and-punchline pairs from randomJokes.txt.

Loads and parses jokes on startup with checks for missing or empty files.

Picks random jokes without repeating the previous joke back-to-back.

Separates the setup and punchline into two steps by toggling button states.




3. Student Manager (03-StudentManager)

A student record management app that reads from and saves updates to studentMarks.txt.

Uses a Student class to validate inputs and calculate totals, percentages, and grades (A–F).

Displays records in a ttk.Treeview table with green/red row highlights for A and F grades.

Supports searching by name or code, sorting by overall mark, viewing highest/lowest scores, and adding, updating, or deleting records.


Raster Bulabos Rasca

CodeLab II — Programming Skills Portfolio
