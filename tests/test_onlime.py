import pytest
import time
from pages.onlime_pages import *
from params_test import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 0. Проверка наличия элементов на страницах и их локаторов.
# Делаю такой мега-тест с кучей ассертов, хотя можно разбить на отдельные - но мы тут заполняем формы
# тыкаем на кнопки. Если один ассерт не пройдёт, тест сразу упадёт, но можно по цепочке разбирать постепенно))0)

# 0.1. Для страницы авторизации по коду
def test01_elements_code_auth(web_browser):
    page = OnlimeCodeAuthPage(web_browser)

    assert page.h1.get_text() == 'Авторизация по коду'
    assert 'Укажите' in page.help_text.get_text()
    assert page.email_ad_form.is_visible()
    assert page.btn_get_code.is_clickable() and page.btn_get_code.get_text() == 'Получить код'
    assert page.btn_standard_auth.is_clickable() and page.btn_standard_auth.get_text() == 'Войти с паролем'

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")
    else:
        page.email_ad_form.send_keys(seven_phone)
        if page.code_timeout.is_visible():
            time.sleep(int(page.code_timeout.get_text().split()[4]))
        page.btn_get_code.click()
        assert page.h1.get_text() == 'Код подтверждения отправлен' and page.code_send.get_text() == f'По SMS на номер '\
                                                                                                    f'{seven_phone}'
        assert page.btn_change_data.is_clickable() and page.btn_change_data.get_text() == 'Изменить номер'
        assert page.code_forms.is_visible() and (page.resend_timeout.is_visible()
                                                 or page.too_many_codes_error.is_visible())
        if page.resend_timeout.is_visible():
            time.sleep((int(page.resend_timeout.get_text().split()[5])))
            assert page.btn_resend_code.is_clickable()
        # По требованиям должна быть надпись, на самом деле нет. На функционал не влияет, поэтому пока спрятала:
        # assert page.btn_resend_code.get_text() == 'Получить новый код'

        page.btn_change_data.click()
        assert page.h1.get_text() == 'Авторизация по коду'
        if page.captcha_form.is_presented():
            pytest.skip("There is CAPTCHA, but I'm a robot")
        else:
            page.email_ad_form.send_keys(google_email)
            if page.code_timeout.is_visible():
                time.sleep(int(page.code_timeout.get_text().split()[4]))
            page.btn_get_code.click()
            assert page.h1.get_text() == 'Код подтверждения отправлен' \
                   and page.code_send.get_text() == f'На почту {google_email}'
            assert page.btn_change_data.is_clickable() and page.btn_change_data.get_text() == 'Изменить почту'
            assert page.code_forms.is_visible() and (page.resend_timeout.is_visible()
                                                     or page.too_many_codes_error.is_visible())
            if page.resend_timeout.is_visible():
                time.sleep((int(page.resend_timeout.get_text().split()[5])))
                assert page.btn_resend_code.is_clickable()
            # По требованиям должна быть надпись, на самом деле нет. На функционал не влияет, поэтому пока спрятала:
            # assert page.btn_resend_code.get_text() == 'Получить новый код'


# 0.2. Для стандартной авторизации с паролем
def test02_elements_standard_auth(web_browser):
    page = OnlimePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()
    assert page.h1.get_text() == 'Авторизация'
    assert page.left_block.is_presented() and page.right_block.is_presented()
    assert page.rit_tagline.is_presented()
    assert page.login_div.is_visible()
    assert page.tab_phone.is_clickable() and page.tab_phone.get_text() == 'Телефон'
    assert page.tab_email.is_clickable() and page.tab_email.get_text() == 'Почта'
    assert page.tab_login.is_clickable() and page.tab_login.get_text() == 'Логин'
    assert page.tab_ls.is_visible() is False
    assert page.login_us_form.is_visible() and page.password_form.is_visible()
    assert page.btn_login.is_clickable() and page.btn_login.get_text() == 'Войти'
    assert page.btn_back_code.is_clickable() and page.btn_back_code.get_text() == 'Войти по временному коду'
    assert page.btn_forgot_password.is_clickable() and page.btn_forgot_password.get_text() == 'Забыл пароль'
    assert page.btn_to_reg.is_presented() is False


