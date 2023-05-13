from pages.start_pages import *
from params_test import *
from help_functions import *

# Тесты для "Старт Web" - базовые для этого проекта и лежат в основе всех остальных тестов.

# 0. Проверка наличия элементов на страницах и их локаторов.
# Внутри одного теста проверяется наличие / кликабельность всех необходимых элементов. Идея была в том, что перед
# запуском самих тестовых сценариев можно быстро проверить элементы, чтобы пофиксить локаторы, если они изменились.
# Раскладывать на отдельные тесты смысла особого не увидела, потому что сомневаюсь, что могут сломать всё и сразу :)


class TestElementsPresence:
    # 0.1. Для страницы авторизации по коду
    def test01_elements_code_auth(self, web_browser):
        page = StartCodeAuthPage(web_browser)
        assert page.h1.get_text() == 'Авторизация по коду'
        assert 'Укажите' in page.help_text.get_text()
        assert page.email_ad_form.is_visible()
        assert page.btn_get_code.is_clickable() and page.btn_get_code.get_text() == 'Получить код'
        assert page.btn_standard_auth.is_clickable() and page.btn_standard_auth.get_text() == 'Войти с паролем'
        captcha_search(page)  # Проверяем, нет ли капчи. Если есть - тест пропускается
        page.email_ad_form.send_keys(seven_phone_plus)
        code_timer_wait(page)  # Если на странице отображается таймер - ждём
        page.btn_get_code.click()
        assert page.h1.get_text() == 'Код подтверждения отправлен' and page.code_send.get_text() == f'По SMS на номер '\
                                                                                                    f'{seven_phone_plus}'
        assert page.btn_change_data.is_clickable() and page.btn_change_data.get_text() == 'Изменить номер'
        assert page.code_forms.is_visible() and (page.resend_timeout.is_visible()
                                                 or page.too_many_codes_error.is_visible())
        resend_timer_wait(page)
        assert page.btn_resend_code.is_clickable()
        # По требованиям должна быть надпись, на самом деле нет. На функционал не влияет, поэтому проверку спрятала:
        # assert page.btn_resend_code.get_text() == 'Получить новый код'

        page.btn_change_data.click()
        assert page.h1.get_text() == 'Авторизация по коду'
        captcha_search(page)
        page.email_ad_form.send_keys(google_email)
        code_timer_wait(page)
        page.btn_get_code.click()
        assert page.h1.get_text() == 'Код подтверждения отправлен' \
               and page.code_send.get_text() == f'На почту {google_email}'
        assert page.btn_change_data.is_clickable() and page.btn_change_data.get_text() == 'Изменить почту'
        assert page.code_forms.is_visible() and (page.resend_timeout.is_visible()
                                                 or page.too_many_codes_error.is_visible())
        resend_timer_wait(page)
        assert page.btn_resend_code.is_clickable()
        # По требованиям должна быть надпись, на самом деле нет. На функционал не влияет, поэтому проверку спрятала:
        # assert page.btn_resend_code.get_text() == 'Получить новый код'

    # 0.2. Для авторизации с паролем
    def test02_elements_password_auth(self, web_browser):
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
    def test03_elements_reset_password(self, web_browser):
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
    def test04_elements_st_reg(self, web_browser):
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


