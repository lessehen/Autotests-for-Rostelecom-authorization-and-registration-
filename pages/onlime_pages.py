from pages.base import WebPage
from locators import *


class OnlimeCodeAuthPage(WebPage):

    def __init__(self, web_driver, url=''):
        url = 'https://my.rt.ru/'
        super().__init__(web_driver, url)

    # Берём нужные для тестов элементы страницы из локаторов
    email_ad_form = email_ad_form
    phone_ad_form = phone_ad_form
    btn_get_code = btn_get_code
    btn_standard_auth = btn_standard_auth
    h1 = h1
    code_send = code_send
    code_timeout = code_timeout
    btn_change_data = btn_change_data
    code_forms = code_forms
    resend_timeout = resend_timeout
    btn_resend_code = btn_resend_code
    captcha_form = captcha_form
    user_name = user_name
    cabinet = cabinet_onlime
    btn_logout_onlime = btn_logout_onlime
    help_text = help_text
    userpic = userpic
    too_many_codes_error = too_many_codes_error
    btn_onlime_go = btn_onlime_go


class OnlimePasswordAuthPage(WebPage):
    def __init__(self, web_driver, url=''):
        # Загружаем страницу входа по временному коду, потому что прямую ссылку на нужную добыть не удалось
        url = 'https://my.rt.ru/'
        super().__init__(web_driver, url)

    # Берём нужные для тестов элементы страницы из локаторов
    btn_standard_auth = btn_standard_auth
    email_us_form = email_us_form
    phone_us_form = phone_us_form
    login_us_form = login_us_form
    ls_us_form = ls_us_form
    password_form = password_form
    btn_login = btn_login
    btn_back_code = btn_back_code
    btn_forgot_password = btn_forgot_password
    btn_to_reg = btn_to_reg
    h1 = h1
    code_timeout = code_timeout
    left_block = left_block
    right_block = right_block
    rit_tagline = rit_tagline
    login_div = login_div
    tab_phone = tab_phone
    tab_email = tab_email
    tab_login = tab_login
    tab_ls = tab_ls
    captcha_form = captcha_form
    user_name = user_name
    btn_logout_onlime = btn_logout_onlime
    error_message = error_message
    userpic = userpic
    too_many_codes_error = too_many_codes_error
    btn_onlime_go = btn_onlime_go
    cabinet = cabinet_onlime


class OnlimeResetPasswordPage(WebPage):
    def __init__(self, web_driver, url=''):
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials?client_id=lk_onlime&' \
              'tab_id=6mSOx_p9qDY'
        super().__init__(web_driver, url)

    # Берём нужные для тестов элементы страницы из локаторов
    tab_phone = tab_phone
    tab_email = tab_email
    tab_login = tab_login
    tab_ls = tab_ls
    email_us_form = email_us_form
    phone_us_form = phone_us_form
    captcha_form = captcha_form
    btn_reset = btn_reset
    btn_reset_back = btn_reset_back
    code_timeout = code_timeout
    h1 = h1
    error_message = error_message
    captcha_image = captcha_image
