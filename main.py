import sys
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from datetime import datetime
import os

def get_settings():
    """Чтение ключ-фразы из config.json"""
    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
        Password = data.get("Password", {})
        return Password.get("Secret_key")
    except FileNotFoundError:
        print("Error: файл config.json не найден.")
        sys.exit(1)


def encrypt_file(filepath, key):
    """Шифрует файл с использованием AES"""
    with open(filepath, "rb") as file:
        data = file.read()

    # Приводим ключ к длине 32 байта для AES-256
    key = key.encode('utf-8')
    key = key[:32].ljust(32, b'\0')  # Делаем ключ длиной 32 байта

    # Настройка шифрования
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    # Запись зашифрованных данных
    with open(filepath, "wb") as file:
        file.write(cipher.iv + encrypted_data)  # Записываем IV перед зашифрованными данными


def decrypt_file(filepath, key):
    """Расшифровывает файл с использованием AES"""
    with open(filepath, "rb") as file:
        data = file.read()

    # Приводим ключ к длине 32 байта для AES-256
    key = key.encode('utf-8')
    key = key[:32].ljust(32, b'\0')  # Делаем ключ длиной 32 байта

    # Извлекаем IV (первые 16 байт)
    iv = data[:AES.block_size]
    encrypted_data = data[AES.block_size:]

    # Настройка шифрования для расшифровки
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Расшифровка данных и удаление паддинга
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # Запись расшифрованных данных обратно в файл
    with open(filepath, "wb") as file:
        file.write(decrypted_data)


def encrypt_folder(folder_path, key):
    """Шифрует все файлы в папке и её подкаталогах"""
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Encrypting: {file_path}")
            try:
                encrypt_file(file_path, key)
            except Exception as e:
                print(f"Failed to encrypt {file_path}: {e}")


def decrypt_folder(folder_path, key):
    """Расшифровывает все файлы в папке и её подкаталогах"""
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Decrypting: {file_path}")
            try:
                decrypt_file(file_path, key)
            except Exception as e:
                print(f"Failed to decrypt {file_path}: {e}")


def write_space(filename):
    """Добавляет два переноса строки между записями в лог, если файл не пустой."""
    with open(filename, "r") as log_file:
        file_content = log_file.read()
        if file_content and not file_content.endswith("\n\n"):
            with open(filename, "a") as append_log:
                append_log.write("\n\n")


def log_operation(operation, details):
    """Функция для записи операций в лог."""
    with open("operations.log", "a") as log_file:
        write_space("operations.log")
        log_file.write(f"[{datetime.now()}]\nOperation Type: {operation}\n{details}")


def clear_log():
    """Очистка лог-файла"""
    with open("operations.log", "w") as log_file:
        log_file.write("")


def encode(data, secret_phrase):
    """Функция кодирования данных с использованием ключ-фразы"""
    key = secret_phrase.encode('utf-8')
    key = key[:32].ljust(32, b'\0')  # AES требует длину ключа 16, 24 или 32 байта
    
    # Используем фиксированный IV
    fixed_iv = b'\0' * 16  # Фиксированный вектор инициализации (небезопасно)
    
    cipher = AES.new(key, AES.MODE_CBC, iv=fixed_iv)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    encrypted_data = base64.b64encode(fixed_iv + ct_bytes).decode('utf-8')
    print(f"Encoded data: {encrypted_data}")
    log_operation("Encode", f"Data: {data}, Encrypted: {encrypted_data}")
    return encrypted_data

def decode(encrypted_data, secret_phrase):
    """Функция декодирования данных с использованием ключ-фразы"""
    key = secret_phrase.encode('utf-8')
    key = key[:32].ljust(32, b'\0')  # AES требует длину ключа 16, 24 или 32 байта
    
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    iv = encrypted_data_bytes[:AES.block_size]  # Извлекаем IV (хотя он фиксированный)
    ct = encrypted_data_bytes[AES.block_size:]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_data = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
        print(f"Decoded data: {decrypted_data}")
        log_operation("Decode", f"Encrypted: {encrypted_data}, Decrypted: {decrypted_data}")
        return decrypted_data
    except ValueError:
        error_msg = "Error: не удалось расшифровать данные. Проверьте ключ-фразу или шифрованные данные."
        print(error_msg)
        log_operation("Decode Error", error_msg)
        return None


