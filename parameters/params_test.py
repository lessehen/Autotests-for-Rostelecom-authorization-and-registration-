from functions.help_functions import generate_alphanum_random_string

valid_password = '&IsguorIR2T4J'

google_email = 'testov.testov.test.test@gmail.com'
gmail_random = f'testov.testov.test.test+{generate_alphanum_random_string(16)}@gmail.com'

mailru_email = 'test_test_testov_testov@mail.ru'
mailru_random = f'test_test_testov_testov+{generate_alphanum_random_string(16)}@mail.ru'

yandex_email = 'test.test.testov.testov@yandex.ru'
yandex_random = f'test.test.testov.testov+{generate_alphanum_random_string(16)}@yandex.ru'

seven_phone_plus = '+7 913 982-32-85'
seven_phone_without_plus = '7 913 982-32-85'
eight_phone = '8 913 982-32-85'
invalid_phone_11 = '12345678910'
invalid_phone_10 = '7345678910'
invalid_phone_12 = '792345678910'
phone_for_key = '79538853278'

login_valid = 'rtkid_1681039760749'
login_shome = 'rtkid_1680791769627'
login_only_numbers = '1681039760749'
login_as_email = 'test.test.testov.testov'
login_longer = 'rtkid_16810397607499'

password_valid_8 = '&Isguor8'
password_valid_20 = '&IsguorIR2T4J&Isguor'
invalid_password = 'qwert12345'
password_invalid_7 ='&Isuor8'
password_invalid_small = '&isguorir2t4j'
password_invalid_caps = '&ISGUORIR2T4J'
password_invalid_21 = '&IsguorIR2T4J&IsguorI'

name = 'Иван'
name_small = 'иван'
name_caps = 'ИВАН'
name_rare = 'Адриан'
name_2 = 'Ян'
name_hyphen = 'Кристиан-Василий'
name_hyphen_spaces = 'Кристиан - Василий'
name_30 = 'Александроиннокентиймаксимофей'
name_yo = 'Пётр'

name_medium_dash = 'Кристиан–Василий'
name_long_dash = 'Кристиан—Василий'
name_number_dash = 'Кристиан‒Василий'
name_with_space = 'Кристиан Василий'
name_lat = 'Ivan'
name_cyr_lat = 'Иvan'
name_cyr_num = 'Иван2'
name_cyr_spec = 'Иван*'
name_nums = '761523'
name_specs = '!@*#$&'
name_cyr_chin = 'Иван漢字'
name_chin = '漢字伊万'
name_first_hyph = '-Иван'
name_last_hyph = 'Иван-'
name_2_first_hyph = '-Ф'
name_2_last_hyph = 'А-'
name_2_hyph = '--'
name_3_words_hyph = 'Иван-Аркадий-Павел'
name_31 = 'Александроиннокентиймаксимофеий'
name_empty = ''
name_spaces = '   '

lastname = 'Кузнецов'
lastname_small = 'кузнецов'
lastname_caps = 'КУЗНЕЦОВ'
lastname_rare = 'Мекле'
lastname_2 = 'Ли'
lastname_hyphen = 'Соколов-Митрич'
lastname_hyphen_spaces = 'Соколов - Митрич'
lastname_30 = 'Черезаборбосоногозадерищенский'
lastname_yo = 'Семёнов'

lastname_medium_dash = 'Соколов–Митрич'
lastname_long_dash = 'Соколов—Митрич'
lastname_number_dash = 'Соколов‒Митрич'
lastname_with_space = 'Соколов Митрич'
lastname_lat = 'Ivanov'
lastname_cyr_lat = 'Иvanов'
lastname_cyr_num = 'Иванов25'
lastname_cyr_spec = 'Иванов*)'
lastname_nums = '761523'
lastname_specs = '!@*#$&'
lastname_cyr_chin = 'Иванов漢字'
lastname_chin = '漢字伊万'
lastname_first_hyph = '-Иванов'
lastname_last_hyph = 'Иванов-'
lastname_2_first_hyph = '-Ф'
lastname_2_last_hyph = 'А-'
lastname_2_hyph = '--'
lastname_3_words_hyph = 'Соколов-Микитов-Митрич'
lastname_31 = 'Череззаборбосоногозадерищенский'
lastname_empty = ''
lastname_spaces = '   '

