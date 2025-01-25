### Все Флаги для работы команды

Ввод:
```
python main.py -h
```
Вывод:
```
-------------------------------------------------Help-------------------------------------------------
Flags:
-h: Show help
-e: Encrypt (with optional secret phrase)
-d: Decrypt (with optional secret phrase)
-c: Check if string matches hash (with optional secret phrase)
-<x>f: Encrypt/Decrypt file (with optional secret phrase)
-<x>d: Encrypt/Decrypt directory (with optional secret phrase)

Use Encrypt:
  -ey <data>: Encrypt using secret phrase from config.json
  -e <data> <secret_phrase>: Encrypt with manually entered secret phrase

Use Decrypt:
  -dy <data>: Decrypt using secret phrase from config.json
  -d <data> <secret_phrase>: Decrypt with manually entered secret phrase

Use Check:
  -cy <hash> <data>: Check if string matches hash using secret phrase from config.json
  -c <hash> <data> <secret_phrase>: Check if string matches hash with manually entered secret phrase

Use File Encryption/Decryption:
  -efy <file>: Encrypt file using secret phrase from config.json
  -ef <file> <secret_phrase>: Encrypt file with manually entered secret phrase
  -dfy <file>: Decrypt file using secret phrase from config.json
  -df <file> <secret_phrase>: Decrypt file with manually entered secret phrase

Use Directory Encryption/Decryption:
  -edy <directory>: Encrypt folder using secret phrase from config.json
  -ed <directory> <secret_phrase>: Encrypt folder with manually entered secret phrase
  -ddy <directory>: Decrypt folder using secret phrase from config.json
  -dd <directory> <secret_phrase>: Decrypt folder with manually entered secret phrase

Use Log:
  log: View operation log
  log -d: Clear operation log
------------------------------------------------------------------------------------------------------
```

### Шифрование строки

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

### Дешифровка строки

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

### Дешифровка файла

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

### Дешифровка директории

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