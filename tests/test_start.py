import pytest
import time
from pages.start_pages import *
from params import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Это своего рода базовые тесты - с них начинала, т. к. Старт Web предусматривает все доступные сценарии.
# Тесты для других продуктов брала отсюда и немного подстраивала под требования / условия.

# 0. Проверка наличия элементов на страницах и их локаторов.
# Делаю такой мега-тест с кучей ассертов, хотя можно разбить на отдельные - но мы тут заполняем формы и
# тыкаем на кнопки. Если один ассерт не пройдёт, тест сразу упадёт, но можно по цепочке разбирать постепенно))0)


# 0.1. Для страницы авторизации по коду
def test01_elements_code_auth(web_browser):
    page = StartCodeAuthPage(web_browser)
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
    page = StartPasswordAuthPage(web_browser)
    page.btn_standard_auth.click()
    assert page.h1.get_text() == 'Авторизация'
    assert page.left_block.is_presented() and page.right_block.is_presented()
    assert page.rit_tagline.is_presented()
    assert page.login_div.is_visible()
    assert page.tab_phone.is_clickable() and page.tab_phone.get_text() == 'Телефон'
    assert page.tab_email.is_clickable() and page.tab_email.get_text() == 'Почта'
    assert page.tab_login.is_clickable() and page.tab_login.get_text() == 'Логин'
    assert page.tab_ls.is_clickable() and page.tab_ls.get_text() == 'Лицевой счёт'
    assert page.login_us_form.is_visible() and page.password_form.is_visible()
    assert page.btn_login.is_clickable() and page.btn_login.get_text() == 'Войти'
    assert page.btn_back_code.is_clickable() and page.btn_back_code.get_text() == 'Войти по временному коду'
    assert page.btn_forgot_password.is_clickable() and page.btn_forgot_password.get_text() == 'Забыл пароль'
    assert page.btn_to_reg.is_clickable() and page.btn_to_reg.get_text() == 'Зарегистрироваться'


# 0.3. Для восстановления пароля
def test03_elements_reset_password(web_browser):
    page = StartResetPasswordPage(web_browser)
    assert page.h1.get_text() == 'Восстановление пароля'
    assert page.tab_phone.is_clickable() and page.tab_phone.get_text() == 'Телефон'
    assert page.tab_email.is_clickable() and page.tab_email.get_text() == 'Почта'
    assert page.tab_login.is_clickable() and page.tab_login.get_text() == 'Логин'
    assert page.tab_ls.is_clickable() and page.tab_ls.get_text() == 'Лицевой счёт'
    assert page.email_us_form.is_visible()
    assert page.captcha_form.is_visible() and page.captcha_image.is_visible()
    assert page.btn_reset.is_clickable() and page.btn_reset.get_text() == 'Продолжить'
    assert page.btn_reset_back.is_clickable() and 'Вернуться' in page.btn_reset_back.get_text()


# 0.4. Для страницы регистрации
def test04_elements_st_reg(web_browser):
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()
    assert page.h1.get_text() == 'Регистрация'
    assert page.left_block.is_presented() and page.right_block.is_presented()
    # assert page.rit_tagline.is_visible()  # скрыт, т. к. сейчас элемента нет, баг, но на функционал не влияет
    assert page.reg_div.is_visible()
    assert page.name_form.is_visible() and page.lastname_form.is_visible()
    assert page.region_form.is_visible()
    assert page.email_ad_form.is_visible()
    assert page.password_form.is_visible() and page.password_confirm_form.is_visible()
    assert page.btn_reg.is_clickable() and page.btn_reg.get_text() == 'Зарегистрироваться'
    # assert для ссылки на политику конфиденциальности, которой нет
    assert page.terms_of_use.is_visible() and page.terms_of_use_link.is_clickable()


# 1. Доступность авторизации по коду на email - позитивные тесты для популярных почтовых сервисов.
    # Mail.ru в отдельном тесте с полным сценарием авторизации.
@pytest.mark.parametrize("email", [google_email, yandex_email],
                         ids=["gmail", "yandex"])
