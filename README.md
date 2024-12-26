# Консольный шифровальщик

## Для чего был создан данный проект
**Данный проект был создан для быстрого шифрования данных из консоли.**
#### И позволяет шифровать:
- Строки
- Файлы
- Директории

**Что позволяет хранить ценные данные в сохранности, держа их на виду у всех в зашифрованном виде, с помощью ключевой фразы.**

## Установка

### Клонирование репозитория:

```
git clone https://github.com/KlimentFis/My_Secrets.git
```

### Переход в папку проекта:

```
cd My_Secrets
```

### Создание виртуального окружения:

```
python -m venv venv
```

### Активация виртуального окружения:

```
venv\Scripts\activate
```

### Установка зависимостей:

```
pip install pycryptodome==3.21.0
```

## Запуск проекта
### Вид команд:
Работа с логом:
```
python main.py log -d ( optional )
```
Работа с другими командами:
```
python main.py <flags> <input data>
```

#### [Подробная инструкция](docs/usage.md)

## Быстрое шифрование и дешифрование

Базовая версия файла `config.json`:

```json
{
    "Password": {
        "Secret_key": "Input Your secret key here"
    }
}
```