class TestCodeAuthReg:
    # 1. Доступность авторизации по коду на email - позитивные тесты для популярных почтовых сервисов.
    # Mail.ru в отдельном тесте с полным сценарием авторизации.
    @pytest.mark.parametrize("email", [google_email, yandex_email],
                             ids=["gmail", "yandex"])
    def test1_email_code_auth_is_available_pos(self, web_browser, email):

        page = StartCodeAuthPage(web_browser)
        captcha_search(page)
        page.email_ad_form.send_keys(email)
        code_timer_wait(page)
        page.btn_get_code.click()
        page.wait_page_loaded()

        assert page.h1.get_text() == 'Код подтверждения отправлен'
        assert page.code_send.get_text() == f'На почту {email}'

    # 2. Авторизация по коду на email - полный сценарий через mail.ru
    @pytest.mark.xfail(reason='Код может не прийти или прийти с большой задержкой, если было много прогонов')
    def test2_email_code_auth_pos(self, web_browser, logout_start):
        page = StartCodeAuthPage(web_browser)
        captcha_search(page)
        page.email_ad_form.send_keys(mailru_email)
        code_timer_wait(page)
        page.btn_get_code.click()
        time.sleep(15)  # очень долгое ожидание, чтобы письмо точно успело прийти (подбирала эмпирически)
        page.code_forms.send_keys(code_from_email())

        assert page.cabinet.get_text() == 'Личный кабинет'  # проверяем, что мы в личном кабинете
        assert page.user_name.get_text() == 'Иван'  # Проверяем, что h2 соответствует имени пользователя
        # Правильнее было бы проверить email пользователя, но это добавляло неоправданно большое количество действий
        # (не только посмотреть ящик - лишние клики появлялись и для выхода из кабинета). Поэтому решила, что
        # для учебного проекта можно не затягивать тест и оставить только проверку имени.

    # 3. Доступность авторизации по коду на телефон
    @pytest.mark.parametrize("phone", [seven_phone_plus, eight_phone, seven_phone_without_plus],
                             ids=["+7x format", "8x format", "7x format"])
    def test3_phone_code_auth_is_available_pos(self, web_browser, phone):
        page = StartCodeAuthPage(web_browser)
        captcha_search(page)
        page.phone_ad_form.send_keys(phone)
        code_timer_wait(page)
        page.btn_get_code.click()
        page.wait_page_loaded()

        assert page.h1.get_text() == 'Код подтверждения отправлен'
        assert page.code_send.get_text() == f'По SMS на номер {seven_phone_plus}'

    # 4. Доступность авторегистрации по коду на email - позитивные тесты для популярных почтовых сервисов.
        # Mail.ru - отдельным тестом с полным сценарием
    @pytest.mark.parametrize("email", [gmail_random, yandex_random],
                             ids=["gmail", "yandex"])
    @pytest.mark.xfail(reason='Может сгенерироваться уже зарегистрированный email (маловероятно, но факт)')
    def test4_autoreg_email_code_is_available_pos(self, web_browser, email):
        page = StartCodeAuthPage(web_browser)
        captcha_search(page)
        page.email_ad_form.send_keys(email)
        code_timer_wait(page)
        page.btn_get_code.click()
        page.wait_page_loaded()

        assert page.h1.get_text() == 'Код подтверждения отправлен'
        assert page.code_send.get_text() == f'На почту {email}'

    # 5. Авторегистрация по коду на email - полный сценарий через mail.ru
    @pytest.mark.xfail(reason='Код может не прийти или прийти с большой задержкой, если было много прогонов')
    def test5_email_code_autoreg_pos(self, web_browser, logout_start):

        page = StartCodeAuthPage(web_browser)
        captcha_search(page)
        page.email_ad_form.send_keys(mailru_random)
        code_timer_wait(page)
        page.btn_get_code.click()
        time.sleep(15)  # очень долгое ожидание, чтобы письмо точно успело прийти
        page.code_forms.send_keys(code_from_email())

        assert page.cabinet.get_text() == 'Личный кабинет'

    # 6. Негативные проверки для авторегистрации по коду на email
    @pytest.mark.parametrize("email", [email_fake_domain, email_error_domain, email_50, email_255, email_256, email_1000])
    @pytest.mark.xfail(reason='В данный момент код отправляется на любой email')
    def test6_autoreg_email_code_is_available_neg(self, web_browser, email):

        page = StartCodeAuthPage(web_browser)
        captcha_search(page)
        page.email_ad_form.send_keys(email)
        code_timer_wait(page)
        page.btn_get_code.click()
        page.wait_page_loaded()

        assert page.h1.get_text() != 'Код подтверждения отправлен'


