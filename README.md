1. Ссылка на Google Sheets: https://docs.google.com/spreadsheets/d/12DKhaTqeFNSs-17tY89D3johfTKXtkXnulbhltB3_Lc/edit#gid=0
2. Скрипт обновления БД из Google Sheets /maindir/app/script.py
3. Google API credentials /maindir/app/kanalservis_sa.json

Инструкция по запуску:

1) Скачать файл с GitHub и разархивировать в удобную для вас директорию
2) Из этой директории, через командную строку, перейти в kanalservis_tz командой cd kanalservis_tz
3) Установить приложение Docker и настроить соответвующе под вашу операционную систему (на Winows включить Hyper-V, отключить wslEngineEnabled. На Linux наоборот). Запустить Docker
4) В директории kanalservis_tz создать файл .env и вписать туда данные для переменных окружения:
   TELEGRAM_API_KEY
   TELEGRAM_USER_ID
   SPREADSHEET_ID
   1) Узнать свой telegram_id можно написав боту @getmyid_bot
5) Перейти обратно в директорию kanalservis_tz и прописать команду docker-compose up --build
6) Открыть браузер и перейти по адресу 127.0.0.1:8000
7) Подождать 1 минуту, чтобы выполнилась запланированная задача для обновления БД
   1) В командой строке можно увидеть кол-во добавленных, изменённых и удалённых записей
