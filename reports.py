"""O‘rtacha baho, reyting va eng yuqori natija.

Modul ikki qismdan iborat:
  1. Sof hisoblash funksiyalari (calculate_*, get_*) — natija qaytaradi,
     hech narsa chiqarmaydi. Barcha hisob-kitob shu yerda bitta joyda.
  2. Menu uchun show_* funksiyalari — hisoblash funksiyalarini chaqirib,
     natijani chiqaradi.

Qarorlar (izchil qo‘llanadi):
  - Umumiy o‘rtacha = BARCHA fanlardagi baholar yig‘indisi / baholar soni
    (fanlar o‘rtachalarining o‘rtachasi emas).
  - O‘rtacha 2 xona aniqlikda yaxlitlanadi; reyting ham shu yaxlitlangan
    qiymat bo‘yicha tuziladi, shunda ekrandagi son va o‘rin mos bo‘ladi.
  - Teng o‘rtachali o‘quvchilar bir xil o‘rinni oladi (1, 2, 2, 4 ...),
    o‘zaro tartib esa ism alifbosi bo‘yicha.
  - Bahosi yo‘q o‘quvchilar reytingga kirmaydi, alohida ko‘rsatiladi.
"""

from database import students
from utils import ask_student, print_table


# ---------- 1. Hisoblash funksiyalari ----------

def calculate_average(numbers):
    """Sonlar ro‘yxatining o‘rtachasi (2 xona); ro‘yxat bo‘sh bo‘lsa None."""
    if not numbers:  # nolga bo‘lish xatosining oldini olamiz
        return None
    return round(sum(numbers) / len(numbers), 2)


def get_all_grades(student):
    """O‘quvchining barcha fanlaridagi baholarni bitta ro‘yxatga yig‘adi."""
    all_grades = []
    for subject_grades in student["grades"].values():
        all_grades.extend(subject_grades)
    return all_grades


def get_student_average(student):
    """O‘quvchining umumiy o‘rtachasi; baholari bo‘lmasa None."""
    return calculate_average(get_all_grades(student))


def get_subject_averages(student):
    """Fan kesimida o‘rtacha: {"Python": 4.67, "English": 4.5}."""
    return {
        subject: calculate_average(subject_grades)
        for subject, subject_grades in student["grades"].items()
        if subject_grades
    }


def get_ranking(student_list):
    """Reytingni tuzadi.

    Qaytaradi: (ranking, unrated)
      ranking — [(o‘rin, o‘quvchi, o‘rtacha), ...] kamayish tartibida
      unrated — bahosi yo‘q o‘quvchilar ro‘yxati
    """
    rated = []
    unrated = []
    for student in student_list:
        average = get_student_average(student)
        if average is None:
            unrated.append(student)
        else:
            rated.append((student, average))

    # Avval o‘rtacha bo‘yicha kamayish (-average), teng bo‘lsa ism bo‘yicha.
    rated.sort(key=lambda item: (-item[1], item[0]["name"].lower()))

    ranking = []
    place = 0
    previous_average = None
    for index, (student, average) in enumerate(rated, start=1):
        if average != previous_average:  # teng natija bo‘lsa, o‘rin o‘zgarmaydi
            place = index
            previous_average = average
        ranking.append((place, student, average))

    return ranking, unrated


def get_top_students(student_list):
    """Eng yuqori o‘rtachali o‘quvchi(lar) va o‘rtacha: (ro‘yxat, o‘rtacha).

    Teng natija bo‘lsa, hammasi qaytariladi. Hech kimda baho bo‘lmasa ([], None).
    """
    ranking, _ = get_ranking(student_list)
    if not ranking:
        return [], None

    top = [student for place, student, average in ranking if place == 1]
    return top, ranking[0][2]


# ---------- 2. Menu uchun funksiyalar ----------

def show_average():
    """9. O‘quvchining umumiy va fan kesimidagi o‘rtacha bahosi."""
    print("\n--- O‘rtacha baho ---")
    student = ask_student(students)
    if student is None:
        return

    print(f"O‘quvchi: {student['name']} ({student['group']})")
    overall = get_student_average(student)
    if overall is None:
        print("Baholar mavjud emas.")
        return

    print(f"Umumiy o‘rtacha: {overall:.2f}")
    print("Fan kesimida:")
    for subject, average in get_subject_averages(student).items():
        count = len(student["grades"][subject])
        print(f"  {subject:<15} {average:.2f}  ({count} ta baho)")


def show_ranking():
    """10. O‘quvchilar reytingi (umumiy o‘rtacha bo‘yicha kamayish tartibida)."""
    print("\n--- O‘quvchilar reytingi ---")
    if not students:
        print("O‘quvchilar ro‘yxati bo‘sh.")
        return

    ranking, unrated = get_ranking(students)

    if ranking:
        rows = [
            (str(place), student["name"], student["group"], f"{average:.2f}")
            for place, student, average in ranking
        ]
        print_table(("O‘rin", "Ism", "Guruh", "O‘rtacha"), rows, right_aligned=(0, 3))
    else:
        print("Hali hech bir o‘quvchida baho yo‘q.")

    if unrated:
        names = ", ".join(f"{s['name']} ({s['group']})" for s in unrated)
        print(f"\nBahosi yo‘q o‘quvchilar: {names}")


def show_top_student():
    """11. Eng yuqori natijali o‘quvchi(lar)."""
    print("\n--- Eng yuqori natijali o‘quvchi ---")
    if not students:
        print("O‘quvchilar ro‘yxati bo‘sh.")
        return

    top, average = get_top_students(students)
    if not top:
        print("Hech bir o‘quvchida baho yo‘q, natijani aniqlab bo‘lmaydi.")
        return

    if len(top) == 1:
        print(f"{top[0]['name']} ({top[0]['group']}) — o‘rtacha: {average:.2f}")
    else:
        print(f"Teng natija! {len(top)} ta o‘quvchi — o‘rtacha: {average:.2f}")
        for student in top:
            print(f"  - {student['name']} ({student['group']})")
