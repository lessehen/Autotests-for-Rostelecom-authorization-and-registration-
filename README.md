# Автотесты для Ростелекома <br/> (авторизация и регистрация в личном кабинете)

Итоговый проект по автоматизации тестирования в рамках курса Skillfactory.

[Тестовая документация](https://docs.google.com/spreadsheets/d/1GjvSxUXRzA5Rv23GxID3IFa9WvPZGs1j82v-gmGr2TE/edit?usp=sharing)
---

Проект выполнен с использованием библиотеки [Smart Page Object](https://github.com/TimurNurlygayanov/ui-tests-example).

Для работы с проектом необходимо установить зависимости, перечисленные в файле [requirements.txt](requirements.txt):

    pip3 install -r requirements
    
---

## Структура проекта

### Тесты

* В папке [tests](tests) располагаются собственно автотесты.

>В рамках прокта мы тестируем формы авторизации, регистрации и восстановления пароля для продуктов Ростелеком. 
>Каждый файл с тестами содержит группу "нулевых" тестов, проверяющих само наличие элементов, за которыми следуют функциональные тесты для всех указанных форм конкретного продукта.
>Наиболее полный "ассортимент" тестов представлен для продукта ["Старт Web"](tests/test_start.py), т. к. именно для него доступены все функции. Тесты для других продуктов сделаны на основе тестов "Старта" с учётом небольших изменений в требованиях и внешнем виде личного кабинета пользователя.


| Продукт Ростелеком  | Файл с автотестами | Команда для запуска тестов |
| :---    | :----    | :---    |
| Старт Web    | [test_start](tests/test_start.py)    | `python -m pytest -v tests/test_start.py`   |
| ЕЛК Web    | [test_elk](tests/test_elk.py)    | `python -m pytest -v tests/test_elk.py`    |
| Онлайм Web    | [test_onlime](tests/test_onlime.py)    | `python -m pytest -v test_onlime.py`    |
| Ключ Web    | [test_key](tests/test_key.py)    | `python -m pytest -v tests/test_key.py`    |
| Умный дом Web    | [test_shome](tests/test_shome.py)    | `python -m pytest -v tests/test_shome.py`    |

---

### Вспомогательные файлы

1. В папке [pages](pages) располагаются файлы с описанием [базового класса страницы](pages/base.py), вспомогательных классов для определения [веб-элементов](pages/elements.py), [локаторов используемых элементов](pages/locators.py) и классов целевых страниц:
* * [ЕЛК Web](pages/elk_pages.py)
* * [Старт Web](pages/start_pages.py)
* * [Онлайм Web](pages/onlime_pages.py)
* * [Умный дом Web](pages/shome_pages.py)
* * [Ключ Web](pages/key_pages.py)

2. Папка [functions](functions) содержит:
* * Файл [help_functions](functions/help_functions.py), в котором задаются несколько небольших вспомогательных функций, многократно использующихся в тестах.
* * Файл [functions_fill_fields](functions/functions_fill_fields.py), в который вынесены функции, заполняющие тестируемые формы данными и отправляющие их. 
> Эти файлы и сами функции появились уже после сдачи проекта на проверку и помогли значительно сократить код тестов. Так, например, [тесты для Старт Web](tests/test_start.py) в начальной версии содержали более 1100 строк, сейчас — около 400.

3. В папке [parameters](parameters) находятся [тестовые данные](parameters/params_test.py) и [данные для подключения к IMAP-серверу](parameters/params_imap.py).

4. Файл [conftest](conftest.py) содержит фикстуры.

5. Также в корневом катологе расположен драйвер для Google Chrome версии 112 — [chromedriver112.exe](chromedriver112.exe).

6. [docker-compose.yml](docker-compose.yml) остался от библиотеки, и я просто опасаюсь его трогать 🙃 

> ВоПРосЕкИ, почему что-то недостаточно красиво / оптимально сделано, можно задать в [TG](https://t.me/lessehen) — возможно, я даже знаю на них ответ)
