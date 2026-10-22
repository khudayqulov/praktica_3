"""Baholar bilan ishlash: baho qo‘shish va o‘quvchi baholarini ko‘rish."""

from database import students
from utils import ask_student, read_grade, read_text


def find_existing_subject(grades, subject):
    """`grades` ichida shu fan bormi? Katta-kichik harfga e’tibor bermaydi.

    Topilsa — mavjud kalitni ("Python"), topilmasa None qaytaradi.
    Shunda "python" va "Python" ikkita alohida fan bo‘lib ketmaydi.
    """
    for existing in grades:
        if existing.lower() == subject.lower():
            return existing
    return None


def add_grade():
    """7. O‘quvchiga baho qo‘shadi.

    Fan yangi bo‘lsa — grades ichida yangi kalit yaratiladi,
    mavjud bo‘lsa — baho shu fan ro‘yxatiga qo‘shiladi.
    """
    print("\n--- Baho qo‘shish ---")
    student = ask_student(students)
    if student is None:
        return

    subject = read_text("Fan nomi: ")
    grade = read_grade("Baho (1–5): ")

    # Avval mavjud fanni qidiramiz; bo‘lmasa, kiritilgan nom yangi kalit bo‘ladi.
    key = find_existing_subject(student["grades"], subject) or subject
    student["grades"].setdefault(key, []).append(grade)

    print(f"{student['name']} uchun '{key}' fanidan {grade} baho qo‘shildi.")


def show_student_grades():
    """8. O‘quvchining har bir fani va shu fandagi baholarini ko‘rsatadi."""
    print("\n--- O‘quvchining baholari ---")
    student = ask_student(students)
    if student is None:
        return

    print(f"O‘quvchi: {student['name']} ({student['group']})")
    if not student["grades"]:
        print("Bu o‘quvchida hali baholar yo‘q.")
        return

    for subject, subject_grades in student["grades"].items():
        print(f"  {subject}: {', '.join(str(g) for g in subject_grades)}")
