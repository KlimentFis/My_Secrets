# Шифровальщик данных
## Для чего был создан данный проект
Данный проект был создан для того, чтобы можно было хранить пароли прямо на рабочем столе/книжке с паролями, не боясь что их используют, т.к. хранится они будут в зашифрованном виде.

## Установка
Клонирование репозитория:
```
git clone https://github.com/KlimentFis/My_Secrets.git
```
Переход в папку проекта:
```
cd My_Secrets
```
Создание виртуального окружения:
```
python -m venv venv
```
Установка зависимостей:
```
pip install pycryptodome
```

## Запуск проекта
### Хеширование данных
С ключ-фразой из config.json:
```
python main.py -ey your_password
```
С ключ-фразой веденной вручную:
```
python main.py -e your_password My_Secret_phrase
```
### Дехеширование данных
С ключ-фразой из config.json:
```
python main.py -dy hash 
```
С ключ-фразой веденной вручную:
```
python main.py -d hash My_Secret_phrase
```
### Обзор функционала
Вывод всех команд:
```
python main.py -h
```

## Быстрое хеширование и дехеширование
Базовая версия файла [config.json](config.json):
```json
{
    "Password":
        {
            "Secret_key": "Input Your secret key here"
        }
}
```