def check_hash(hash_value, data, secret_phrase):
    """Проверка соответствия строки хэшу"""
    key = secret_phrase.encode('utf-8')
    key = key[:32].ljust(32, b'\0')  # AES требует длину ключа 16, 24 или 32 байта
    encrypted_data = base64.b64decode(hash_value)
    iv = encrypted_data[:AES.block_size]
    ct = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_data = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
        if decrypted_data == data:
            success_msg = f"Success: строка '{data}' соответствует хэшу '{hash_value}'."
            print(success_msg)
            log_operation("Check Hash", success_msg)
        else:
            error_msg = "Error: строка не соответствует хэшу."
            print(error_msg)
            log_operation("Check Hash Error", error_msg)
    except ValueError:
        error_msg = "Error: не удалось расшифровать данные. Проверьте ключ-фразу или хэш."
        print(error_msg)
        log_operation("Check Hash Error", error_msg)


def show_log():
    """Вывод лога операций"""
    try:
        with open("operations.log", "r") as log_file:
            print("\n---------------------------------------------Операции---------------------------------------------")
            print(log_file.read())
            print("--------------------------------------------------------------------------------------------------")
    except FileNotFoundError:
        print("Лог-файл отсутствует.")


def encrypt_folder(folder_path, key):
    """Encrypts all files in the folder and its subdirectories"""
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Encrypting: {file_path}")
            try:
                encrypt_file(file_path, key)
            except Exception as e:
                print(f"Failed to encrypt {file_path}: {e}")


def decrypt_folder(folder_path, key):
    """Decrypts all files in the folder and its subdirectories"""
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Decrypting: {file_path}")
            try:
                decrypt_file(file_path, key)
            except Exception as e:
                print(f"Failed to decrypt {file_path}: {e}")


