"""O‘quvchilar ustidagi amallar: qo‘shish, ko‘rish, tahrirlash, o‘chirish, qidirish."""

from database import get_next_id, students
from utils import ask_student, print_students, read_age, read_text


def show_all_students():
    """1. Barcha o‘quvchilarni ko‘rsatadi (baholarsiz)."""
    print_students(students, "Barcha o‘quvchilar", "Hozircha o‘quvchilar yo‘q.")


def add_student():
    """2. Yangi o‘quvchi qo‘shadi (ID avtomatik, grades — bo‘sh lug‘at)."""
    print("\n--- Yangi o‘quvchi qo‘shish ---")
    name = read_text("Ism familiya: ")
    age = read_age("Yosh: ")
    group = read_text("Guruh nomi: ")

    student = {
        "id": get_next_id(),
        "name": name,
        "age": age,
        "group": group,
        "grades": {},
    }
    students.append(student)
    print(f"O‘quvchi qo‘shildi. ID = {student['id']}")


def edit_student():
    """3. Ism, yosh yoki guruhni tahrirlaydi (Enter — eski qiymat saqlanadi)."""
    print("\n--- O‘quvchi ma’lumotlarini tahrirlash ---")
    student = ask_student(students)
    if student is None:
        return

    print("Eski qiymatni saqlab qolish uchun shunchaki Enter bosing.")

    new_name = input(f"Yangi ism [{student['name']}]: ").strip()
    new_age = read_age(f"Yangi yosh [{student['age']}]: ", allow_blank=True)
    new_group = input(f"Yangi guruh [{student['group']}]: ").strip()

    if new_name:
        student["name"] = new_name
    if new_age is not None:
        student["age"] = new_age
    if new_group:
        student["group"] = new_group

    print("O‘quvchi ma’lumotlari yangilandi.")


def delete_student():
    """4. O‘quvchini ID bo‘yicha o‘chiradi (boshqalarga ta’sir qilmaydi)."""
    print("\n--- O‘quvchini o‘chirish ---")
    student = ask_student(students)
    if student is None:
        return

    students.remove(student)
    print(f"'{student['name']}' o‘chirildi.")


def search_by_id():
    """5. ID bo‘yicha aniq qidiradi."""
    print("\n--- ID orqali qidirish ---")
    student = ask_student(students)
    if student is None:
        return

    print_students([student], "Topilgan o‘quvchi")


def search_by_name():
    """6. Ism bo‘yicha qidiradi (qisman moslik, katta-kichik harf farq qilmaydi)."""
    print("\n--- Ism orqali qidirish ---")
    if not students:
        print("O‘quvchilar ro‘yxati bo‘sh.")
        return

    query = read_text("Ism (to‘liq yoki qisman): ").lower()
    results = [s for s in students if query in s["name"].lower()]
    print_students(results, f"Qidiruv natijalari: '{query}'", "Hech kim topilmadi.")
