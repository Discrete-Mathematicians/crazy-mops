from datetime import date
from pets.models import Pet

def get_upcoming_birthdays(user):
    return (
        Pet.objects
        .filter(subscription__user=user)
        .exclude(birthday__isnull=True)
    )

def sort_by_nearest_birthday(pets):
    def days_until(pet):
        today = date.today()
        try:
            next_bday = pet.birthday.replace(year=today.year)
        except ValueError:
            # 29 февраля в невисокосном году - считаем как 1 марта
            next_bday = date(today.year, 3, 1)
        if next_bday < today:
            try:
                next_bday = next_bday.replace(year=today.year + 1)
            except ValueError:
                next_bday = date(today.year + 1, 3, 1)
        return (next_bday - today).days

    return sorted(pets, key=days_until)
