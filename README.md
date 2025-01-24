# Приложение по файлам CORPRESS

Основной код приложения находится в файле "app_bd.py".

**Как запустить:**
1. Открыть файл "app_bd.py" в pycharm.
2. Открыть терминал, написать команду "python app_bd.py"
3. Перейти по ссылке в терминале ("Running on: <ссылка>"). Эта ссылка ведет на начальную страницу.

На вкладке /table находится основная таблица (по файлу "new_inton_units_with_f0.csv"). В ней информация по всем файлам:
* название файла
* интонационная модель
* границы синтагмы
* длительность синтагмы (сек)
* слова в этой синтагме
* транскрипция слов
* значения ЧОТ

Внизу на вкладке /table есть возможность выбрать интонационную модель из выпадающего списка и вывести все синтагмы с этой моделью.
Так же можно вывести все синтагмы конкретного файла.

Есть кнопки для подсчета общего числа синтагм в таблице и средней длительности синтагмы в секундах.
