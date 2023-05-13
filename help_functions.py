import pytest
import time
import string
import random
import imaplib
import email
import re
from params_imap import *


# Ищем капчу и пропускаем тест при её наличии (ментор сказал, что отключить её никак низзя, поэтому придумала такой ход)
def captcha_search(page):
    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")


# Если на странице есть таймер активности кнопки, ждём указанное время
def code_timer_wait(page):
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))


# Ожидание активности для кнопки "Отправить код повторно"
def resend_timer_wait(page):
    if page.resend_timeout.is_visible():
        time.sleep((int(page.resend_timeout.get_text().split()[5])))


# Генерируем рандомную строку, чтобы добавить её в email для регистрации
def generate_alphanum_random_string(length):
    letters_and_digits = string.ascii_lowercase + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string


# Получаем код авторизации из письма на mail.ru
def code_from_email():
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(mailru, imap_password)
    imap.select("INBOX")
    imap.search(None, "All")
    code_in = str(imap.search(None, "All")[1]).split()[-1].replace("']", "")  # получаем номер последнего письма
    res, msg = imap.fetch(code_in, '(RFC822)')
    msg = email.message_from_bytes(msg[0][1])  # извлекаем письмо

    code = ''
    for part in msg.walk():
        if part.get_content_maintype() == 'text':
            text = str(part.get_payload())
            code = re.search(r'\d{6}', text).group()  # находим код через регулярное выражение

    return code
