## Общий подход
[Ссылка на задание](https://gist.github.com/chistyakov/a17d47b373b04162e0e76fdf349a656a)

Из требований известно, что каждый час начинается в 00 минут.
Для запросов нам нужны данные за час, и за 12 часов.

Из этих двух вводных звучит логичной идея разделить данные в документы так, чтобы каждый документ содержал в себе данные за 1 час.
Тогда для первого запроса(почасового) мы будем брать 1 документ, для второго(за 12 часов) - 12 документов.

Однако с точки зрения стоимости операций драматически дешевле будет хранить данные кусками по 12 часов.
Это, к сожалению, приводит нас к накладным расходам по доставанию данных за конкретный час при разработке. 
Но зато дёшево с точки зрения денег =)

**Итоговая стоимость: $840.00 в месяц**

Для сравнения: почасовая запись будет стоить около $1300 в месяц.

## Как работала с ChatGPT
Для начала мне нужны были тестовые данные, попросила сгенерировать.

Дальше написала функции для подсчёта стоимости и провалидировала об ChatGPT. У него оказался чуть другой алгоритм подсчёта размеров, использовала тот, что указан в требованияx.

Затем описала ему суть задачи. Он нагенерил код и комментарии, убедилась, что думала в верную сторону.
Чуть оптимизировала его решение.

Затем сверилась с предлагаемым им тестовым покрытием. На мой вкус, предложенное им покрытие избыточно, оставила нужное.

Потом подумала ещё раз и попросила поприкидывать разные варианты разбивки данных (по 1 часу, по 12 часов, etc). Выбрала самый дешёвый, причесала, обложила тестами.

[Ссылка на диалог](https://chat.openai.com/share/f8e54d3a-810c-4a97-835e-87e8f90db714)

## TESTS
### test_convert_to_documents
Тестирует, что написанная функция выдаёт ожидаемый результат.

**Потенциальные места для улучшения:**
- _test_has_all_activity_scores_for_each_hour_ проверяет два поля сразу, гипотетически можно делить на два теста. Но я оставила в таком виде, чтобы проверять, что каждому часу соответствует нужный кусок.

### test_calc_price
Тестирует, что я правильно считаю.

Не стала здесь сильно упарываться в краевые значения и невалидные данные, т.к. по факту это достаточно технический код, а не продуктовый.