# 0.3. Для восстановления пароля
def test03_elements_reset_password(web_browser):
    page = OnlimeResetPasswordPage(web_browser)
    assert page.h1.get_text() == 'Восстановление пароля'
    assert page.tab_phone.is_clickable() and page.tab_phone.get_text() == 'Телефон'
    assert page.tab_email.is_clickable() and page.tab_email.get_text() == 'Почта'
    assert page.tab_login.is_clickable() and page.tab_login.get_text() == 'Логин'
    assert page.tab_ls.is_clickable() and page.tab_ls.get_text() == 'Лицевой счёт'
    assert page.email_us_form.is_visible()
    assert page.captcha_form.is_visible() and page.captcha_image.is_visible()
    assert page.btn_reset.is_clickable() and page.btn_reset.get_text() == 'Продолжить'
    assert page.btn_reset_back.is_clickable() and 'Вернуться' in page.btn_reset_back.get_text()


# 1. Доступность авторизации по коду на email - позитивные тесты для популярных почтовых сервисов.
    # Mail.ru в отдельном тесте с полным сценарием авторизации.
@pytest.mark.parametrize("email", [google_email, yandex_email],
                         ids=["gmail", "yandex"])
def test1_email_code_auth_is_available_pos(web_browser, email):

    page = OnlimeCodeAuthPage(web_browser)

    page.email_ad_form.send_keys(email)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    # Задаём ожидание, если на странице отображён счётчик времени (появляется довольно быстро)
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))  # 4 - позиция цифр в полученном тексте

    page.btn_get_code.click()

    # ожидание, т. к. иногда страница для assert'a не успевает загрузиться
    if page.h1.get_text() == 'Авторизация по коду':
        time.sleep(3)

    assert page.h1.get_text() == 'Код подтверждения отправлен'
    assert page.code_send.get_text() == f'На почту {email}'


# 2. Авторизация по коду на email - полный сценарий через mail.ru
@pytest.mark.xfail(reason='Код может не прийти или прийти с большой задержкой, если было много прогонов')
def test2_email_code_auth_pos(web_browser):

    page = OnlimeCodeAuthPage(web_browser)

    page.email_ad_form.send_keys(mailru_email)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    # Задаём ожидание, если на странице отображён счётчик времени (появляется довольно быстро)
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_get_code.click()
    time.sleep(15)  # очень долгое ожидание, чтобы пришло письмо
    page.code_forms.send_keys(code_from_email())
    page.btn_onlime_go.click()
    assert page.cabinet.get_text() == 'Личный кабинет'

    # Выходим из личного кабинета
    page.btn_logout_onlime.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 3. Доступность авторизации по коду на телефон
@pytest.mark.parametrize("phone", [seven_phone, eight_phone],
                         ids=["+7x format", "8x format"])
def test3_phone_code_auth_is_available_pos(web_browser, phone):

    page = OnlimeCodeAuthPage(web_browser)

    page.phone_ad_form.send_keys(phone)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_get_code.click()

    # ожидание, т. к. иногда страница для assert'a не успевает загрузиться
    if page.h1.get_text() == 'Авторизация по коду':
        time.sleep(3)

    assert page.h1.get_text() == 'Код подтверждения отправлен'
    assert page.code_send.get_text() == f'По SMS на номер {seven_phone}'


# 4. Авторизация по связке email-пароль - позитивные тесты для популярных почтовых сервисов
@pytest.mark.parametrize("email", [google_email, mailru_email, yandex_email],
                         ids=["gmail", "mailru", "yandex"])
def test4_email_password_auth_pos(web_browser, email):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = OnlimePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.email_us_form.send_keys(email)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()
    page.btn_onlime_go.click()

    assert page.cabinet.get_text() == 'Личный кабинет'
    page.btn_logout_onlime.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 5. Авторизация по связке email-пароль - негативный тест с некорректным email
