"""Извдечение таблицы из сайта wikipedia
и сохрание в .csv file"""
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.io as pio


pio.renderers.default = 'browser'
# Путь к таблице на сайте wikipedia
page = "https://en.wikipedia.org/wiki/List_of_states_and_union_territories_of_India_by_population"
# Чтение файла с помощью pandas
data = pd.read_html(page)
# Находим количество таблиц на старанице
print(f"Page has: {len(data)} table(s)")
# Нам нужна таблица 1
table = data[1]
# print(table)
# # Сохраняем таблицу в excel
table.to_excel('tab.xlsx')
# # Сохраняем таблицу в csv
df = pd.DataFrame(table.to_csv('tab.csv', index=False))
# Убираем первую строку из таблицы
with open('tab.csv', 'r') as file:
    with open('table.csv', 'w') as f_out:
        # Пропускаем первую строку
        next(file)
        for i in file:
            # Запись нового файла
            f_out.write(i)

# f = df["State or Union Territory"]
# Открываем файл geojson
filename = './states_india-2.geojson'
india_states = json.load(open(filename, 'r'))
# выводим на экран ключи
all_key = india_states['features'][1]['properties']
print(all_key) # dict_keys(['type', 'geometry', 'properties'])
# Находим ключ словоря 'properties'  в словаре 'features'
# print(india_states['features'][0]['properties']) # {'cartodb_id': 1, 'state_code': 0, 'st_nm': 'Telangana'}
# Создаем новый словарь
state_id_map = {}
# запускаем цикл для сохраниния значения 'state_code' в
# значение 'st_nm' в словаре  state_id_map[feature['properties']['st_nm']]
# через новое значение feature['id']
for feature in india_states["features"]:
    feature['id'] = feature['properties']['state_code']
    state_id_map[feature['properties']['st_nm']] = feature['id']

# Заменяем '&' на 'and', убираем [c] в конце города, изменяем название некоторых городов как и в файле .csv
state_id_map = {key.replace('&', 'and').replace('Telengana', 'Telangana')
                .replace('Delhi', 'NCT of Delhi')
                .replace('Andaman and Nicobar', 'Andaman and Nicobar Islands')
                .replace('Manipur', 'Manipur[c]'):
                    value for key, value in state_id_map.items()}
# print(state_id_map.keys())
df = pd.read_csv('table.csv')
# Вывод для заголовков таблицы
# print(list(df.columns.values.tolist()))
#  print(df["Density [a]"])
#  Изменяем данные на int с помощью фукции lambda и мета apply применяем ко всем
#  сохраняем в новой переменной для всей таблицы
df['Density'] = df["Density [a]"].apply(lambda x: int(x))
#  устанавливаем плотновть населения с np.log10
df['DensityScale'] = np.log10(df["Density"])
#  Удаляем две строчки 34 и 36, которых нет в .geojson file
df = df.drop([34, 36])
#  Все города
#  print(df["State or Union Territory"])
# Вставляем 'id' в таблицу городов посредсвом apply и lambda
df["id"] = df["State or Union Territory"].apply(lambda x: state_id_map[x])
# Выводим новую таблицу с новые заголовки с данными
print(list(df.columns.values.tolist()))
# Вводим необходимые данные для отображения индии на карте мира
# fig = px.choropleth(df,
#                     locations='id',
#                     geojson=india_states,
#                     color='DensityScale',
#                     scope='asia',
#                     hover_name='State or Union Territory',
#                     hover_data=(['Density']))
fig = px.choropleth_mapbox(df,
                           locations='id',
                           geojson=india_states,
                           color='DensityScale',
                           hover_name='State or Union Territory',
                           hover_data=['Density'],
                           mapbox_style='carto-positron',
                           center={'lat': 24, 'lon': 78},
                           zoom=3, opacity=0.5)
# скрываем карту мира
fig.update_geos(fitbounds='locations', visible=False)
fig.show()