class TestPassAuth:
    # 7. Авторизация по связке email-пароль - позитивные тесты для популярных почтовых сервисов
    @pytest.mark.parametrize("email", [google_email, mailru_email, yandex_email],
                             ids=["gmail", "mailru", "yandex"])
    def test7_email_password_auth_pos(self, web_browser, logout_start, email):

        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartPasswordAuthPage(web_browser)
        page.btn_standard_auth.click()

        page.email_us_form.send_keys(email)
        page.password_form.send_keys(valid_password)
        captcha_search(page)
        code_timer_wait(page)
        page.btn_login.click()

        assert page.cabinet.get_text() == 'Личный кабинет'
        assert page.user_name.get_text() == 'Иван'  # Проверяем, что h2 соответствует имени пользователя

    # 8. Авторизация по связке email-пароль - негативный тест с некорректным email
    def test8_invalid_email_password_auth_neg(self, web_browser):

        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartPasswordAuthPage(web_browser)
        page.btn_standard_auth.click()

        page.email_us_form.send_keys(gmail_random)
        page.password_form.send_keys(valid_password)
        captcha_search(page)
        code_timer_wait(page)
        page.btn_login.click()

        assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
        assert page.error_message.get_text() == 'Неверный логин или пароль'

    # 9. Авторизация по связке email-пароль - негативный тест с некорректным паролем
    def test9_email_invalid_password_auth_neg(self, web_browser):

        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartPasswordAuthPage(web_browser)
        page.btn_standard_auth.click()

        page.email_us_form.send_keys(google_email)
        page.password_form.send_keys(invalid_password)
        captcha_search(page)
        code_timer_wait(page)
        page.btn_login.click()

        assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
        assert page.error_message.get_text() == 'Неверный логин или пароль'

    # 10. Авторизация по связке телефон-пароль - позитивные тесты
    @pytest.mark.parametrize("phone", [seven_phone_plus, eight_phone, seven_phone_without_plus],
                             ids=["+7x format", "8x format", "7x format"])
    def test10_phone_password_auth_pos(self, web_browser, phone, logout_start):

        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartPasswordAuthPage(web_browser)
        page.btn_standard_auth.click()

        page.phone_us_form.send_keys(phone)
        page.password_form.send_keys(valid_password)
        captcha_search(page)
        code_timer_wait(page)
        page.btn_login.click()

        assert page.cabinet.get_text() == 'Личный кабинет'
        assert page.user_name.get_text() == 'Анастасия'  # Проверяем, что h2 соответствует имени пользователя в ЛК

    # 11. Авторизация по связке номер-пароль - негативные тесты с некорректными номерами
    @pytest.mark.parametrize("phone", [invalid_phone_11, invalid_phone_10, invalid_phone_12],
                             ids=["invalid 11 numbers", "invalid 10 numbers", "invalid 12 numbers"])
    def test11_invalid_phone_password_auth_neg(self, web_browser, phone):

        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartPasswordAuthPage(web_browser)
        page.btn_standard_auth.click()

        page.phone_us_form.send_keys(phone)
        page.password_form.send_keys(valid_password)
        captcha_search(page)
        code_timer_wait(page)
        page.btn_login.click()

        assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации

    # 12. Авторизация по связке телефон-пароль - негативный тест с некорректным паролем
    def test12_phone_invalid_password_auth_neg(self, web_browser):

        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartPasswordAuthPage(web_browser)
        page.btn_standard_auth.click()

        page.phone_us_form.send_keys(seven_phone_plus)
        page.password_form.send_keys(invalid_password)
        captcha_search(page)
        code_timer_wait(page)
        page.btn_login.click()

        assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
        assert page.error_message.get_text() == 'Неверный логин или пароль'

    # 13. Авторизация по связке логин-пароль - позитивный тест
    def test13_login_password_auth_pos(self, web_browser, logout_start):

        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartPasswordAuthPage(web_browser)
        page.btn_standard_auth.click()

        page.login_us_form.send_keys(login_valid)
        page.password_form.send_keys(valid_password)
        captcha_search(page)
        code_timer_wait(page)
        page.btn_login.click()

        assert page.cabinet.get_text() == 'Личный кабинет'
        assert page.user_name.get_text() == 'Иван'  # Проверяем, что h2 соответствует имени пользователя в ЛК

    # 14. Авторизация по связке логин-пароль - негативные тесты с некорректными логинами
    @pytest.mark.parametrize("login", [login_only_numbers, login_as_email, login_longer],
                             ids=["only numbers", "as email", "long"])
    def test14_invalid_login_password_auth_neg(self, web_browser, login):

        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartPasswordAuthPage(web_browser)
        page.btn_standard_auth.click()

        page.login_us_form.send_keys(login)
        page.password_form.send_keys(valid_password)
        captcha_search(page)
        code_timer_wait(page)
        page.btn_login.click()

        assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации

    # 15. Авторизация по связке логин-пароль - негативный тест с некорректным паролем
    def test15_login_invalid_password_auth_neg(self, web_browser):

        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartPasswordAuthPage(web_browser)
        page.btn_standard_auth.click()

        page.login_us_form.send_keys(login_valid)
        page.password_form.send_keys(invalid_password)
        captcha_search(page)
        code_timer_wait(page)
        page.btn_login.click()

        assert page.h1.get_text() == 'Авторизация'  # Проверяем, что мы остаёмся на странице авторизации
        assert page.error_message.get_text() == 'Неверный логин или пароль'


