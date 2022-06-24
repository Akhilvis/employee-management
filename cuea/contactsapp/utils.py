

from .models import Section, Unit

def handle_uploaded_file(f):
    with open('employee_csv.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def load_data():
    Unit.objects.bulk_create([Unit(unit=i) for i in range(1, 10)])
    sections_set = set()
    f = open("sections_list.txt", "r")
    for line in f.readlines():
        sections_set.add(line.strip())
    for section in sections_set:
        unit = Unit.objects.first()
        Section.objects.create(section=section, unit=unit)