import qrcode
from PIL import Image, ImageDraw
import os
import json
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class QRGenerator:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        self.qr_color = "#000000"
        self.bg_color = "#FFFFFF"
        self.logo_path = None
        self.qr_type = 'text'
        self.default_save_dir = os.path.join(os.path.expanduser("~"), "QR_Codes")
        self.history_file = os.path.join(self.default_save_dir, "history.json")
        self._ensure_save_dir()
        self._load_history()
        self._clean_expired_codes()
        self.encryption_key = None
    
    def _ensure_save_dir(self):
        if not os.path.exists(self.default_save_dir):
            os.makedirs(self.default_save_dir, exist_ok=True)
    
    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = []
        else:
            self.history = []
    
    def _save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def _clean_expired_codes(self):
        now = datetime.now()
        self.history = [entry for entry in self.history 
                       if not entry.get('expires_at') or 
                       datetime.fromisoformat(entry['expires_at']) > now]
        self._save_history()
    
    def set_type(self, qr_type):
        self.qr_type = qr_type
    
    def set_colors(self, qr_color, bg_color):
        self.qr_color = qr_color
        self.bg_color = bg_color
    
    def set_logo(self, logo_path):
        self.logo_path = logo_path
    
    def _generate_encryption_key(self, password):
        # Генерируем ключ из пароля
        salt = b'QR_Code_Salt'  # В реальном приложении соль должна быть уникальной
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)
    
    def encrypt_data(self, data, password):
        if not password:
            return data
        f = self._generate_encryption_key(password)
        encrypted_data = f.encrypt(data.encode())
        return f"ENC:{encrypted_data.decode()}"
    
    def decrypt_data(self, encrypted_data, password):
        if not encrypted_data.startswith("ENC:"):
            return encrypted_data
        if not password:
            return "Требуется пароль для расшифровки"
        try:
            f = self._generate_encryption_key(password)
            decrypted_data = f.decrypt(encrypted_data[4:].encode())
            return decrypted_data.decode()
        except:
            return "Неверный пароль"
    
    def generate_qr(self, text, expires_in=None, password=None):
        # Форматируем текст в зависимости от типа QR-кода
        if self.qr_type == 'wifi':
            formatted_text = text
        elif self.qr_type == 'location':
            formatted_text = text
        else:
            formatted_text = text
        
        # Шифруем данные, если указан пароль
        if password:
            formatted_text = self.encrypt_data(formatted_text, password)
        
        self.qr.clear()
        self.qr.add_data(formatted_text)
        self.qr.make(fit=True)
        
        img = self.qr.make_image(fill_color=self.qr_color, back_color=self.bg_color)
        
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo = Image.open(self.logo_path)
                logo_size = (img.size[0] // 4, img.size[1] // 4)
                logo = logo.resize(logo_size, Image.Resampling.LANCZOS)
                pos = ((img.size[0] - logo.size[0]) // 2,
                      (img.size[1] - logo.size[1]) // 2)
                img.paste(logo, pos)
            except Exception as e:
                print(f"Ошибка при добавлении логотипа: {e}")
        
        # Сохраняем в историю
        entry = {
            'text': text,
            'type': self.qr_type,
            'created_at': datetime.now().isoformat(),
            'encrypted': bool(password)
        }
        
        if expires_in:
            entry['expires_at'] = (datetime.now() + timedelta(minutes=expires_in)).isoformat()
        
        self.history.append(entry)
        self._save_history()
        
        return img
    
    def save_qr(self, img, filename):
        # Если путь относительный, сохраняем в папку по умолчанию
        if not os.path.isabs(filename):
            filename = os.path.join(self.default_save_dir, filename)
        
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        img.save(filename)
        return filename
    
    def get_history(self):
        return self.history
    
    def clear_history(self):
        self.history = []
        self._save_history()