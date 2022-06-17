import os
from datetime import datetime
import django
import telebot
from bs4 import BeautifulSoup
import httplib2
import apiclient
import requests
from oauth2client.service_account import ServiceAccountCredentials
from main.models import Order


# Определяем settings для данного скрипта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Данные для авторизации и получения доступа к Google Sheets API
CREDENTIALS_FILE = 'kanalservis_sa.json'
spreadsheet_id = '12DKhaTqeFNSs-17tY89D3johfTKXtkXnulbhltB3_Lc'


def auth_in_api():
    """Авторизация и подключение к API"""
    # Подключаемся к  API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    # Авторизуемся по http запросу
    http_auth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=http_auth)
    return service


def get_google_sheet_data():
    """Получение данных после авторизации"""
    service = auth_in_api()
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A:D',
        majorDimension='ROWS'
    ).execute()
    return values['values']


def get_usd_rub_price():
    """Получение актуального курса доллара в рублях"""
    url = 'https://www.cbr.ru/scripts/XML_daily.asp?'
    xml_data = requests.get(url).text
    soup = BeautifulSoup(xml_data, "xml")
    # ищем валюту по id USD
    currency_value = float(soup.find("Valute", {'ID': 'R01235'}).find("Value").get_text(strip=True).replace(',', '.'))
    return currency_value


def sheet_orders_list(values):
    """Создаём список таблицы заказов, каждый элемент - модель Order"""
    # Получаем цену доллара в рублях
    usd_rub_price = get_usd_rub_price()
    sheet_orders = []
    for i in range(1, len(values)):
        item = values[i]
        # Приводим дату каждой строки, к рабочему формату Django
        delivery_date = datetime.strptime(str(item[3]).strip(), '%d.%m.%Y').date()
        # Определяем цену в рублях
        rub_price = round(float(item[2].replace(',', '.')) * usd_rub_price, 2)

        order = Order(article=item[1], price=float(item[2]), rub_price=rub_price,
                      delivery_date=delivery_date)
        sheet_orders.append(order)
    return sheet_orders


def check_overdue_orders(orders):
    """Проверяем список на просроченные заказы и отправляем в телеграмм"""
    overdue_orders = []
    for order in orders:
        if order.delivery_date < datetime.now().date():
            overdue_orders.append(order)

    bot = telebot.TeleBot(os.getenv('TELEGRAM_API_KEY', '5478578538:AAFmpn-tP2G5pkC_wG-WBPqTuF-yB03325E'))

    stroka = f"{len(overdue_orders)} overdue orders\n"
    # если есть просроченные заказы
    if overdue_orders:
        # Сортируем по дате от старых к новым
        overdue_orders.sort(key=lambda x: x.delivery_date, reverse=False)
        for item in overdue_orders:
            stroka += f"Order: {item.article} Date: {item.delivery_date}\n"
        bot.send_message(os.getenv('TELEGRAM_USER_ID', '743338178'), stroka)


def update_orders_info():
    """Обновляем/добавляем/удаляем информацию о заказах"""
    # получаем список заказов из гугл таблицы
    sheet_orders = sheet_orders_list(get_google_sheet_data())
    # Список заказов в БД
    bd_orders = Order.objects.all()
    # Список номеров заказов в гугл таблице
    sheet_orders_articles = [sheet_order.article for sheet_order in sheet_orders]
    # Списки для работы с заказами гугл таблицы
    orders_to_create, orders_to_update, orders_to_delete_articles = [], [], []
    # Передаем список заказов на проверку просроченных и отправку сообщения в ТГ
    check_overdue_orders(sheet_orders)

    if bd_orders:
        for bd_order in bd_orders:
            for sheet_order in sheet_orders:
                # получаем записи для обновления
                if not sheet_order.__eq__(bd_order) and sheet_order.article == bd_order.article:
                    orders_to_update.append(bd_orders)
                    # прерываем цикл при совпадении
                    break
            # получаем записи для удаления из БД
            if bd_order.article not in sheet_orders_articles:
                orders_to_delete_articles.append(bd_order.article)
        # получаем записи для добавления, если таблица в БД не пуста
        for item in sheet_orders:
            if item.article not in [bd_order.article for bd_order in bd_orders]:
                orders_to_create.append(item)
    else:
        # получаем записи для добавления, если таблица в БД пуста
        orders_to_create = sheet_orders

    if orders_to_create:
        Order.objects.bulk_create(orders_to_create)
    if orders_to_update:
        Order.objects.bulk_update(sheet_orders, ['price', 'rub_price', 'delivery_date'])
    if orders_to_delete_articles:
        Order.objects.filter(article__in=orders_to_delete_articles).delete()

    print(f"Table main_order was updated.\n"
          f"{len(orders_to_create)} orders were created\n"
          f"{len(orders_to_update)} orders were updated\n"
          f"{len(orders_to_delete_articles)} orders were deleted\n")
