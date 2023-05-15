from pages.base import WebPage
from pages.locators import *


class KeyCodeAuthPage(WebPage):

    def __init__(self, web_driver, url=''):
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_dmh&redirect_uri=' \
              'https://sso.key.rt.ru/api/v1/oauth2/b2c/callback&response_type=code&state=aHR0cHM6Ly9rZXkucnQucnUvbWF' \
              'pbi9zaWduaW4/dD0xNjgxNDczMzM0MTU3'
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
    cabinet = cabinet
    btn_logout = btn_logout_key
    help_text = help_text
    userpic = userpic
    too_many_codes_error = too_many_codes_error
    btn_key_go = btn_key_go


class KeyPasswordAuthPage(WebPage):
    def __init__(self, web_driver, url=''):
        # Загружаем страницу входа по временному коду, к целевой странице переходим по кнопкам
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_dmh&redirect_uri=' \
              'https://sso.key.rt.ru/api/v1/oauth2/b2c/callback&response_type=code&state=aHR0cHM6Ly9rZXkucnQucnUvbWF' \
              'pbi9zaWduaW4/dD0xNjgxNDczMzM0MTU3'
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
    btn_logout = btn_logout_key
    error_message = error_message
    cabinet = cabinet
    userpic = userpic
    too_many_codes_error = too_many_codes_error
    btn_key_go = btn_key_go


class KeyResetPasswordPage(WebPage):
    def __init__(self, web_driver, url=''):
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials?client_id=' \
              'lk_dmh&tab_id=fgp-CS9cjYo'
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


class KeyRegPage(WebPage):
    def __init__(self, web_driver, url=''):
        # Загружаем страницу входа по временному коду, к целевой странице переходим по кнопкам
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_dmh&redirect_uri=' \
              'https://sso.key.rt.ru/api/v1/oauth2/b2c/callback&response_type=code&state=aHR0cHM6Ly9rZXkucnQucnUvbWF' \
              'pbi9zaWduaW4/dD0xNjgxNDczMzM0MTU3'
        super().__init__(web_driver, url)

    # Берём нужные для тестов элементы страницы из локаторов
    left_block = left_block
    right_block = right_block
    rit_tagline = rit_tagline
    reg_div = reg_div
    name_form = name_form
    lastname_form = lastname_form
    region_form = region_form
    email_ad_form = email_ad_form
    phone_ad_form = phone_ad_form
    password_form = password_form
    password_confirm_form = password_confirm_form
    btn_reg = btn_reg
    terms_of_use = terms_of_use
    terms_of_use_link = terms_of_use_link
    captcha_form = captcha_form
    btn_to_reg = btn_to_reg
    btn_standard_auth = btn_standard_auth
    code_timeout = code_timeout
    reg_code_send = reg_code_send
    h1 = h1
    error_reg_forms = error_reg_forms
    user_name = user_name
    userpic = userpic
    code_forms = code_forms
    btn_logout = btn_logout_key
    cabinet = cabinet
    error_popup = error_popup
    btn_key_go = btn_key_go