class TestResetPass:
    # 16. Доступность восстановления пароля по коду на email
    # Т. к. капчу ввести не можем, проверяем просто, что почта вводится и кнопка нажимается
    # Тест по большому счёту бессмысленный, но если вдруг отключат капчу, его можно было бы быстро допилить до рабочего
    # состояния
    @pytest.mark.parametrize("email", [google_email, mailru_email, yandex_email],
                             ids=["gmail", "mailru", "yandex"])
    def test16_email_reset_password_is_available(self, web_browser, email):

        page = StartResetPasswordPage(web_browser)

        page.email_us_form.send_keys(email)
        code_timer_wait(page)
        page.btn_reset.click()

        assert page.h1.get_text() == 'Восстановление пароля'
        assert page.error_message.get_text() == 'Неверный логин или текст с картинки'

    # 17. Доступность восстановления пароля по коду на телефон
    # Т. к. капчу ввести не можем, проверяем просто, что телефон вводится и кнопка нажимается, без негативных проверок
    @pytest.mark.parametrize("phone", [seven_phone_plus, eight_phone, seven_phone_without_plus],
                             ids=["+7x format", "8x format", "7x format"])
    def test17_phone_reset_password_is_available(self, web_browser, phone):

        page = StartResetPasswordPage(web_browser)

        page.phone_us_form.send_keys(phone)
        code_timer_wait(page)
        page.btn_reset.click()

        assert page.h1.get_text() == 'Восстановление пароля'


