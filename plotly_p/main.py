import pandas as pd
import csv


# Путь к таблице на сайте wikipedia
url = "https://en.wikipedia.org/wiki/List_of_states_and_union_territories_of_India_by_population"
# Чтение файла с помощью pandas
data = pd.read_html(url)
# Находим количество таблиц на старанице
print(f"Page has: {len(data)} table(s)")
# Нам нужна таблица 1
table = data[1]
# Сохраняем таблицу в excel
table.to_excel('tab.xlsx')
# Сохраняем таблицу в csv
pd.DataFrame(table.to_csv('tab.csv'))

