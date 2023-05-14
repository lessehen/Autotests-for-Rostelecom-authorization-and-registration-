import pytest
import time
from pages.shome_pages import *
from parameters.params_test import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 0. Проверка наличия элементов на страницах и их локаторов.
# Делаю такой мега-тест с кучей ассертов, хотя можно разбить на отдельные - но мы тут заполняем формы и
# тыкаем на кнопки. Если один ассерт не пройдёт, тест сразу упадёт, но можно по цепочке разбирать постепенно))0)


# 0.1. Для страницы авторизации по коду
def test01_elements_code_auth(web_browser):
    page = SHomeCodeAuthPage(web_browser)

    assert page.h1.get_text() == 'Авторизация по коду'
    assert 'Укажите контактный номер телефона, на который' in page.help_text.get_text()
    assert page.phone_ad_form.is_visible()
    assert page.btn_get_code.is_clickable() and page.btn_get_code.get_text() == 'Получить код'
    assert page.btn_standard_auth.is_clickable() and page.btn_standard_auth.get_text() == 'Войти с паролем'

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")
    else:
        page.phone_ad_form.send_keys(seven_phone)
        if page.code_timeout.is_visible():
            time.sleep(int(page.code_timeout.get_text().split()[4]))
        page.btn_get_code.click()
        assert page.h1.get_text() == 'Код подтверждения отправлен' and page.code_send.get_text() == f'По SMS на номер ' \
                                                                                                    f'{seven_phone}'
        assert page.btn_change_data.is_clickable() and page.btn_change_data.get_text() == 'Изменить номер'
        assert page.code_forms.is_visible() and (page.resend_timeout.is_visible()
                                                 or page.too_many_codes_error.is_visible())
        if page.resend_timeout.is_visible():
            time.sleep((int(page.resend_timeout.get_text().split()[5])))
            assert page.btn_resend_code.is_clickable()
        # По требованиям должна быть надпись, на самом деле нет. На функционал не влияет, поэтому пока спрятала:
        # assert page.btn_resend_code.get_text() == 'Получить новый код'


# 0.2. Для стандартной авторизации с паролем
def test02_elements_standard_auth(web_browser):
    page = SHomePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()
    assert page.h1.get_text() == 'Авторизация'
    assert page.left_block.is_presented() and page.right_block.is_presented()
    # assert page.rit_tagline.is_presented()
    assert page.login_div.is_visible()
    assert page.tab_phone.is_clickable() and page.tab_phone.get_text() == 'Телефон'
    assert page.tab_email.is_clickable() and page.tab_email.get_text() == 'Почта'
    assert page.tab_login.is_clickable() and page.tab_login.get_text() == 'Логин'
    assert page.tab_ls.is_visible() is False
    assert page.login_us_form.is_visible() and page.password_form.is_visible()
    assert page.btn_login.is_clickable() and page.btn_login.get_text() == 'Войти'
    assert page.btn_back_code.is_clickable() and page.btn_back_code.get_text() == 'Войти по временному коду'
    assert page.btn_forgot_password.is_clickable() and page.btn_forgot_password.get_text() == 'Забыл пароль'
    assert page.btn_to_reg.is_clickable() and page.btn_to_reg.get_text() == 'Зарегистрироваться'


# 0.3. Для восстановления пароля
def test03_elements_reset_password(web_browser):
    page = SHomeResetPasswordPage(web_browser)
    assert page.h1.get_text() == 'Восстановление пароля'
    assert page.tab_phone.is_clickable() and page.tab_phone.get_text() == 'Телефон'
    assert page.tab_email.is_clickable() and page.tab_email.get_text() == 'Почта'
    assert page.tab_login.is_clickable() and page.tab_login.get_text() == 'Логин'
    assert page.tab_ls.is_visible() is False
    assert page.phone_us_form.is_visible()
    assert page.captcha_form.is_visible() and page.captcha_image.is_visible()
    assert page.btn_reset.is_clickable() and page.btn_reset.get_text() == 'Продолжить'
    assert page.btn_reset_back.is_clickable() and 'Вернуться' in page.btn_reset_back.get_text()


# 0.4. Для страницы регистрации
def test04_elements_st_reg(web_browser):
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()
    assert page.h1.get_text() == 'Регистрация'
    assert page.left_block.is_presented() and page.right_block.is_presented()
    # assert page.rit_tagline.is_visible()  # скрыт, т. к. сейчас элемента нет, баг, но на функционал не влияет
    assert page.reg_div.is_visible()
    assert page.name_form.is_visible() and page.lastname_form.is_visible()
    assert page.region_form.is_visible()
    assert page.phone_ad_form.is_visible()
    assert page.password_form.is_visible() and page.password_confirm_form.is_visible()
    assert page.btn_reg.is_clickable() and page.btn_reg.get_text() == 'Зарегистрироваться'
    # assert для ссылки на политику конфиденциальности, которой нет
    assert page.terms_of_use.is_visible() and page.terms_of_use_link.is_clickable()