email_fake_domain = 'mail@fake.gb'
email_error_domain = 'mail@yandex.r'
email_50 = 'dsrfepcnoloqp0n4o6nkfei87n6axwlf9kmcvgptw3@mail.ru'
email_255 = 'oq6cg2zhwees94zxlvx86m5e1zitqrmvkfah0um11ahyrht717na2bzgr4t90yby7ol83duhfg7u2bqvzvpr1tg6kfks798wa4g4kvao' \
            'lukqrfnqsxs7t5qa0upbiedx31w03nqde0cltn38otspc0ymmsuqtfmwygrjnz50hhxm0y987yjzc9lyh3kfo8x328fmeh2ykcyevrv9' \
            '4zlfq4tzpj9vag7176dgiveknnqmj2pq15434eu@mail.ru'
email_256 = 'oq6cg2zhwees94zxlvx86m5e1zitqrmvkfah0um11ahyrht717na2bzgr4t90yby7ol83duhfg7u2bqvzvpr1tg6kfks798wa4g4kvao' \
            'lukqrfnqsxs7t5qa0upbiedx31w03nqde0cltn38otspc0ymmsuqtfmwygrjnz50hhxm0y987yjzc9lyh3kfo8x328fmeh2ykcyevrv9' \
            '4zlfq4tzpj9vag7176dgiveknnqmj2pq15434eu3@mail.ru'
email_1000 = 'u8gtjxvkb17yd82e3vjy27xxtn64gjespcmfvch571nyvtwwq2dtrx0yj6qf1mhbskprkeb2q1gxnmebfh2efi9kgh1f6wmwotuo0g6' \
             'isp7fvsggjpzp9j93vif15ng7m2brehhnoojno4jtzp3rvaqk8xxijy1r7r1siet7lw3dn4gr999zgrtf6lc84k44d8x4cx0xnf932f' \
             'b4u3wnttw0hl1panq3wdjghirkfi1ougnbqmz4ryz2ggwysqnip05u7lv5za8s09ch5bxnopms1j8vje0l1jtboz7jh4i60a3h6yh27' \
             '3otkf0ajsqyiuxn5srq4cxo6zvpfuh4bmre5d273olm1yy2au6zo5f99q18mlcnbhu9s5rvaca61pyy21t22q4mxlcn0lrl772v922' \
             'bibahjq4xdfgjf04mbj7amxt7n67qru6oflk00x57d94e7uqb6a8xoqoh618s0g18focy32z9g1t7zgrwqibnogi9nqo3r34a9oen95' \
             'xz2usl3hhzh2fe7zjoltxpxd1h2n8yusg2330fu72jygl1hgeiivjyh7atej8mn5w96sapxvdcsvxmhctmjqw7q42k95irv3mvsls7t' \
             'dyt3goqb2o5zekodore94baatgs3v3nrgjf1lgrafqv820pgj3c80tqach36rm24s0cvzf3nftg4s35wli74p0rds4j9rrurbe16pyl' \
             'we9u93fem9lvl626ugy3qu2mwsb6lp9zeu5i3u2nsgv8l338mfgb00rk515p0pdn7kup5sb86ikncp7at7z2q9xger0foftbc7pciuu' \
             '3moq6hgeekpeov97tcqrt3xrkrdkjddnkex7ijaosu15susza9uvdidu2bo36pfvaltxa7q462npnfa69im8hcj5621xoxjthj5f5yv' \
             'cq2f5frrb6ocjc4v6el9zii4zhrd7r6rvpfyzvdh69ym40ov9ty1xu10k4owvjp6v6@mail.ru'