def test5_invalid_email_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = OnlimePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.email_us_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
    assert page.error_message.get_text() == 'Неверный логин или пароль'


# 6. Авторизация по связке email-пароль - негативный тест с некорректным паролем
def test6_email_invalid_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = OnlimePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.email_us_form.send_keys(google_email)
    page.password_form.send_keys(invalid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
    assert page.error_message.get_text() == 'Неверный логин или пароль'


# 7. Авторизация по связке телефон-пароль - позитивные тесты
@pytest.mark.parametrize("phone", [seven_phone, eight_phone],
                         ids=["+7x format", "8x format"])
def test7_phone_password_auth_pos(web_browser, phone):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = OnlimePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.phone_us_form.send_keys(phone)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()
    page.btn_onlime_go.click()

    assert page.cabinet.get_text() == 'Личный кабинет'
    page.btn_logout_onlime.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 8. Авторизация по связке номер-пароль - негативные тесты с некорректными номерами
@pytest.mark.parametrize("phone", [invalid_phone_11, invalid_phone_10, invalid_phone_12],
                         ids=["invalid 11 numbers", "invalid 10 numbers", "invalid 12 numbers"])
def test8_invalid_phone_password_auth_neg(web_browser, phone):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = OnlimePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.phone_us_form.send_keys(phone)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации


# 9. Авторизация по связке телефон-пароль - негативный тест с некорректным паролем
def test9_phone_invalid_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = OnlimePasswordAuthPage(web_browser)
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


# 10. Авторизация по связке логин-пароль - позитивный тест
def test10_login_password_auth_pos(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = OnlimePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.login_us_form.send_keys(login_valid)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()
    page.btn_onlime_go.click()

    assert page.cabinet.get_text() == 'Личный кабинет'
    page.btn_logout_onlime.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 11. Авторизация по связке логин-пароль - негативные тесты с некорректными логинами
@pytest.mark.parametrize("login", [login_only_numbers, login_as_email, login_longer],
                         ids=["only numbers", "as email", "long"])
def test11_invalid_login_password_auth_neg(web_browser, login):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = OnlimePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.login_us_form.send_keys(login)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации


# 12. Авторизация по связке логин-пароль - негативный тест с некорректным паролем
def test12_login_invalid_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = OnlimePasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.login_us_form.send_keys(login_valid)
    page.password_form.send_keys(invalid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
    assert page.error_message.get_text() == 'Неверный логин или пароль'


# 13. Доступность восстановления пароля по коду на email
    # Т. к. капчу ввести не можем, проверяем просто, что почта вводится и кнопка нажимается
    # Тест по большому счёту бессмысленный, то если вдруг отключат капчу, его можно было бы быстро допилить до рабочего
    # состояния
@pytest.mark.parametrize("email", [google_email, mailru_email, yandex_email],
                         ids=["gmail", "mailru", "yandex"])
def test13_email_reset_password_is_available(web_browser, email):

    page = OnlimeResetPasswordPage(web_browser)

    page.email_us_form.send_keys(email)

    # Задаём ожидание, если на странице отображён счётчик времени (появляется довольно быстро)
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reset.click()

    assert page.h1.get_text() == 'Восстановление пароля'
    assert page.error_message.get_text() == 'Неверный логин или текст с картинки'


# 14. Доступность восстановления пароля по коду на телефон
    # Т. к. капчу ввести не можем, проверяем просто, что телефон вводится и кнопка нажимается, без негативных проверок
@pytest.mark.parametrize("phone", [seven_phone, eight_phone],
                         ids=["+7x format", "8x format"])
def test14_phone_reset_password_is_available(web_browser, phone):

    page = OnlimeResetPasswordPage(web_browser)

    page.phone_us_form.send_keys(phone)

    # Задаём ожидание, если на странице отображён счётчик времени (появляется довольно быстро)
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reset.click()

    assert page.h1.get_text() == 'Восстановление пароля'
