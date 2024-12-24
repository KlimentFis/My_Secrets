import sys
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
from datetime import datetime

def get_settings():
    """Чтение ключ-фразы из config.json"""
    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
        Password = data.get("Password", {})
        return Password.get("Secret_key")
    except FileNotFoundError:
        print("Ошибка: файл config.json не найден.")
        sys.exit(1)

def log_operation(operation, details):
    """Функция для записи операций в лог"""
    with open("operations.log", "a") as log_file:
        log_file.write(f"[{datetime.now()}] \nOperation Type: {operation}\n{details}\n\n\n")

def clear_log():
    """Очистка лог-файла"""
    with open("operations.log", "w") as log_file:
        log_file.write("")

def encode(data, secret_phrase):
    """Функция кодирования данных с использованием ключ-фразы"""
    key = secret_phrase.encode('utf-8')
    key = key[:32].ljust(32, b'\0')  # AES требует длину ключа 16, 24 или 32 байта
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    encrypted_data = base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
    print(f"Encoded data: {encrypted_data}")
    log_operation("Encode", f"Data: {data}, Encrypted: {encrypted_data}")

def decode(encrypted_data, secret_phrase):
    """Функция декодирования данных с использованием ключ-фразы"""
    key = secret_phrase.encode('utf-8')
    key = key[:32].ljust(32, b'\0')  # AES требует длину ключа 16, 24 или 32 байта
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    iv = encrypted_data_bytes[:AES.block_size]
    ct = encrypted_data_bytes[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_data = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
        print(f"Decoded data: {decrypted_data}")
        log_operation("Decode", f"Encrypted: {encrypted_data}, Decrypted: {decrypted_data}")
    except ValueError:
        error_msg = "Ошибка: не удалось расшифровать данные. Проверьте ключ-фразу или шифрованные данные."
        print(error_msg)
        log_operation("Decode Error", error_msg)

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
        error_msg = "Ошибка: не удалось расшифровать данные. Проверьте ключ-фразу или хэш."
        print(error_msg)
        log_operation("Check Hash Error", error_msg)

def show_log():
    """Вывод лога операций"""
    try:
        with open("operations.log", "r") as log_file:
            print("\n---------------------------------------------Операции---------------------------------------------\n")
            print(log_file.read())
            print("--------------------------------------------------------------------------------------------------")
    except FileNotFoundError:
        print("Лог-файл отсутствует.")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1]:
            if "h" in sys.argv[1]:
                print("""
-------------------------------------------------Help-------------------------------------------------
Flags:
-h: Show help
-e: Encode (with optional secret phrase)
-d: Decode (with optional secret phrase)
-c: Check if string matches hash (with optional secret phrase)

Use Encode:
  -ey <data>: Encode using secret phrase from config.json
  -e <data> <secret_phrase>: Encode with manually entered secret phrase

Use Decode:
  -dy <data>: Decode using secret phrase from config.json
  -d <data> <secret_phrase>: Decode with manually entered secret phrase

Use Check:
  -cy <hash> <data>: Check if string matches hash using secret phrase from config.json
  -c <hash> <data> <secret_phrase>: Check if string matches hash with manually entered secret phrase

Use Log:
  log: View operation log
  log -d: Clear operation log
------------------------------------------------------------------------------------------------------
""")
                return
            if "e" in sys.argv[1]:
                if sys.argv[1] == "-ey":
                    if len(sys.argv) < 3:
                        print("Ошибка: требуется указать данные для кодирования.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Ошибка: ключ-фраза отсутствует в config.json.")
                        return
                    encode(sys.argv[2], secret_phrase)
                elif sys.argv[1] == "-e":
                    if len(sys.argv) < 4:
                        print("Ошибка: требуется указать данные и ключ-фразу.")
                        return
                    encode(sys.argv[2], sys.argv[3])
                else:
                    print("Ошибка: неизвестная команда для кодирования.")
                return
            if "d" in sys.argv[1]:
                if sys.argv[1] == "-dy":
                    if len(sys.argv) < 3:
                        print("Ошибка: требуется указать данные для декодирования.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Ошибка: ключ-фраза отсутствует в config.json.")
                        return
                    decode(sys.argv[2], secret_phrase)
                elif sys.argv[1] == "-d":
                    if len(sys.argv) < 4:
                        print("Ошибка: требуется указать данные и ключ-фразу.")
                        return
                    decode(sys.argv[2], sys.argv[3])
                else:
                    print("Ошибка: неизвестная команда для декодирования.")
                return
            if "c" in sys.argv[1]:
                if sys.argv[1] == "-cy":
                    if len(sys.argv) < 4:
                        print("Ошибка: требуется указать хэш и данные для проверки.")
                        return
                    secret_phrase = get_settings()
                    if not secret_phrase:
                        print("Ошибка: ключ-фраза отсутствует в config.json.")
                        return
                    check_hash(sys.argv[2], sys.argv[3], secret_phrase)
                elif sys.argv[1] == "-c":
                    if len(sys.argv) < 5:
                        print("Ошибка: требуется указать хэш, данные и ключ-фразу.")
                        return
                    check_hash(sys.argv[2], sys.argv[3], sys.argv[4])
                else:
                    print("Ошибка: неизвестная команда для проверки соответствия хэшу.")
                return
            if sys.argv[1] == "log":
                if len(sys.argv) > 2 and sys.argv[2] == "-d":
                    clear_log()
                    print("Лог-файл очищен.")
                else:
                    show_log()
                return
            print("Ошибка: неизвестная команда.")
            return
    print("Ошибка: введите данные!")

if __name__ == "__main__":
    main()