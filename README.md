# Student Management System

Terminalda ishlaydigan o‘quvchilarni boshqarish tizimi (faqat Python standart kutubxonasi, `class`siz).

## Ishga tushirish

Python 3.8+ kerak. Loyiha papkasida:

```bash
cd student_management
python main.py        # Linux/macOS'da: python3 main.py
```

Menyudan `0` ni tanlasangiz, dastur tugaydi. Ma’lumotlar faqat xotirada saqlanadi — dastur yopilganda yo‘qoladi. Dastur 5 ta namunaviy o‘quvchi bilan boshlanadi (reyting va teng natijalarni darhol ko‘rish uchun); xohlasangiz, ularni menyudan o‘chirib tashlashingiz mumkin.

## Fayllar va vazifalari

| Fayl | Vazifasi |
|------|----------|
| `main.py` | Menyu va dastur oqimi. Hisob-kitob mantiqi yo‘q — faqat funksiyalarni chaqiradi. |
| `students.py` | O‘quvchini qo‘shish, ko‘rish, tahrirlash, o‘chirish, ID va ism bo‘yicha qidirish. |
| `grades.py` | O‘quvchiga baho qo‘shish va baholarini ko‘rish. |
| `reports.py` | O‘rtacha baho, reyting, eng yuqori natija (hisoblash + chiqarish). |
| `utils.py` | Input tekshirish, o‘quvchini ID bo‘yicha topish, jadval chiqarish. |
| `database.py` | `students` ro‘yxati va ID hisoblagichi. |

## O‘quvchi ma’lumotlari qanday tashkil qilingan

Ichma-ich `list` → `dict` → `dict` → `list`:

```python
students = [                          # list: o‘quvchilar ro‘yxati
    {                                 # dict: bitta o‘quvchi
        "id": 1,
        "name": "Ali Valiyev",
        "age": 16,
        "group": "Python-01",
        "grades": {                   # dict: fan nomi -> baholar
            "Python":  [5, 4, 5],     # list: shu fandagi baholar
            "English": [4, 5],
        },
    },
]
```

Baho qo‘shish shu tuzilmaga tayanadi: fan `grades` ichida bor bo‘lsa — baho uning ro‘yxatiga `append` qilinadi, yo‘q bo‘lsa — yangi kalit yaratiladi (`setdefault(fan, []).append(baho)`). Fan nomi katta-kichik harfni farqlamasdan solishtiriladi, shuning uchun `python` va `Python` ikkita alohida fan bo‘lib ketmaydi.

## O‘rtacha baho qanday hisoblanadi

**Umumiy o‘rtacha = barcha fanlardagi baholar yig‘indisi ÷ baholar soni.**

Misol (Ali): `Python [5, 4, 5]` + `English [4, 5]` → `(5+4+5+4+5) / 5 = 4.60`.

Bu *fanlar o‘rtachalarining o‘rtachasi* emas: o‘sha misolda u `(4.67 + 4.50) / 2 = 4.58` bo‘lardi. Biz hamma baho teng vazn bilan hisoblanadigan variantni tanladik.

Hisob-kitob zanjiri (`reports.py`):

```
get_all_grades(student)          ← barcha fanlarning baholarini bitta ro‘yxatga yig‘adi
  └── calculate_average(list)    ← sum / len; ro‘yxat bo‘sh bo‘lsa None (nolga bo‘lish yo‘q)
        ├── get_student_average(student)   ← umumiy o‘rtacha
        └── get_subject_averages(student)  ← fan kesimida o‘rtacha
```

O‘rtacha 2 xona aniqlikda yaxlitlanadi. Reyting ham shu yaxlitlangan qiymat bo‘yicha tuziladi, shunda ekrandagi son va o‘rin bir-biriga mos bo‘ladi.

## Reyting va teng natijalar qoidasi

- O‘quvchilar umumiy o‘rtacha bo‘yicha **kamayish** tartibida saralanadi.
- Teng o‘rtachali o‘quvchilar **bir xil o‘rinni** oladi (`1, 2, 2, 4` ko‘rinishida), o‘zaro tartib esa ism alifbosi bo‘yicha.
- Bahosi yo‘q o‘quvchilar reytingga kirmaydi, jadval ostida alohida ko‘rsatiladi.
- "Eng yuqori natijali o‘quvchi" ham xuddi shu reytingdan olinadi: 1-o‘rindagi **hamma** o‘quvchi ko‘rsatiladi (teng bo‘lsa, ikkalasi ham).

