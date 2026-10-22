"""Yordamchi funksiyalar: input tekshirish, o‘quvchi topish, jadval chiqarish."""

MIN_GRADE = 1
MAX_GRADE = 5


# ---------- Input tekshirish ----------

def read_text(prompt):
    """Bo‘sh bo‘lmagan matn kiritilguncha so‘raydi."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Xato: bo‘sh qiymat kiritib bo‘lmaydi.")


def read_int(prompt, allow_blank=False, min_value=None, max_value=None, range_message=None):
    """Butun son kiritilguncha so‘raydi.

    - allow_blank=True bo‘lsa, bo‘sh kiritish (Enter) None qaytaradi.
    - min_value / max_value berilsa, son shu oraliqda bo‘lishi shart.
    """
    while True:
        raw = input(prompt).strip()

        if raw == "":
            if allow_blank:
                return None
            print("Xato: bo‘sh qiymat kiritib bo‘lmaydi.")
            continue

        try:
            number = int(raw)
        except ValueError:
            print("Xato: butun son kiriting (masalan: 5).")
            continue

        too_small = min_value is not None and number < min_value
        too_big = max_value is not None and number > max_value
        if too_small or too_big:
            print(range_message or "Xato: son ruxsat etilgan oraliqda emas.")
            continue

        return number


def read_age(prompt, allow_blank=False):
    """Yoshni so‘raydi: musbat butun son (1 dan 120 gacha)."""
    return read_int(
        prompt,
        allow_blank=allow_blank,
        min_value=1,
        max_value=120,
        range_message="Xato: yosh musbat son bo‘lishi kerak (1–120).",
    )


def read_grade(prompt):
    """Bahoni so‘raydi: faqat 1 dan 5 gacha butun son."""
    return read_int(
        prompt,
        min_value=MIN_GRADE,
        max_value=MAX_GRADE,
        range_message=f"Xato: baho {MIN_GRADE} dan {MAX_GRADE} gacha bo‘lishi kerak.",
    )


# ---------- O‘quvchi topish ----------

def find_student_by_id(students, student_id):
    """ID bo‘yicha o‘quvchini qaytaradi, topilmasa None."""
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def ask_student(students, prompt="O‘quvchi ID sini kiriting"):
    """Foydalanuvchidan ID so‘rab, o‘quvchini topib beradi.

    Muammo bo‘lsa (ro‘yxat bo‘sh, ID topilmadi, bekor qilindi) xabar
    chiqarib None qaytaradi.
    """
    if not students:
        print("O‘quvchilar ro‘yxati bo‘sh.")
        return None

    student_id = read_int(f"{prompt} (bekor qilish uchun Enter): ", allow_blank=True)
    if student_id is None:
        print("Amal bekor qilindi.")
        return None

    student = find_student_by_id(students, student_id)
    if student is None:
        print(f"Xato: ID = {student_id} bo‘lgan o‘quvchi topilmadi.")
    return student


# ---------- Chiroyli chiqarish ----------

def print_table(headers, rows, right_aligned=()):
    """Umumiy jadval chiqaruvchi.

    headers       — ustun nomlari (tuple)
    rows          — qatorlar ro‘yxati (har biri matnlardan iborat tuple)
    right_aligned — o‘ngga tekislanadigan ustun indekslari (masalan, raqamlar)
    """
    widths = [
        max([len(headers[i])] + [len(row[i]) for row in rows])
        for i in range(len(headers))
    ]

    def build_line(cells):
        parts = []
        for i, cell in enumerate(cells):
            if i in right_aligned:
                parts.append(cell.rjust(widths[i]))
            else:
                parts.append(cell.ljust(widths[i]))
        return " | ".join(parts)

    header_line = build_line(headers)
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print(build_line(row))


def print_students(students, heading, empty_message="O‘quvchilar topilmadi."):
    """O‘quvchilar ro‘yxatini chiqaradi (ID, ism, yosh, guruh). Baholar chiqarilmaydi."""
    print(f"\n--- {heading} ---")

    if not students:
        print(empty_message)
        return

    rows = [
        (str(s["id"]), s["name"], str(s["age"]), s["group"])
        for s in students
    ]
    print_table(("ID", "Ism", "Yosh", "Guruh"), rows, right_aligned=(0, 2))
    print(f"Jami: {len(students)} ta o‘quvchi")
