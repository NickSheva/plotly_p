import pandas as pd

# Путь к таблице на сайте wikipedia
url = "https://en.wikipedia.org/wiki/List_of_states_and_union_territories_of_India_by_population"
# Чтение файла с помощью pandas
data = pd.read_html(url)
print(data)