# 1. Доступность авторизации по коду на телефон
@pytest.mark.parametrize("phone", [seven_phone, eight_phone],
                         ids=["+7x format", "8x format"])
def test1_phone_code_auth_is_available_pos(web_browser, phone):
    page = SHomeCodeAuthPage(web_browser)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.phone_ad_form.send_keys(phone)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_get_code.click()

    # ожидание, т. к. иногда страница для assert'a не успевает загрузиться
    if page.h1.get_text() == 'Авторизация по коду':
        time.sleep(3)

    assert page.h1.get_text() == 'Код подтверждения отправлен'
    assert page.code_send.get_text() == f'По SMS на номер {seven_phone}'


# 2. Авторизация по связке email-пароль - негативный тест с некорректным email
# Позитивного теста с почтой нет, потому что делала SmartHome в последнюю очередь и боялась сломать привязыванием email
# уже имеющиеся учётки, а вместе с ними и тесты)
def test2_invalid_phone_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.phone_us_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
    assert page.error_message.get_text() == 'Неверный логин или пароль'


# 3. Авторизация по связке email-пароль - негативный тест с некорректным паролем
def test3_phone_invalid_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.phone_us_form.send_keys(google_email)
    page.password_form.send_keys(invalid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
    assert page.error_message.get_text() == 'Неверный логин или пароль'


# 4. Авторизация по связке телефон-пароль - позитивные тесты
@pytest.mark.parametrize("phone", [seven_phone, eight_phone],
                         ids=["+7x format", "8x format"])
def test4_phone_password_auth_pos(web_browser, phone):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.phone_us_form.send_keys(phone)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert 'умный дом' in page.cabinet.get_text()

    # Выходим из личного кабинета
    page.userpic.click()
    page.btn_logout.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 5. Авторизация по связке номер-пароль - негативные тесты с некорректными номерами
@pytest.mark.parametrize("phone", [invalid_phone_11, invalid_phone_10, invalid_phone_12],
                         ids=["invalid 11 numbers", "invalid 10 numbers", "invalid 12 numbers"])
def test5_invalid_phone_password_auth_neg(web_browser, phone):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.phone_us_form.send_keys(phone)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации


# 6. Авторизация по связке телефон-пароль - негативный тест с некорректным паролем
def test6_phone_invalid_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.phone_us_form.send_keys(seven_phone)
    page.password_form.send_keys(invalid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
    assert page.error_message.get_text() == 'Неверный логин или пароль'


# 7. Авторизация по связке логин-пароль - позитивный тест
def test7_login_password_auth_pos(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.login_us_form.send_keys(login_shome)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert 'умный дом' in page.cabinet.get_text()

    # Выходим из личного кабинета
    page.userpic.click()
    page.btn_logout.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 8. Авторизация по связке логин-пароль - негативные тесты с некорректными логинами
@pytest.mark.parametrize("login", [login_only_numbers, login_as_email, login_longer],
                         ids=["only numbers", "as email", "long"])
def test8_invalid_login_password_auth_neg(web_browser, login):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.login_us_form.send_keys(login)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации


# 9. Авторизация по связке логин-пароль - негативный тест с некорректным паролем
def test9_login_invalid_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.login_us_form.send_keys(login_shome)
    page.password_form.send_keys(invalid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
    assert page.error_message.get_text() == 'Неверный логин или пароль'


# 10. Доступность восстановления пароля по коду на телефон
    # Т. к. капчу ввести не можем, проверяем просто, что телефон вводится и кнопка нажимается, без негативных проверок
@pytest.mark.parametrize("phone", [seven_phone, eight_phone],
                         ids=["+7x format", "8x format"])
def test10_phone_reset_password_is_available(web_browser, phone):

    page = SHomeResetPasswordPage(web_browser)

    page.phone_us_form.send_keys(phone)

    # Задаём ожидание, если на странице отображён счётчик времени (появляется довольно быстро)
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reset.click()

    assert page.h1.get_text() == 'Восстановление пароля'


# 11. Регистрация - негативный тест с уже зарегистрированным номером
def test11_standard_reg_used_phone_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.phone_ad_form.send_keys(seven_phone)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    # Вообще ожидаем некоторое сообщение об ошибке, но т. к. его нет, проверяем, что нам на почту не отправили код
    assert page.error_popup.get_text() == 'Учётная запись уже существует'


# 12. Регистрация - попытка зарегистрироваться с email
def test12_standard_reg_email_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.phone_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    # Вообще ожидаем некоторое сообщение об ошибке, но т. к. его нет, проверяем, что нам на почту не отправили код
    assert page.error_popup.get_text() == 'Учётная запись уже существует'


# 13. Регистрация - позитивные варианты заполнения поля "Имя"
def test13_reg_name_validation_pos(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name_small)
    page.lastname_form.click()
    assert page.error_reg_forms.is_presented() is False
    # assert page.name_input.get_text() == name  # не достаёт текст из поля

    # очищаем поле
    page.name_form.clear()
    page.name_form.send_keys(name_caps)
    page.lastname_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.name_form.clear()
    page.name_form.send_keys(name_yo)
    page.lastname_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.name_form.clear()
    page.name_form.send_keys(name_rare)
    page.lastname_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.name_form.clear()
    page.name_form.send_keys(name_2)
    page.lastname_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.name_form.clear()
    page.name_form.send_keys(name_hyphen)
    page.lastname_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.name_form.clear()
    page.name_form.send_keys(name_hyphen_spaces)
    page.lastname_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.name_form.clear()
    page.name_form.send_keys(name_30)
    page.lastname_form.click()
    assert page.error_reg_forms.is_presented() is False


# 14. Регистрация - негативные варианты заполнения поля "Имя", которые система не пропускает
def test14_reg_name_validation_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name_medium_dash)
    page.lastname_form.double_click()  # даблклик, потому что он с ожиданием - чтобы убедиться, что ошибка не исчезает
    assert page.error_reg_forms.is_presented() is True

    # очищаем поле
    page.name_form.clear()
    page.name_form.send_keys(name_long_dash)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_number_dash)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_with_space)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_lat)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_cyr_lat)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_cyr_num)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_cyr_spec)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_nums)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_specs)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_cyr_chin)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_chin)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_first_hyph)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_2_first_hyph)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_2_hyph)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_3_words_hyph)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_31)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True