class TestRegistration:
    # 18. Регистрация - позитивные тесты для популярных почтовых сервисов. Mail.ru отдельно с полным сценарием
    @pytest.mark.parametrize("email", [gmail_random, yandex_random],
                             ids=["gmail", "yandex"])
    @pytest.mark.xfail(reason='Может сгенерироваться уже зарегистрированный email (маловероятно, но факт)')
    def test18_standard_reg_dif_emails_pos(self, web_browser, email):
        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(email)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        code_timer_wait(page)
        page.btn_reg.click()

        assert page.h1.get_text() == 'Подтверждение email'
        assert page.reg_code_send.get_text() == f'Kод подтверждения отправлен на адрес {email}'

    # 19. Регистрация - полный сценарий через mail.ru
    @pytest.mark.xfail(reason='Код может не прийти или прийти с большой задержкой, если было много прогонов')
    def test19_standard_reg_mailru_pos(self, web_browser, logout_start):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(mailru_random)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        code_timer_wait(page)
        page.btn_reg.click()

        time.sleep(15)  # очень долгое ожидание, чтобы пришло письмо
        page.code_forms.send_keys(code_from_email())

        assert page.cabinet.get_text() == 'Личный кабинет'

    # 20. Регистрация - негативный тест с уже зарегистрированным email
    def test20_standard_reg_used_email_neg(self, web_browser):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(google_email)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        code_timer_wait(page)
        page.btn_reg.click()

        # Вообще ожидаем некоторое сообщение об ошибке, но т. к. его нет, проверяем, что нам на почту не отправили код
        assert page.error_popup.get_text() == 'Учётная запись уже существует'

    # 21. Регистрация - негативные тесты для некорректных email
    @pytest.mark.parametrize("email", [email_fake_domain, email_error_domain, email_50, email_255, email_256, email_1000])
    @pytest.mark.xfail(reason='В данный момент код отправляется на любой email')
    def test21_standard_reg_dif_emails_neg(self, web_browser, email):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(email)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        code_timer_wait(page)
        page.btn_reg.click()

        assert page.h1.get_text() != 'Подтверждение email'

    # 22. Регистрация - позитивные варианты заполнения поля "Имя"
    # В первой версии проекта все варианты подставлялись в рамках одного теста: вставили имя, проверили, что нет
    # сообщения об ошибке, очистили поле, поставили новое имя... Это сокращает время выполнения теста, т. к. страница
    # не грузится заново, но очень неудобно из-за большого количества лишнего кода. Да и проверять надо всё-таки
    # весь сценарий, а не только отсутствие сообщения об ошибке :)
    @pytest.mark.parametrize("name", [name_small, name_caps, name_yo, name_rare, name_2, name_hyphen,
                                      name_hyphen_spaces, name_30])
    def test22_reg_dif_names_pos(self, web_browser, name):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(gmail_random)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        assert page.error_reg_forms.is_presented() is False  # не отображается сообщение об ошибке
        # Дальше код закрыт, потому что мне не нравится мысль инициировать создание кучи учёток,
        # которые я не смогу удалить
        # code_timer_wait(page)
        # page.btn_reg.click()
        # assert page.h1.get_text() == 'Подтверждение email'
        # assert page.reg_code_send.get_text() == f'Kод подтверждения отправлен на адрес {gmail_random}'

    # 23. Регистрация - негативные варианты заполнения поля "Имя"
    # Здесь было аналогично 22 тесту, но тоже нельзя ограничиться чисто проверкой валидации - нельзя быть уверенным,
    # что даже при наличии ошибки форма не отправится :)
    @pytest.mark.parametrize("name", [name_medium_dash, name_long_dash, name_number_dash, name_with_space, name_lat,
                                      name_cyr_lat, name_cyr_num, name_cyr_spec, name_nums, name_specs, name_cyr_chin,
                                      name_chin, name_first_hyph, name_2_first_hyph, name_2_hyph, name_3_words_hyph,
                                      name_31, name_empty, name_spaces, name_last_hyph, name_2_last_hyph])
    @pytest.mark.xfail(reason='Пропускает имя с последним символом дефисом')
    def test23_reg_dif_names_neg(self, web_browser, name):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(gmail_random)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        assert page.error_reg_forms.is_presented() is True  # отображается сообщение об ошибке
        code_timer_wait(page)
        page.btn_reg.click()
        assert page.h1.get_text() != 'Подтверждение email'

    # 24. Регистрация - пустое поле "Имя"
    @pytest.mark.parametrize("name", [name_empty, name_spaces])
    def test24_reg_dif_names_neg(self, web_browser, name):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(gmail_random)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        code_timer_wait(page)
        page.btn_reg.click()
        assert page.h1.get_text() != 'Подтверждение email'

    # 25. Регистрация - позитивные варианты заполнения поля "Фамилия"
    @pytest.mark.parametrize("lastname", [lastname_small, lastname_caps, lastname_yo, lastname_rare, lastname_2,
                                          lastname_hyphen, lastname_hyphen_spaces, lastname_30])
    def test25_reg_dif_lastnames_pos(self, web_browser, lastname):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(gmail_random)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        assert page.error_reg_forms.is_presented() is False  # не отображается сообщение об ошибке
        # Дальше код закрыт, потому что мне не нравится мысль инициировать создание кучи учёток,
        # которые я не смогу удалить
        # code_timer_wait(page)
        # page.btn_reg.click()
        # assert page.h1.get_text() == 'Подтверждение email'
        # assert page.reg_code_send.get_text() == f'Kод подтверждения отправлен на адрес {gmail_random}'

    # 26. Регистрация - негативные варианты заполнения поля "Фамилия"
    @pytest.mark.parametrize("lastname", [lastname_medium_dash, lastname_long_dash, lastname_number_dash,
                                          lastname_with_space, lastname_lat, lastname_cyr_lat, lastname_cyr_num,
                                          lastname_cyr_spec, lastname_nums, lastname_specs, lastname_cyr_chin,
                                          lastname_chin, lastname_first_hyph, lastname_2_first_hyph, lastname_2_hyph,
                                          lastname_3_words_hyph, lastname_31,lastname_empty, lastname_spaces,
                                          lastname_last_hyph, lastname_2_last_hyph])
    @pytest.mark.xfail(reason='Пропускает фамилию с последним символом дефисом')
    def test26_reg_dif_lastnames_neg(self, web_browser, lastname):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(gmail_random)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        assert page.error_reg_forms.is_presented() is True  # отображается сообщение об ошибке
        code_timer_wait(page)
        page.btn_reg.click()
        assert page.h1.get_text() != 'Подтверждение email'

    # 27. Регистрация - пустое поле "Фамилия"
    @pytest.mark.parametrize("lastname", [lastname_empty, lastname_spaces])
    def test26_reg_dif_lastnames_neg(self, web_browser, lastname):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(gmail_random)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(valid_password)
        code_timer_wait(page)
        page.btn_reg.click()
        assert page.h1.get_text() != 'Подтверждение email'

    # 26. Регистрация - тесты для корректных вариантов пароля
    @pytest.mark.parametrize("password", [password_valid_8, password_valid_20])
    def test26_standard_reg_dif_passwords_pos(self, web_browser, password):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)

        page.email_ad_form.send_keys(gmail_random)
        page.password_form.send_keys(password)
        page.password_confirm_form.send_keys(password)
        code_timer_wait(page)
        page.btn_reg.click()

        assert page.h1.get_text() == 'Подтверждение email'
        assert page.reg_code_send.get_text() == f'Kод подтверждения отправлен на адрес {gmail_random}'

    # 27. Регистрация - некорректные пароли
    @pytest.mark.parametrize("password", [password_invalid_7, password_invalid_small, password_invalid_caps,
                                          password_invalid_21])
    def test27_standard_reg_invalid_passwords_neg(self, web_browser, password):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()

        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(gmail_random)
        page.password_form.send_keys(password)
        page.password_confirm_form.send_keys(password)
        assert page.error_reg_forms.is_presented() is True  # отображается сообщение об ошибке
        code_timer_wait(page)
        page.btn_reg.click()
        assert page.h1.get_text() != 'Подтверждение email'

    # 28. Регистрация - введённые пароли не совпадают
    def test28_standard_reg_invalid_password_confirm_neg(self, web_browser):
        page = StartRegPage(web_browser)
        page.btn_standard_auth.click()
        page.btn_to_reg.click()
        page.name_form.send_keys(name)
        page.lastname_form.send_keys(lastname)
        captcha_search(page)
        page.email_ad_form.send_keys(gmail_random)
        page.password_form.send_keys(valid_password)
        page.password_confirm_form.send_keys(password_invalid_small)
        code_timer_wait(page)
        page.btn_reg.click()
        assert page.error_reg_forms.is_presented() is True
