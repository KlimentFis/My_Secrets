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
### Хэширование данных
С ключ-фразой из config.json:
```
python main.py -ey <data>
```
С ключ-фразой веденной вручную:
```
python main.py -e <data> <secret_phrase>
```
### Дехэширование данных
С ключ-фразой из config.json:
```
python main.py -dy <hash>
```
С ключ-фразой веденной вручную:
```
python main.py -d <hash> <secret_phrase>
```

### Проверка правильности хэша
С ключ-фразой из config.json:
```
python main.py -cy <hash>
```
С ключ-фразой веденной вручную:
```
python main.py -c <hash> <secret_phrase>
```

### Работа с логом
Вывод лога:
```
python main.py log
```
Очистка лога:
```
python main.py log -d
```

### Просмотр команд в консольном режиме
Вывод всех команд:
```
python main.py -h
```

## Быстрое хэширование и дехэширование
Базовая версия файла [config.json](config.json):
```json
{
    "Password":
        {
            "Secret_key": "Input Your secret key here"
        }
}
```