import hashlib
import openpyxl
import secrets
import string


def generate_password():
    letters = [
        secrets.choice(string.ascii_uppercase),
        *[secrets.choice(string.ascii_lowercase) for _ in range(2)],
        secrets.choice(string.ascii_uppercase)]
    digits = [secrets.choice(string.digits) for _ in range(4)]
    return ''.join(letters) + ''.join(digits)


# # НЕЗАБУДЬ ПОМЕНЯТЬ RANGE!!!
# # Старт - номер строки экселя с которой начинать
# # Конец - номер строки экселя + 1!
# book = openpyxl.load_workbook('pwd.xlsx')
# sheet = book['Center']
# for i in range(304, 312):
#     sheet[f'C{i}'] = generate_password()
#     sheet[f'D{i}'] = hashlib.sha512(
#         sheet[f'C{i}'].value.encode('utf-8')).hexdigest()
# book.save('pwd.xlsx')

pwd = 'VbyT7289'
result = hashlib.sha512(pwd.encode('utf-8')).hexdigest()
print(result)
