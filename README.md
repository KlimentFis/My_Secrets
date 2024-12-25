
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
pip install pycryptodome==3.21.0
```

## Запуск проекта

### Шифрование данных

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

### Дешифрование данных

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

### Проверка правильности шифра

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

### Шифровка файла

#### С ключ-фразой из `config.json`:

```
python main.py -efy <file>
```

#### С ключ-фразой, введенной вручную:

```
python main.py -efy <file> <secret_phrase>
```

**Пример использования**

Ввод:

```
python main.py -ef test.txt "Hello World!"
```

Вывод:

```
Success: файл test.txt зашифрован.
```

### Расшифровка файла

#### С ключ-фразой из `config.json`:

```
python main.py -dfy <file>
```

#### С ключ-фразой, введенной вручную:

```
python main.py -dfy <file> <secret_phrase>
```

**Пример использования**

Ввод:

```
python main.py -df test.txt "Hello World!"
```

Вывод:

```
Success: файл test.txt расшифрован.
```

### Шифрование директории

#### С ключ-фразой из `config.json`:

```
python main.py -edy <directory>
```

#### С ключ-фразой, введенной вручную:

```
python main.py -edy <directory> <secret_phrase>
```

**Пример использования**

Ввод:

```
python main.py -ed Test "Hello World!"
```

Вывод:

```
Encrypting: Test\19a969647d79feb6fb745665ff732337a5eb7416r1-720-720v2_uhq.jpg
Encrypting: Test\8227876-kurama.jpg
Encrypting: Test\maxresdefault.jpg
Encrypting: Test\Снимок экрана 2024-12-23 235324.png
```

### Расшифровывание директории

#### С ключ-фразой из `config.json`:

```
python main.py -ddy <directory>
```

#### С ключ-фразой, введенной вручную:

```
python main.py -dd <directory> <secret_phrase>
```

**Пример использования**

Ввод:

```
python main.py -ed Test "Hello World!"
```

Вывод:

```
Decrypting: Test\19a969647d79feb6fb745665ff732337a5eb7416r1-720-720v2_uhq.jpg
Decrypting: Test\8227876-kurama.jpg
Decrypting: Test\maxresdefault.jpg
Decrypting: Test\Снимок экрана 2024-12-23 235324.png
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
[2024-12-24 16:57:09.344184]
Operation Type: Encode
Data: Hello World!, Encrypted: AMQnsiy3mO9K/d54GdttWphFt7cSHfu+VrAgs9Cj9zA=

[2024-12-24 16:57:21.551593]
Operation Type: Decode
Encrypted: AMQnsiy3mO9K/d54GdttWphFt7cSHfu+VrAgs9Cj9zA=, Decrypted: Hello World!

[2024-12-24 16:57:36.702427]
Operation Type: Check Hash
Success: строка 'Hello World!' соответствует хэшу 'AMQnsiy3mO9K/d54GdttWphFt7cSHfu+VrAgs9Cj9zA='.
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

## Быстрое шифрование и дешифрование

Базовая версия файла `config.json`:

```json
{
    "Password": {
        "Secret_key": "Input Your secret key here"
    }
}
```