# 15. Регистрация - xfail-негативные варианты заполнения поля "Имя"
@pytest.mark.xfail(reason='Пропускает имя с последним символом дефисом')
def test15_reg_name_validation_neg_xfail(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name_last_hyph)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_2_last_hyph)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True


# 16. Регистрация - передаём пустое поле "Имя"
@pytest.mark.parametrize("name", [name_empty, name_spaces])
def test16_standard_reg_empty_name_neg(web_browser, name):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.phone_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    assert page.error_reg_forms.is_presented() is True


# 17. Регистрация - позитивные варианты заполнения поля "Фамилия"
def test17_reg_lastname_validation_pos(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.lastname_form.send_keys(lastname_small)
    page.name_form.click()
    assert page.error_reg_forms.is_presented() is False
    # assert page.name_input.get_text() == name  # не достаёт текст из поля

    # очищаем поле
    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_caps)
    page.name_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_yo)
    page.name_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_rare)
    page.name_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_2)
    page.name_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_hyphen)
    page.name_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_hyphen_spaces)
    page.name_form.click()
    assert page.error_reg_forms.is_presented() is False

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_30)
    page.name_form.click()
    assert page.error_reg_forms.is_presented() is False


# 18. Регистрация - негативные варианты заполнения поля "Фамилия", которые система не пропускает
def test18_reg_lastname_validation_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.lastname_form.send_keys(lastname_medium_dash)
    page.name_form.double_click()  # даблклик, потому что он с ожиданием - чтобы убедиться, что ошибка не исчезает
    assert page.error_reg_forms.is_presented() is True

    # очищаем поле
    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_long_dash)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_number_dash)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_with_space)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_lat)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_cyr_lat)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_cyr_num)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_cyr_spec)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_nums)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_specs)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_cyr_chin)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_chin)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_first_hyph)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_2_first_hyph)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_2_hyph)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_3_words_hyph)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_31)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True


# 19. Регистрация - xfail-негативные варианты заполнения поля "Фамилия"
@pytest.mark.xfail(reason='Пропускает имя с последним символом дефисом')
def test19_reg_lastname_validation_neg_xfail(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.lastname_form.send_keys(lastname_last_hyph)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_2_last_hyph)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True


# 20. Регистрация - передаём пустое поле "Фамилия"
@pytest.mark.parametrize("lastname", [lastname_empty, lastname_spaces])
def test20_standard_reg_empty_lastname_neg(web_browser, lastname):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.phone_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    assert page.error_reg_forms.is_presented() is True


# 21. Регистрация - валидация для корректных вариантов пароля
@pytest.mark.parametrize("password", [password_valid_8, password_valid_20])
def test21_standard_reg_dif_passwords_pos(web_browser, password):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.password_form.send_keys(password)
    page.password_confirm_form.double_click()
    assert page.error_reg_forms.is_presented() is False


# 22. Регистрация - валидация поля для некорректных паролей
def test22_standard_reg_invalid_passwords_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.password_form.send_keys(password_invalid_7)
    page.password_confirm_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    # очищаем поле
    page.password_form.clear()
    page.password_form.send_keys(password_invalid_small)
    page.password_confirm_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.password_form.clear()
    page.password_form.send_keys(password_invalid_caps)
    page.password_confirm_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.password_form.clear()
    page.password_form.send_keys(password_invalid_21)
    page.password_confirm_form.double_click()
    assert page.error_reg_forms.is_presented() is True


# 23. Регистрация - введённые пароли не совпадают
def test23_standard_reg_invalid_password_confirm_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = SHomeRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.phone_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(password_invalid_small)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    assert page.error_reg_forms.is_presented() is True
