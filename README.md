# Can You Pass Engineering?

| | |
|---|---|
| **In-Class Project Title** | Can You Pass Engineering? |
| **Student Developer** | Arda Esas (250416007) |
| **Course** | EEM-2005 Programming |
| **Academic Term** | Fall 2026-2027 |
| **Instructor** | Assist. Prof. Dr. Ulya Bayram (@ubayram) |
| **University** | Çanakkale Onsekiz Mart University, Faculty of Engineering, Electrical and Electronics Engineering |

## Description

*Can You Pass Engineering?* is a text-based survival game about an Electrical and
Electronics Engineering student trying to get through four years of university.
The courses come from the real ÇOMÜ EEM curriculum, from Matematik I in the first
semester to Lazer Teorisi in the last one.

You start with **100 energy** and **3 burnout rights**. Every exam is a dice roll:
each course has its own pass chance, and harder courses cost more energy when you
fail them. If your energy drops to zero you burn out, lose the courses you passed
that semester and everything in your backpack, and have to start the semester
again. Burn out three times and you are dropped out of school. Pass all eight
semesters and you graduate.

Passing a course sometimes gets you a consumable from a classmate:

| Item | Effect |
|---|---|
| Kahve (Coffee) | +15% pass chance on your next exam |
| Kestirme (Power Nap) | +30 energy |
| Enerji İçeceği (Energy Drink) | +40 energy, but failing your next exam costs double |
| Ritalin | One extra try if you fail your next exam |
| Çıkmış Sorular (Past Exam Papers) | +25% pass chance on your next exam |

> The in-game text is in Turkish.

## How to Play

1. Start the game (see [Running the Game](#running-the-game)).
2. Every turn you see your energy, burnout rights, backpack and the courses left in the
   current semester.
3. Type a command:

| Input | Action |
|---|---|
| `1`, `2`, ... | Take the exam of that course |
| `e` | Use an item from your backpack |
| `r` | Restart the game |
| `q` | Quit |

4. In years 1 and 2 you must pass **every** course of the semester. In years 3 and 4
   some courses are electives, so passing 6 (year 3) or 5 (year 4) of them is enough.
5. Between semesters you rest: the winter break gives +20 energy, the summer break +50.
6. When the game ends, answer `e` (evet / yes) to start over or `h` (hayır / no) to quit.

**Tips:** use items *before* the exam they should affect, since their effect only
lasts for one exam. Save naps and energy drinks for when your energy is low, and
take the easier courses first in elective semesters.

## Requirements

- Python 3
- Jupyter Notebook

The game only uses Python's standard library (`random`, `time`, `collections`,
`dataclasses`, `typing`), so no extra libraries are needed. Jupyter Notebook can be
installed with:

```bash
pip install notebook
```

## Running the Game

**In a terminal:**

```bash
python muhendisligi-gecebilir-misin.py
```

**In Jupyter Notebook:** start Jupyter with `jupyter notebook`, create a new notebook
in this folder and run this in a cell:

```python
%run muhendisligi-gecebilir-misin.py
```
