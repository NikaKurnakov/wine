from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
import pprint
import collections


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('index.html')

lists = collections.defaultdict(list)
excel_data_df = pandas.read_excel('wine.xlsx', usecols=['Название', 'Сорт', 'Цена', 'Картинка'])
excel_data2 = pandas.read_excel('wine2.xlsx', usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка'], na_values=['N/A', 'NA'], keep_default_na=False)
wines = excel_data_df.to_dict(orient="records")
wines2 = excel_data2.to_dict(orient="records")
column_key = excel_data2['Категория'].to_dict()
wines_by_category = excel_data2.groupby('Категория').apply(lambda x: x.to_dict(orient='records')).to_dict()
result = {
    '': wines_by_category
}
# for result in wines_by_category:
#     lists[result].append(result)
pprint.pprint(result)


years = "103"
name_age = ""
if years[-2:] == "11" or years[-2:] == "12" or years[-2:] == "13" or years[-2:] == "14":
    name_age = "лет"
elif years[-1] == "1":
    name_age = "год"
elif years[-1] == "2" or years[-1] == "3" or years[-1] == "4":
    name_age = "года"
elif years[-1] == "0" or years[-1] == "5" or years[-1] == "6" or years[-1] == "7" or  years[-1] == "8" or years[-1] == "9":
    name_age = "лет"

rendered_page = template.render(
    years_text=f"Уже {years} {name_age}",
    wines=wines
)




with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()