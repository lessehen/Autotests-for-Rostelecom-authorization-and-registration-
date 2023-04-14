from pages.elements import WebElement

# Локаторы форм
email_us_form = phone_us_form = login_us_form = ls_us_form = WebElement(id='username')
email_ad_form = phone_ad_form = WebElement(id='address')
password_form = WebElement(id='password')
password_confirm_form = WebElement(id='password-confirm')
code_forms = WebElement(id='rt-code-0')
captcha_form = WebElement(id='captcha')
name_form = WebElement(name='firstName')
name_input = WebElement(xpath='/html/body/div[1]/main/section[2]/div/div/div/form/div[1]/div[1]/div/span[1]/span[1]/text()')  # введённое имя
lastname_form = WebElement(name='lastName')
region_form = WebElement(xpath='//*[@id="page-right"]/div/div/div/form/div[2]/div/div/div[2]')  # стрелка в поле

# Локаторы кнопок
btn_get_code = WebElement(id='otp_get_code')  # получить временный код
btn_standard_auth = WebElement(id='standard_auth_btn')  # перейти к стандартной авторизации
btn_change_data = WebElement(name='otp_back_phone')  # кнопка "изменить номер | почту"
btn_resend_code = WebElement(name='otp_resend_code')  # кнопка получения нового кода
tab_phone = WebElement(id='t-btn-tab-phone')
tab_email = WebElement(id='t-btn-tab-mail')
tab_login = WebElement(id='t-btn-tab-login')
tab_ls = WebElement(id='t-btn-tab-ls')
btn_login = WebElement(id='kc-login')  # кнопка "войти"
btn_back_code = WebElement(id='back_to_otp_btn')  # кнопка "войти по временному коду"
btn_forgot_password = WebElement(id='forgot_password')
btn_to_reg = WebElement(id='kc-register')  # кнопка перехода к регистрации
btn_reset = WebElement(id='reset')  # кнопка сброса пароля
btn_reset_back = WebElement(id='reset-back')  # кнопка "вернуться назад" со страницы сброса пароля
btn_reg = WebElement(name='register')  # кнопка "зарегистрироваться" после заполнения формы
btn_logout = WebElement(class_name='sc-bnOPBZ.dvyUXv')
btn_logout_onlime = WebElement(id='logout-btn')
btn_logout_key = WebElement(class_name='changeUserLink--ecCgz')
btn_logout_shome = WebElement(class_name='sc-ipEyDJ.jXHLMj.button___3jo3H.button___2W6wR')
btn_onlime_go = WebElement(xpath='/html/body/div/main/section[2]/div/div')
btn_key_go = WebElement(class_name='redirect--kJuuA')

# Прочие локаторы
h1 = WebElement(tag_name='h1')
user_name = WebElement(class_name='iqOiiv')
help_text = WebElement(class_name='card-container__desc')  # текст с подсказкой по вводу
code_send = WebElement(class_name='otp-code-form-container__desc')  # куда отправлен код
reg_code_send = WebElement(class_name='register-confirm-form-container__desc')
code_timeout = WebElement(class_name='otp-form__timeout')  # счётчик времени до смены телефона / почты
resend_timeout = WebElement(class_name='code-input-container__timeout')  # счётчик времени до повторной отправки кода
left_block = WebElement(id='page-left')  # страница делится на два вертикальных блока - левый
right_block = WebElement(id='page-right')  # страница делится на два вертикальных блока - правый
rit_tagline = WebElement(class_name='what-is-container')
rit_tagline_xpath = '/html/body/div[1]/main/section[1]/div'
login_div = WebElement(class_name='login-form-container')  # форма входа
login_div_xpath = '/html/body/div[1]/main/section[2]/div'
reg_div = WebElement(class_name='register-form-container')  # форма регистрации
terms_of_use = WebElement(class_name='auth-policy')
terms_of_use_link = WebElement(xpath='/html/body/div[1]/main/section[2]/div/div/div/form/div[5]/a')
error_message = WebElement(id='form-error-message')
error_reg_forms = WebElement(class_name='rt-input-container__meta--error')  # ошибки в форме регистрации
too_many_codes_error = WebElement(class_name='code-input-container__error')
cabinet = WebElement(class_name='StyledHeaderTopPartMenuItemLk-kHgfwO')
cabinet_onlime = WebElement(xpath='/html/body/div/header/div/div[2]/div/div[1]/a[2]')
error_popup = WebElement(class_name='card-modal__title')
captcha_image = WebElement(class_name='rt-captcha__image')
userpic = WebElement(xpath='/html/body/div[1]/div/div/div[1]/div/div[1]/div[3]/div[2]')
userpic_shome = WebElement(class_name='profileLink___pMvUU')
my_home = WebElement(id='go_to_home_1088532')