def test1_email_code_auth_is_available_pos(web_browser, email):

    page = StartCodeAuthPage(web_browser)

    # Проверяем, нет ли на странице капчи, которую мы не сможем пройти (появляется после кучи прогонов)
    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(email)

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
    page = StartCodeAuthPage(web_browser)

    # Проверяем, нет ли на странице капчи, которую мы не сможем пройти (появляется после кучи прогонов)
    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(mailru_email)

    # Задаём ожидание, если на странице отображён счётчик времени (появляется довольно быстро)
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_get_code.click()
    time.sleep(15)  # очень долгое ожидание, чтобы пришло письмо
    page.code_forms.send_keys(code_from_email())

    assert page.cabinet.get_text() == 'Личный кабинет'

    # Выходим из личного кабинета
    page.userpic.click()
    page.btn_logout.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))  # ожидание логаута - сначала тесты работали
    # без него, а через несколько дней перестали - я глазами видела, что кнопка кликается, а на следующем тесте
    # открывается ЛК, а не форма авторизации. Это доставило мне много боли, но самое очевидное решение оказалось самым
    # подходящим. Был ещё вариант сделать логаут фикстурой в начале каждого теста (там через условие оформлять), но
    # это дело настроить не получилось, а ожидания стабильны и надёжны :) Если ставить секунд 10 - может не хватить.


# 3. Доступность авторизации по коду на телефон
@pytest.mark.parametrize("phone", [seven_phone, eight_phone],
                         ids=["+7x format", "8x format"])
def test3_phone_code_auth_is_available_pos(web_browser, phone):
    page = StartCodeAuthPage(web_browser)

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


# 4. Доступность авторегистрации по коду на email - позитивные тесты для популярных почтовых сервисов.
    # Mail.ru - отдельным тестом с полным сценарием
@pytest.mark.parametrize("email", [gmail_random, yandex_random],
                         ids=["gmail", "yandex"])
@pytest.mark.xfail(reason='Может сгенерироваться уже зарегистрированный email (маловероятно, но факт)')
def test4_autoreg_email_code_is_available_pos(web_browser, email):
    page = StartCodeAuthPage(web_browser)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(email)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_get_code.click()

    # ожидание, т. к. иногда страница для assert'a не успевает загрузиться
    if page.h1.get_text() == 'Авторизация по коду':
        time.sleep(3)

    assert page.h1.get_text() == 'Код подтверждения отправлен'
    assert page.code_send.get_text() == f'На почту {email}'


# 5. Авторегистрация по коду на email - полный сценарий через mail.ru
@pytest.mark.xfail(reason='Код может не прийти или прийти с большой задержкой, если было много прогонов')
def test5_email_code_autoreg_pos(web_browser):

    page = StartCodeAuthPage(web_browser)

    # Проверяем, нет ли на странице капчи, которую мы не сможем пройти (появляется после кучи прогонов)
    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(mailru_random)

    # Задаём ожидание, если на странице отображён счётчик времени (появляется довольно быстро)
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_get_code.click()
    time.sleep(15)  # очень долгое ожидание, чтобы пришло письмо
    page.code_forms.send_keys(code_from_email())

    assert page.cabinet.get_text() == 'Личный кабинет'

    # Выходим из личного кабинета
    page.userpic.click()
    page.btn_logout.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 6. Негативные проверки для авторегистрации по коду на email
@pytest.mark.parametrize("email", [email_fake_domain, email_error_domain, email_50, email_255, email_256, email_1000])
@pytest.mark.xfail(reason='В данный момент код отправляется на любой email')
def test6_autoreg_email_code_is_available_neg(web_browser, email):

    page = StartCodeAuthPage(web_browser)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(email)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_get_code.click()
    # ожидание, т. к. иногда страница для assert'a не успевает загрузиться
    if page.h1.get_text() == 'Авторизация по коду':
        time.sleep(3)

    assert page.h1.get_text() != 'Код подтверждения отправлен'


# 7. Авторизация по связке email-пароль - позитивные тесты для популярных почтовых сервисов
@pytest.mark.parametrize("email", [google_email, mailru_email, yandex_email],
                         ids=["gmail", "mailru", "yandex"])
def test7_email_password_auth_pos(web_browser, email):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartPasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.email_us_form.send_keys(email)
    page.password_form.send_keys(valid_password)

    # Проверка на капчу опустилась ниже, потому что иногда срабатывает до того, как загрузится нужная страница
    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.cabinet.get_text() == 'Личный кабинет'
    assert page.user_name.get_text() == 'Иван'  # Проверяем, что h2 соответствует имени пользователя в личном кабинете

    # Выходим из личного кабинета
    page.userpic.click()
    page.btn_logout.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 8. Авторизация по связке email-пароль - негативный тест с некорректным email
def test8_invalid_email_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartPasswordAuthPage(web_browser)
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


# 9. Авторизация по связке email-пароль - негативный тест с некорректным паролем
def test9_email_invalid_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartPasswordAuthPage(web_browser)
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


# 10. Авторизация по связке телефон-пароль - позитивные тесты
@pytest.mark.parametrize("phone", [seven_phone, eight_phone],
                         ids=["+7x format", "8x format"])
