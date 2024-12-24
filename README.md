
# Шифровальщик данных

## Для чего был создан данный проект

Данный проект был создан для того, чтобы можно было хранить пароли прямо на рабочем столе/в книжке с паролями, не боясь, что их используют, т.к. они будут храниться в зашифрованном виде.

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

### Установка зависимостей:

```
pip install pycryptodome
```

## Запуск проекта

### Хэширование данных

#### С ключ-фразой из `config.json`:

```
python main.py -ey <data>
```

#### С ключ-фразой, введенной вручную:

```
python main.py -e <data> <secret_phrase>
```

**Пример использования**

Ввод:

```
python main.py -e "Hello World!" "Test"
```

Вывод:

```
Encoded data: 4lgtf8M1ZJZ+rs8nCDf7SeJ4RWQfV+AHlb+G236PPoU=
```

### Дехэширование данных

#### С ключ-фразой из `config.json`:

```
python main.py -dy <hash>
```

#### С ключ-фразой, введенной вручную:

```
python main.py -d <hash> <secret_phrase>
```

**Пример использования**

Ввод:

```
python main.py -d 4lgtf8M1ZJZ+rs8nCDf7SeJ4RWQfV+AHlb+G236PPoU= "Test"
```

Вывод:

```
Decoded data: Hello World!
```

### Проверка правильности хэша

#### С ключ-фразой из `config.json`:

```
python main.py -cy <hash>
```

#### С ключ-фразой, введенной вручную:

```
python main.py -c <hash> <secret_phrase>
```

**Пример использования**

Ввод:

```
python main.py -c 4lgtf8M1ZJZ+rs8nCDf7SeJ4RWQfV+AHlb+G236PPoU= "Hello World!" "Test"
```

Вывод:

```
Success: строка соответствует хэшу.
```

### Работа с логом

#### Вывод лога:

```
python main.py log
```

#### Очистка лога:

```
python main.py log -d
```

**Пример использования**

Ввод:

```
python main.py log
```

Вывод:

```
---------------------------------------------Операции---------------------------------------------

[2024-12-24 16:33:43.396941]
Operation Type: Encode
Data: Hello World!, Encrypted: fIGB7Zt9LKz7kOsu6yGStF/4LRD4ZXaAveBb0VTcTtI=


[2024-12-24 16:34:15.103751]
Operation Type: Decode
Encrypted: fIGB7Zt9LKz7kOsu6yGStF/4LRD4ZXaAveBb0VTcTtI=, Decrypted: Hello World!


[2024-12-24 16:34:27.081862]
Operation Type: Check Hash
Success: строка 'Hello World!' соответствует хэшу 'fIGB7Zt9LKz7kOsu6yGStF/4LRD4ZXaAveBb0VTcTtI='.



--------------------------------------------------------------------------------------------------
```

Ввод:

```
python main.py log -d
```

Вывод:

```
Лог-файл очищен.
```

### Просмотр команд в консольном режиме

Вывод всех команд:

```
python main.py -h
```

## Быстрое хэширование и дехэширование

Базовая версия файла `config.json`:

```json
{
    "Password": {
        "Secret_key": "Input Your secret key here"
    }
}
```