def help_menu():
    print("""-------------------------------------------------Help-------------------------------------------------
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
------------------------------------------------------------------------------------------------------""")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1]:
            if "-h" in sys.argv[1]:
                help_menu()
                return
            
            # Шифрование файла
            if "-ef" in sys.argv[1]:
                if sys.argv[1] == "-efy":
                    if len(sys.argv) < 3:
                        print("Error: требуется указать имя файла для шифрования.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Error: ключ-фраза отсутствует в config.json.")
                        return
                    encrypt_file(sys.argv[2], secret_phrase)
                    print(f"Success: файл {sys.argv[2]} зашифрован.")
                    log_operation("Encrypt File", f"File {sys.argv[2]} encrypted using secret key from config.json.")
                elif sys.argv[1] == "-ef":
                    if len(sys.argv) < 4:
                        print("Error: требуется указать имя файла и ключ-фразу для шифрования.")
                        return
                    encrypt_file(sys.argv[2], sys.argv[3])
                    print(f"Success: файл {sys.argv[2]} зашифрован.")
                    log_operation("Encrypt File", f"File {sys.argv[2]} encrypted using provided secret key.")
                else:
                    print("Error: неизвестная команда для шифрования.")
                return

            # Расшифровка файла
            if "-df" in sys.argv[1]:
                if sys.argv[1] == "-dfy":
                    if len(sys.argv) < 3:
                        print("Error: требуется указать имя файла для расшифровки.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Error: ключ-фраза отсутствует в config.json.")
                        return
                    decrypt_file(sys.argv[2], secret_phrase)
                    print(f"Success: файл {sys.argv[2]} расшифрован.")
                    log_operation("Decrypt File", f"File {sys.argv[2]} decrypted using secret key from config.json.")
                elif sys.argv[1] == "-df":
                    if len(sys.argv) < 4:
                        print("Error: требуется указать имя файла и ключ-фразу для расшифровки.")
                        return
                    decrypt_file(sys.argv[2], sys.argv[3])
                    print(f"Success: файл {sys.argv[2]} расшифрован.")
                    log_operation("Decrypt File", f"File {sys.argv[2]} decrypted using provided secret key.")
                else:
                    print("Error: неизвестная команда для расшифровки.")
                return

            # Шифрование папки
            if "-ed" in sys.argv[1]:
                if sys.argv[1] == "-edy":
                    if len(sys.argv) < 3:
                        print("Error: требуется указать путь к папке для шифрования.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Error: ключ-фраза отсутствует в config.json.")
                        return
                    encrypt_folder(sys.argv[2], secret_phrase)
                    log_operation("Encrypt Folder", f"Folder {sys.argv[2]} encrypted using secret key from config.json.")
                elif sys.argv[1] == "-ed":
                    if len(sys.argv) < 4:
                        print("Error: требуется указать путь к папке и ключ-фразу для шифрования.")
                        return
                    encrypt_folder(sys.argv[2], sys.argv[3])
                    log_operation("Encrypt Folder", f"Folder {sys.argv[2]} encrypted using provided secret key.")
                else:
                    print("Error: неизвестная команда для шифрования папки.")
                return

            # Расшифровка папки
            if "dd" in sys.argv[1]:
                if sys.argv[1] == "-ddy":
                    if len(sys.argv) < 3:
                        print("Error: требуется указать путь к папке для расшифровки.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Error: ключ-фраза отсутствует в config.json.")
                        return
                    decrypt_folder(sys.argv[2], secret_phrase)
                    log_operation("Decrypt Folder", f"Folder {sys.argv[2]} decrypted using secret key from config.json.")
                elif sys.argv[1] == "-dd":
                    if len(sys.argv) < 4:
                        print("Error: требуется указать путь к папке и ключ-фразу для расшифровки.")
                        return
                    decrypt_folder(sys.argv[2], sys.argv[3])
                    log_operation("Decrypt Folder", f"Folder {sys.argv[2]} decrypted using provided secret key.")
                else:
                    print("Error: неизвестная команда для расшифровки папки.")
                return
            
            # Шифрование строки
            if "-e" in sys.argv[1]:
                if sys.argv[1] == "-ey":
                    if len(sys.argv) < 3:
                        print("Error: требуется указать данные для кодирования.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Error: ключ-фраза отсутствует в config.json.")
                        return
                    encode(sys.argv[2], secret_phrase)
                elif sys.argv[1] == "-e":
                    if len(sys.argv) < 4:
                        print("Error: требуется указать данные и ключ-фразу.")
                        return
                    encode(sys.argv[2], sys.argv[3])
                else:
                    print("Error: неизвестная команда для кодирования.")
                return
            
            # Расшифровка строки
            if "-d" in sys.argv[1]:
                if sys.argv[1] == "-dy":
                    if len(sys.argv) < 3:
                        print("Error: требуется указать данные для декодирования.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Error: ключ-фраза отсутствует в config.json.")
                        return
                    decode(sys.argv[2], secret_phrase)
                elif sys.argv[1] == "-d":
                    if len(sys.argv) < 4:
                        print("Error: требуется указать данные и ключ-фразу.")
                        return
                    decode(sys.argv[2], sys.argv[3])
                else:
                    print("Error: неизвестная команда для декодирования.")
                return
            
            # Проверка хэша
            if "-c" in sys.argv[1]:
                if sys.argv[1] == "-cy":
                    if len(sys.argv) < 4:
                        print("Error: требуется указать хэш и данные для проверки.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Error: ключ-фраза отсутствует в config.json.")
                        return
                    check_hash(sys.argv[2], sys.argv[3], secret_phrase)
                elif sys.argv[1] == "-c":
                    if len(sys.argv) < 5:
                        print("Error: требуется указать хэш, данные и ключ-фразу.")
                        return
                    check_hash(sys.argv[2], sys.argv[3], sys.argv[4])
                else:
                    print("Error: неизвестная команда для проверки соответствия хэшу.")
                return

            # Вывод и очистка лога
            if sys.argv[1] == "log":
                if len(sys.argv) > 2 and sys.argv[2] == "-d":
                    clear_log()
                    print("Лог-файл очищен.")
                else:
                    show_log()
                return
            print("Error: неизвестная команда.")
            return
    print("Error: команда не распознана!")


if __name__ == "__main__":
    main()