def test10_phone_password_auth_pos(web_browser, phone):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartPasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.phone_us_form.send_keys(phone)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.cabinet.get_text() == 'Личный кабинет'
    assert page.user_name.get_text() == 'Анастасия'  # Проверяем, что h2 соответствует имени пользователя в ЛК

    # Выходим из личного кабинета
    page.userpic.click()
    page.btn_logout.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 11. Авторизация по связке номер-пароль - негативные тесты с некорректными номерами
@pytest.mark.parametrize("phone", [invalid_phone_11, invalid_phone_10, invalid_phone_12],
                         ids=["invalid 11 numbers", "invalid 10 numbers", "invalid 12 numbers"])
def test11_invalid_phone_password_auth_neg(web_browser, phone):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartPasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.phone_us_form.send_keys(phone)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации


# 12. Авторизация по связке телефон-пароль - негативный тест с некорректным паролем
def test12_phone_invalid_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartPasswordAuthPage(web_browser)
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


# 13. Авторизация по связке логин-пароль - позитивный тест
def test13_login_password_auth_pos(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartPasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.login_us_form.send_keys(login_valid)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.cabinet.get_text() == 'Личный кабинет'
    assert page.user_name.get_text() == 'Иван'  # Проверяем, что h2 соответствует имени пользователя в ЛК

    # Выходим из личного кабинета
    page.userpic.click()
    page.btn_logout.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 14. Авторизация по связке логин-пароль - негативные тесты с некорректными логинами
@pytest.mark.parametrize("login", [login_only_numbers, login_as_email, login_longer],
                         ids=["only numbers", "as email", "long"])
def test14_invalid_login_password_auth_neg(web_browser, login):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartPasswordAuthPage(web_browser)
    page.btn_standard_auth.click()

    page.login_us_form.send_keys(login)
    page.password_form.send_keys(valid_password)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_login.click()

    assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации


# 15. Авторизация по связке логин-пароль - негативный тест с некорректным паролем
def test15_login_invalid_password_auth_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartPasswordAuthPage(web_browser)
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


# 16. Доступность восстановления пароля по коду на email
    # Т. к. капчу ввести не можем, проверяем просто, что почта вводится и кнопка нажимается
    # Тест по большому счёту бессмысленный, то если вдруг отключат капчу, его можно было бы быстро допилить до рабочего
    # состояния
@pytest.mark.parametrize("email", [google_email, mailru_email, yandex_email],
                         ids=["gmail", "mailru", "yandex"])
def test16_email_reset_password_is_available(web_browser, email):

    page = StartResetPasswordPage(web_browser)

    page.email_us_form.send_keys(email)

    # Задаём ожидание, если на странице отображён счётчик времени (появляется довольно быстро)
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reset.click()

    assert page.h1.get_text() == 'Восстановление пароля'
    assert page.error_message.get_text() == 'Неверный логин или текст с картинки'


# 17. Доступность восстановления пароля по коду на телефон
    # Т. к. капчу ввести не можем, проверяем просто, что телефон вводится и кнопка нажимается, без негативных проверок
@pytest.mark.parametrize("phone", [seven_phone, eight_phone],
                         ids=["+7x format", "8x format"])
def test17_phone_reset_password_is_available(web_browser, phone):

    page = StartResetPasswordPage(web_browser)

    page.phone_us_form.send_keys(phone)

    # Задаём ожидание, если на странице отображён счётчик времени (появляется довольно быстро)
    if page.code_timeout.is_visible():
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reset.click()

    assert page.h1.get_text() == 'Восстановление пароля'


# 18. Регистрация - позитивные тесты для популярных почтовых сервисов. Mail.ru отдельно с полным сценарием
@pytest.mark.parametrize("email", [gmail_random, yandex_random],
                         ids=["gmail", "yandex"])
@pytest.mark.xfail(reason='Может сгенерироваться уже зарегистрированный email (маловероятно, но факт)')
def test18_standard_reg_dif_emails_pos(web_browser, email):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(email)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    assert page.h1.get_text() == 'Подтверждение email'
    assert page.reg_code_send.get_text() == f'Kод подтверждения отправлен на адрес {email}'


# 19. Регистрация - негативный тест с уже зарегистрированным email
def test19_standard_reg_used_email_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(google_email)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    # Вообще ожидаем некоторое сообщение об ошибке, но т. к. его нет, проверяем, что нам на почту не отправили код
    assert page.error_popup.get_text() == 'Учётная запись уже существует'


# 20. Регистрация - полный сценарий через mail.ru
@pytest.mark.xfail(reason='Код может не прийти или прийти с большой задержкой, если было много прогонов')
def test20_standard_reg_mailru_pos(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(mailru_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    time.sleep(15)  # очень долгое ожидание, чтобы пришло письмо
    page.code_forms.send_keys(code_from_email())

    assert page.cabinet.get_text() == 'Личный кабинет'

    # Выходим из личного кабинета
    page.userpic.click()
    page.btn_logout.click()
    WebDriverWait(web_browser, 30).until(EC.title_is('Ростелеком ID'))


# 21. Регистрация - негативные тесты для некорректных email
@pytest.mark.parametrize("email", [email_fake_domain, email_error_domain, email_50, email_255, email_256, email_1000])
@pytest.mark.xfail(reason='В данный момент код отправляется на любой email')
def test21_standard_reg_dif_emails_neg(web_browser, email):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(email)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    assert page.h1.get_text() != 'Подтверждение email'


# 22. Регистрация - позитивные варианты заполнения поля "Имя"
    # Здесь хотела проверить ещё и то, что при неправильном вводе имена адаптируются под маску. Но введённый текст лежит
    # в двух span'ах, и мне удалось нагуглить только, как достать его через BeautifulSoup, но тогда вроде как нужно
    # парсить страницу через api-запрос. Пусть будет просто проверка того, что система не выдаёт сообщение об ошибке =
    # принимает введённый текст (без проверки того, как этот текст отображается).
    # Все проверки внутри теста, а не через параметризацию, чтобы каждый раз заново не открывать страницу - это долго
def test22_reg_name_validation_pos(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
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


# 23. Регистрация - негативные варианты заполнения поля "Имя", которые система не пропускает
def test23_reg_name_validation_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
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


# 24. Регистрация - xfail-негативные варианты заполнения поля "Имя"
@pytest.mark.xfail(reason='Пропускает имя с последним символом дефисом')
def test24_reg_name_validation_neg_xfail(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name_last_hyph)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.name_form.clear()
    page.name_form.send_keys(name_2_last_hyph)
    page.lastname_form.double_click()
    assert page.error_reg_forms.is_presented() is True


# 25. Регистрация - передаём пустое поле "Имя"
@pytest.mark.parametrize("name", [name_empty, name_spaces])
def test25_standard_reg_empty_name_neg(web_browser, name):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    assert page.error_reg_forms.is_presented() is True


# 26. Регистрация - позитивные варианты заполнения поля "Фамилия"
def test26_reg_lastname_validation_pos(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
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


# 27. Регистрация - негативные варианты заполнения поля "Фамилия", которые система не пропускает
def test27_reg_lastname_validation_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
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


# 28. Регистрация - xfail-негативные варианты заполнения поля "Фамилия"
@pytest.mark.xfail(reason='Пропускает имя с последним символом дефисом')
def test28_reg_lastname_validation_neg_xfail(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.lastname_form.send_keys(lastname_last_hyph)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True

    page.lastname_form.clear()
    page.lastname_form.send_keys(lastname_2_last_hyph)
    page.name_form.double_click()
    assert page.error_reg_forms.is_presented() is True


# 29. Регистрация - передаём пустое поле "Фамилия"
@pytest.mark.parametrize("lastname", [lastname_empty, lastname_spaces])
def test29_standard_reg_empty_lastname_neg(web_browser, lastname):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(valid_password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    assert page.error_reg_forms.is_presented() is True


# 30. Регистрация - тесты для корректных вариантов пароля
@pytest.mark.parametrize("password", [password_valid_8, password_valid_20])
def test30_standard_reg_dif_passwords_pos(web_browser, password):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(password)
    page.password_confirm_form.send_keys(password)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    assert page.h1.get_text() == 'Подтверждение email'
    assert page.reg_code_send.get_text() == f'Kод подтверждения отправлен на адрес {gmail_random}'


# 31. Регистрация - валидация поля для некорректных паролей
def test31_standard_reg_invalid_passwords_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
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


# 32. Регистрация - введённые пароли не совпадают
def test32_standard_reg_invalid_password_confirm_neg(web_browser):

    # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
    page = StartRegPage(web_browser)
    page.btn_standard_auth.click()
    page.btn_to_reg.click()

    page.name_form.send_keys(name)
    page.lastname_form.send_keys(lastname)

    if page.captcha_form.is_presented():
        pytest.skip("There is CAPTCHA, but I'm a robot")

    page.email_ad_form.send_keys(gmail_random)
    page.password_form.send_keys(valid_password)
    page.password_confirm_form.send_keys(password_invalid_small)

    if page.code_timeout.is_visible():  # Задаём ожидание, если на странице отображён счётчик времени
        time.sleep(int(page.code_timeout.get_text().split()[4]))

    page.btn_reg.click()

    assert page.error_reg_forms.is_presented() is True
