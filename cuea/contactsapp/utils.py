

def handle_uploaded_file(f):
    with open('employee_csv.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)