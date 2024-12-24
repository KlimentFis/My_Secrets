import sys
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

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

def encode(data, secret_phrase):
    """Функция кодирования данных с использованием ключ-фразы"""
    key = secret_phrase.encode('utf-8')
    key = key[:32].ljust(32, b'\0')  # AES требует длину ключа 16, 24 или 32 байта
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    encrypted_data = base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
    print(f"Encoded data: {encrypted_data}")

def decode(encrypted_data, secret_phrase):
    """Функция декодирования данных с использованием ключ-фразы"""
    key = secret_phrase.encode('utf-8')
    key = key[:32].ljust(32, b'\0')  # AES требует длину ключа 16, 24 или 32 байта
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:AES.block_size]
    ct = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_data = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
        print(f"Decoded data: {decrypted_data}")
    except ValueError:
        print("Ошибка: не удалось расшифровать данные. Проверьте ключ-фразу или шифрованные данные.")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1]:
            if "h" in sys.argv[1]:
                print("""
Help:
-h: Show help
-e: Encode (with optional secret phrase)
-d: Decode (with optional secret phrase)

Use Encode:
  -ey <data>: Encode using secret phrase from config.json
  -e <data> <secret_phrase>: Encode with manually entered secret phrase

Use Decode:
  -dy <data>: Decode using secret phrase from config.json
  -d <data> <secret_phrase>: Decode with manually entered secret phrase
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
            print("Ошибка: неизвестная команда.")
            return
    print("Ошибка: введите данные!")

if __name__ == "__main__":
    main()
