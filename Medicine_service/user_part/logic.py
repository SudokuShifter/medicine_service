from datetime import datetime


def calculate_age(birthday):
    today = datetime.today().date()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    print(today, birthday)
    return age
