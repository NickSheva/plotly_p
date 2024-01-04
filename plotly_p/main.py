"""Извдечение таблицы из сайта wikipedia
и сохрание в .csv file"""
import pandas as pd
import json

# Путь к таблице на сайте wikipedia
page = "https://en.wikipedia.org/wiki/List_of_states_and_union_territories_of_India_by_population"
# Чтение файла с помощью pandas
data = pd.read_html(page)
# Находим количество таблиц на старанице
print(f"Page has: {len(data)} table(s)")
# Нам нужна таблица 1
table = data[1]
# Сохраняем таблицу в excel
table.to_excel('tab.xlsx')
# Сохраняем таблицу в csv
df = pd.DataFrame(table.to_csv('tab.csv', index=False))
# Убираем первую строку из таблицы
with open('tab.csv', 'r') as file:
    with open('table.csv', 'w') as f_out:
        # Пропускаем первую строку
        next(file)
        for i in file:
            # Запись нового файла
            f_out.write(i)
# открывает изменненый файл
df = pd.read_csv('table.csv')
# используем функцию lambda для схранения значения  int в df['Density]
df['Density'] = df['Density [a]'].apply(lambda x: int(x))
print(df['Density'])
# Открываем файл geojson
filename = './states_india.geojson'
india_states = json.load(open(filename, 'r'))
# выводим на экран ключи
print(india_states['features'][0].keys())
# Находим ключ словоря 'properties'  в словаре 'features'
print(india_states['features'][1]['properties'])
# Создаем новый словарь
state_id_map = {}
# запускаем цикл для сохраниния значения 'state_code' в
# значение 'st_nm' в словаре  state_id_map[feature['properties']['st_nm']]
# через новое значение feature['id']
for feature in india_states["features"]:
    feature['id'] = feature['properties']['state_code']
    state_id_map[feature['properties']['st_nm']] = feature['id']