## Modullar bir-biri bilan qanday ishlaydi

```
main.py ──► students.py ──┐
   │                      ├──► utils.py   (input tekshirish, ask_student, jadval)
   ├─────► grades.py   ───┤
   │                      ├──► database.py (students ro‘yxati, ID hisoblagichi)
   └─────► reports.py  ───┘
```

- `main.py` faqat menyu raqamini mos funksiyaga bog‘laydi (`ACTIONS` lug‘ati).
- `students.py`, `grades.py`, `reports.py` ma’lumotni `database.students` dan oladi va tekshiruv uchun `utils.py` ga tayanadi.
- Menyu funksiyalari ichida ID so‘rash, bo‘sh ro‘yxat va "topilmadi" holatlari `utils.ask_student()` da **bitta joyda** boshqariladi.
- `reports.py` ichida hisoblash funksiyalari (`calculate_*`, `get_*`) hech narsa chiqarmaydi, `show_*` funksiyalari esa faqat chiqaradi.

## Asosiy funksiyalar

**`students.py`**
- `show_all_students()` — ID, ism, yosh, guruhni jadvalda chiqaradi (baholarsiz).
- `add_student()` — ism, yosh, guruhni tekshirib, avtomatik ID va bo‘sh `grades` bilan qo‘shadi.
- `edit_student()` — Enter bosilsa eski qiymat saqlanadi.
- `delete_student()` — faqat tanlangan o‘quvchini o‘chiradi.
- `search_by_id()` / `search_by_name()` — ID bo‘yicha aniq, ism bo‘yicha qisman va katta-kichik harfni farqlamasdan qidiradi.

**`grades.py`**
- `add_grade()` — o‘quvchi, fan va bahoni (1–5) tekshirib saqlaydi.
- `find_existing_subject()` — fan nomini katta-kichik harfsiz qidiradi.
- `show_student_grades()` — har bir fan va undagi baholarni chiqaradi.

**`reports.py`**
- `calculate_average()`, `get_all_grades()`, `get_student_average()`, `get_subject_averages()` — hisoblash.
- `get_ranking()` — reytingni tuzadi: `(reyting, bahosizlar)` qaytaradi. Reyting ham, eng yuqori natija ham shu bitta funksiyaga tayanadi.
- `get_top_students()` — 1-o‘rindagi o‘quvchi(lar)ni qaytaradi.
- `show_average()`, `show_ranking()`, `show_top_student()` — menyu 9, 10, 11.

**`utils.py`**
- `read_text()`, `read_int()`, `read_age()` (1–120), `read_grade()` (1–5) — input tekshirish.
- `find_student_by_id()`, `ask_student()` — o‘quvchini topish va xatolarni boshqarish.
- `print_table()` — umumiy jadval chiqaruvchi; `print_students()` va reyting jadvali shundan foydalanadi.

## Qisqa demo

1. `10` → reyting: Madina 4.67 (1-o‘rin), Ali va Dilnoza 4.60 (ikkalasi 2-o‘rin), Sardor 3.50 (4-o‘rin); Bobur bahosizlar qatorida.
2. `9` → ID `1` → Ali: umumiy 4.60; Python 4.67, English 4.50.
3. `9` → ID `5` → Bobur: "Baholar mavjud emas."
4. `7` → ID `5`, fan `Python`, baho `5` → Bobur endi reytingga kiradi.
5. `11` → eng yuqori natijali o‘quvchi.
6. `2` → yangi o‘quvchi qo‘shing, `6` → ism bo‘yicha qisman (`ali`) qidiring.

## Xatolik holatlarini sinab ko‘rish

- O‘quvchi qo‘shishda yoshga `abc`, `-3`, `0` kiriting — rad etiladi.
- Bahoga `0`, `6`, `abc` kiriting — rad etiladi (faqat 1–5).
- Fan nomini bo‘sh qoldiring — rad etiladi.
- Mavjud bo‘lmagan ID (`99`) bilan qidiring, tahrirlang, o‘chiring.
- Barcha o‘quvchilarni o‘chiring, so‘ng har bir menyu bandini oching — hammasi "ro‘yxat bo‘sh" deydi.
- Bahosi yo‘q o‘quvchi uchun `8`, `9` ni oching.
- Ikki o‘quvchiga bir xil baholar bering — reytingda bir xil o‘rin oladilar.
