"""Ma’lumotlar ombori (hozircha faqat xotirada, list va dict ko‘rinishida).

Ma’lumotlar tuzilishi — ichma-ich list va dict:

    students = [                         # list: o‘quvchilar ro‘yxati
        {                                # dict: bitta o‘quvchi
            "id": 1,
            "name": "Ali Valiyev",
            "age": 16,
            "group": "Python-01",
            "grades": {                  # dict: fan nomi -> baholar ro‘yxati
                "Python": [5, 4, 5],     # list: shu fandagi baholar
                "English": [4, 5],
            },
        },
    ]

Dastur yopilganda ma’lumotlar yo‘qoladi.
"""

# Namunaviy o‘quvchilar (reyting va teng natijalarni darhol ko‘rish uchun).
# Dilnoza va Ali baholari bir xil -> o‘rtachasi teng (4.6).
# Bobur esa hali baho olmagan.
students = [
    {
        "id": 1,
        "name": "Ali Valiyev",
        "age": 16,
        "group": "Python-01",
        "grades": {"Python": [5, 4, 5], "English": [4, 5]},
    },
    {
        "id": 2,
        "name": "Madina Karimova",
        "age": 17,
        "group": "Python-01",
        "grades": {"Python": [5, 5], "Math": [4]},
    },
    {
        "id": 3,
        "name": "Sardor Aliyev",
        "age": 15,
        "group": "Python-02",
        "grades": {"Python": [3, 4]},
    },
    {
        "id": 4,
        "name": "Dilnoza Rahimova",
        "age": 16,
        "group": "Python-02",
        "grades": {"Python": [5, 4, 5], "English": [4, 5]},
    },
    {
        "id": 5,
        "name": "Bobur Tursunov",
        "age": 18,
        "group": "Python-02",
        "grades": {},
    },
]

# Keyingi o‘quvchi ID si. Butun son o‘rniga dict ishlatilgan, chunki boshqa
# modul ichida o‘zgartirilganda ham qiymat hamma joyda bir xil bo‘lib qoladi.
counter = {"next_student_id": 6}


def get_next_id():
    """Yangi, takrorlanmaydigan ID qaytaradi va hisoblagichni oshiradi."""
    new_id = counter["next_student_id"]
    counter["next_student_id"] += 1
    return new_id
