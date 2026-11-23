Programming Skills Portfolio — CodeLab II

A collection of three interactive desktop applications built in Python using Tkinter, demonstrating event-driven GUI development, file input/output, input validation, and object-oriented programming.

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


Exercises Overview

1. Maths Quiz (01-MathsQuiz)

An interactive 10-question arithmetic quiz featuring three difficulty levels (Easy, Moderate, and Difficult).

Key Features:

Single-window dynamic screen transitions (clearWindow()).

Difficulty-scaled random addition and subtraction problems (1–9, 10–99, 1000–9999).

Two-attempt scoring system (10 points on first try, 5 points on second try) with inline feedback.

Numeric input validation (try-except) and Enter key submission.

Automated final score and letter grade (A+ to F) summary screen.



2. Alexa Tell Me a Joke (02-AlexaTellMeAJoke)

A GUI joke-telling assistant that loads setup-and-punchline pairs from an external text file (randomJokes.txt).

Key Features:

File reading and string parsing with error handling for missing or empty files.

Non-repeating random joke selection (random.choice()).

Two-step setup and punchline reveal flow with dynamic button state toggling.

Wrapped text labels for clean formatting inside a fixed window layout.




3. Student Manager (03-StudentManager)

An object-oriented student record management system backed by persistent storage in studentMarks.txt.

Key Features:

Encapsulated Student data model with strict input validation and @property calculations for coursework total (/60), overall mark (/160), percentage, and letter grade (A–F).

Interactive ttk.Treeview table with color-coded A (green) and F (red) rows.

Live search filtering by student name or 4-digit code.

View and Sort menus for full class summaries, highest/lowest marks, and ascending/descending sorting.

Reusable modal form dialog (StudentFormDialog) for adding, updating, and deleting records with automatic file saving.



Raster Bulabos Rasca

CodeLab II — Programming Skills Portfolio
