from functions.help_functions import *
from parameters.params_test import *


# 1. ПО КОДУ (авторизация и авторегистрация) - в user передаём email или номер телефона
def code_auth_fill_fields(page, user):
    captcha_search(page)
    page.email_ad_form.send_keys(user)
    code_timer_wait(page)
    page.btn_get_code.click()
    page.wait_page_loaded()


# 2. ПАРОЛЬ (авторизация):
# 2.1. USER - заполняем и отправляем форму - в user передаём email, номер телефона или логин
def password_auth_fill_fields(page, user):
    to_password_auth(page)
    page.email_us_form.send_keys(user)
    page.password_form.send_keys(valid_password)
    captcha_search(page)
    code_timer_wait(page)
    page.btn_login.click()
    page.wait_page_loaded()


# 2.2. INVALID_PASS - заполняем и отправляем форму - в user передаём email, телефон или логин
def password_auth_fill_fields_invalid_pass(page, user, invalid_password):
    to_password_auth(page)
    page.email_us_form.send_keys(user)
    page.password_form.send_keys(invalid_password)
    captcha_search(page)
    code_timer_wait(page)
    page.btn_login.click()
    page.wait_page_loaded()


# 3. РЕГИСТРАЦИЯ полная
# 3.1. ПОЧТА - заполняем и отправляем форму, меняя EMAIL:
def reg_fill_fields_email(page, email):
    to_registration(page)
    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)
    captcha_search(page)
    page.email_ad_form.send_keys(email)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)
    code_timer_wait(page)
    page.btn_reg.click()
    page.wait_page_loaded()


# 3.2. ИМЕНА - заполняем и отправляем форму, меняя имя (позитивные - с неполным сценарием):
def reg_fill_fields_names_pos(page, name):
    to_registration(page)
    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)
    captcha_search(page)
    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)
    # Код закрыт, чтобы не создавать кучу учёток, которые не получится удалить
    # assert page.error_reg_forms.is_presented() is False
    # code_timer_wait(page)
    # page.btn_reg.click()
    # page.wait_page_loaded()


# 3.3. ИМЕНА - заполняем и отправляем форму, меняя имя (негативные - с полным сценарием):
def reg_fill_fields_names_neg(page, name):
    to_registration(page)
    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)
    captcha_search(page)
    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)
    code_timer_wait(page)
    page.btn_reg.click()
    page.wait_page_loaded()


# 3.4. ФАМИЛИИ - заполняем и отправляем форму, меняя фамилию (позитивные - с неполным сценарием):
def reg_fill_fields_lastnames_pos(page, lastname):
    to_registration(page)
    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)
    captcha_search(page)
    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)
    # Код закрыт, чтобы не создавать кучу учёток, которые не получится удалить
    # assert page.error_reg_forms.is_presented() is False
    # code_timer_wait(page)
    # page.btn_reg.click()
    # page.wait_page_loaded()


# 3.5. ФАМИЛИИ - заполняем и отправляем форму, меняя фамилию (негативные - с полным сценарием):
def reg_fill_fields_lastnames_neg(page, lastname):
    to_registration(page)
    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)
    captcha_search(page)
    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)
    code_timer_wait(page)
    page.btn_reg.click()
    page.wait_page_loaded()


# 3.6. ПАРОЛИ - заполняем и отправляем форму, меняя пароль:
def reg_fill_fields_password(page, password):
    to_registration(page)
    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)
    captcha_search(page)
    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(password)
    page.password_confirm_form.send_keys(password)
    code_timer_wait(page)
    page.btn_reg.click()
    page.wait_page_loaded()


# 3.7. ПАРОЛИ НЕ СОВПАДАЮТ:
def reg_fill_fields_confirm_password(page, valid_password, invalid_password):
    to_registration(page)
    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)
    captcha_search(page)
    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(invalid_password)
    code_timer_wait(page)
    page.btn_reg.click()
    page.wait_page_loaded()


# 4. ВОССТАНОВЛЕНИЕ ПАРОЛЯ - в user передаём email или номер телефона
def reset_pass_fill_fields(page, user):
    page.email_us_form.send_keys(user)
    code_timer_wait(page)
    page.btn_reset.click()
    page.wait_page_loaded()
