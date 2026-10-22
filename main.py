"""Student Management System — dasturning kirish nuqtasi.

Ishga tushirish:  python main.py

Bu faylda hisob-kitob mantiqi yo‘q: faqat menyu va funksiyalarni chaqirish.
"""

from grades import add_grade, show_student_grades
from reports import show_average, show_ranking, show_top_student
from students import (
    add_student,
    delete_student,
    edit_student,
    search_by_id,
    search_by_name,
    show_all_students,
)

MENU_TEXT = """
===== STUDENT MANAGEMENT SYSTEM =====
1. Barcha o‘quvchilarni ko‘rish
2. O‘quvchi qo‘shish
3. O‘quvchi ma’lumotlarini tahrirlash
4. O‘quvchini o‘chirish
5. O‘quvchini ID orqali qidirish
6. O‘quvchini ism orqali qidirish
7. O‘quvchiga baho qo‘shish
8. O‘quvchining baholarini ko‘rish
9. O‘rtacha bahoni ko‘rish
10. O‘quvchilar reytingi
11. Eng yuqori natijali o‘quvchi
0. Chiqish"""

# Menu raqami -> bajariladigan funksiya
ACTIONS = {
    "1": show_all_students,
    "2": add_student,
    "3": edit_student,
    "4": delete_student,
    "5": search_by_id,
    "6": search_by_name,
    "7": add_grade,
    "8": show_student_grades,
    "9": show_average,
    "10": show_ranking,
    "11": show_top_student,
}


def show_menu():
    """Menyuni ekranga chiqaradi."""
    print(MENU_TEXT)


def main():
    """Foydalanuvchi 0 ni tanlamaguncha menyuni takrorlaydi."""
    while True:
        show_menu()
        choice = input("Tanlovingiz: ").strip()

        if choice == "0":
            print("Dasturdan chiqildi. Xayr!")
            break

        action = ACTIONS.get(choice)
        if action is None:
            print("Xato: noto‘g‘ri tanlov. 0 dan 11 gacha raqam kiriting.")
            continue

        action()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nDastur to‘xtatildi. Xayr!")