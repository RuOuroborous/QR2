import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import PIL.Image
import PIL.ImageTk
from backend import QRGenerator
from languages import LANGUAGES
import os
import platform
from datetime import datetime

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title(LANGUAGES['ru']['title'])
        self.root.geometry("480x540")  # Уменьшаем на 40% от 800x900
        
        # Определяем ОС и выбираем формат иконки
        system = platform.system()
        if system == "Windows":
            self.icon_path = os.path.join('icon', 'icona.ico')
        else:  # Linux или macOS
            self.icon_path = os.path.join('icon', 'icona.png')
        
        if os.path.exists(self.icon_path):
            try:
                icon = PIL.Image.open(self.icon_path)
                photo = PIL.ImageTk.PhotoImage(icon)
                self.root.iconphoto(True, photo)
            except Exception as e:
                print(f"Ошибка загрузки иконки: {e}")
        
        self.current_language = 'ru'
        self.generator = QRGenerator()
        
        # Создание меню
        self.create_menu()
        
        # Создание основного интерфейса
        self.create_widgets()
        
        # Применение текущего языка
        self.change_language(self.current_language)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Меню файл
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=LANGUAGES[self.current_language]['menu_save'], 
                            command=self.save_qr)
        file_menu.add_separator()
        file_menu.add_command(label=LANGUAGES[self.current_language]['menu_exit'], 
                            command=self.root.quit)
        menubar.add_cascade(label=LANGUAGES[self.current_language]['menu_file'], 
                          menu=file_menu)
        
        # Меню настроек
        settings_menu = tk.Menu(menubar, tearoff=0)
        
        # Подменю цветов
        colors_menu = tk.Menu(settings_menu, tearoff=0)
        colors_menu.add_command(label=LANGUAGES[self.current_language]['qr_color'], 
                              command=self.choose_qr_color)
        colors_menu.add_command(label=LANGUAGES[self.current_language]['bg_color'], 
                              command=self.choose_bg_color)
        settings_menu.add_cascade(label=LANGUAGES[self.current_language]['colors'], 
                                menu=colors_menu)
        
        # Подменю логотипа
        logo_menu = tk.Menu(settings_menu, tearoff=0)
        logo_menu.add_command(label=LANGUAGES[self.current_language]['add_logo'], 
                            command=self.add_logo)
        logo_menu.add_command(label=LANGUAGES[self.current_language]['remove_logo'], 
                            command=self.remove_logo)
        settings_menu.add_cascade(label=LANGUAGES[self.current_language]['logo'], 
                                menu=logo_menu)
        
        # Подменю типа QR-кода
        type_menu = tk.Menu(settings_menu, tearoff=0)
        type_menu.add_command(label=LANGUAGES[self.current_language]['type_text'], 
                            command=lambda: self.change_type('text'))
        type_menu.add_command(label=LANGUAGES[self.current_language]['type_wifi'], 
                            command=lambda: self.change_type('wifi'))
        type_menu.add_command(label=LANGUAGES[self.current_language]['type_location'], 
                            command=lambda: self.change_type('location'))
        settings_menu.add_cascade(label=LANGUAGES[self.current_language]['type'], 
                                menu=type_menu)
        
        # Подменю временных QR-кодов
        temp_menu = tk.Menu(settings_menu, tearoff=0)
        temp_menu.add_command(label=LANGUAGES[self.current_language]['temp_1h'], 
                            command=lambda: self.generate_temp_qr(60))
        temp_menu.add_command(label=LANGUAGES[self.current_language]['temp_24h'], 
                            command=lambda: self.generate_temp_qr(1440))
        temp_menu.add_command(label=LANGUAGES[self.current_language]['temp_7d'], 
                            command=lambda: self.generate_temp_qr(10080))
        settings_menu.add_cascade(label=LANGUAGES[self.current_language]['temp_qr'], 
                                menu=temp_menu)
        
        # Подменю истории
        history_menu = tk.Menu(settings_menu, tearoff=0)
        history_menu.add_command(label=LANGUAGES[self.current_language]['show_history'], 
                               command=self.show_history)
        history_menu.add_command(label=LANGUAGES[self.current_language]['clear_history'], 
                               command=self.clear_history)
        settings_menu.add_cascade(label=LANGUAGES[self.current_language]['history'], 
                                menu=history_menu)
        
        # Подменю шифрования
        encryption_menu = tk.Menu(settings_menu, tearoff=0)
        encryption_menu.add_command(label=LANGUAGES[self.current_language]['encrypt_qr'], 
                                  command=self.show_encryption_dialog)
        encryption_menu.add_command(label=LANGUAGES[self.current_language]['decrypt_qr'], 
                                  command=self.show_decryption_dialog)
        settings_menu.add_cascade(label=LANGUAGES[self.current_language]['encryption'], 
                                menu=encryption_menu)
        
        menubar.add_cascade(label=LANGUAGES[self.current_language]['menu_settings'], 
                          menu=settings_menu)
        
        # Меню языка
        language_menu = tk.Menu(menubar, tearoff=0)
        language_menu.add_command(label="Русский", 
                                command=lambda: self.change_language('ru'))
        language_menu.add_command(label="English", 
                                command=lambda: self.change_language('en'))
        language_menu.add_command(label="Español", 
                                command=lambda: self.change_language('es'))
        language_menu.add_command(label="Français", 
                                command=lambda: self.change_language('fr'))
        language_menu.add_command(label="Deutsch", 
                                command=lambda: self.change_language('de'))
        language_menu.add_command(label="中文", 
                                command=lambda: self.change_language('zh'))
        menubar.add_cascade(label=LANGUAGES[self.current_language]['menu_language'], 
                          menu=language_menu)
        
        self.root.config(menu=menubar)
    
    def create_widgets(self):
        # Создаем фрейм для кнопки "Вставить" и поля ввода
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=5)
        
        # Кнопка "Вставить"
        self.paste_button = ttk.Button(input_frame, text=LANGUAGES[self.current_language]['paste'],
                                     command=self.paste_text)
        self.paste_button.pack(side=tk.LEFT, padx=5)
        
        # Поле ввода с плейсхолдером
        self.text_entry = ttk.Entry(input_frame, width=30)
        self.text_entry.pack(side=tk.LEFT, padx=5)
        self.text_entry.insert(0, LANGUAGES[self.current_language]['enter_text'])
        self.text_entry.bind('<FocusIn>', self.on_entry_click)
        self.text_entry.bind('<FocusOut>', self.on_focus_out)
        
        self.generate_button = ttk.Button(self.root, text=LANGUAGES[self.current_language]['generate'], command=self.generate_qr)
        self.generate_button.pack(pady=5)
        
        self.qr_label = ttk.Label(self.root)
        self.qr_label.pack(pady=10)
    
    def on_entry_click(self, event):
        if self.text_entry.get() == LANGUAGES[self.current_language]['enter_text']:
            self.text_entry.delete(0, tk.END)
            self.text_entry.config(foreground='black')
    
    def on_focus_out(self, event):
        if not self.text_entry.get():
            self.text_entry.insert(0, LANGUAGES[self.current_language]['enter_text'])
            self.text_entry.config(foreground='gray')
    
    def paste_text(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, clipboard_text)
            self.text_entry.config(foreground='black')
        except:
            pass
    
    def show_encryption_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(LANGUAGES[self.current_language]['encrypt_title'])
        dialog.geometry("240x120")  # Уменьшаем на 40% от 400x200
        self.set_window_icon(dialog)
        
        ttk.Label(dialog, text=LANGUAGES[self.current_language]['encrypt_password']).pack(pady=5)
        password_entry = ttk.Entry(dialog, show="*", width=24)  # Уменьшаем ширину на 40%
        password_entry.pack(pady=5)
        
        def encrypt_and_generate():
            password = password_entry.get()
            if not password:
                messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                     LANGUAGES[self.current_language]['enter_password'])
                return
            
            text = self.text_entry.get()
            if not text or text == LANGUAGES[self.current_language]['enter_text']:
                messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                     LANGUAGES[self.current_language]['enter_text'])
                return
            
            img = self.generator.generate_qr(text, password=password)
            self.display_qr(img)
            dialog.destroy()
            messagebox.showinfo(LANGUAGES[self.current_language]['success'], 
                              LANGUAGES[self.current_language]['encrypt_success'])
        
        ttk.Button(dialog, text="OK", command=encrypt_and_generate).pack(pady=10)
    
    def show_decryption_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(LANGUAGES[self.current_language]['decrypt_title'])
        dialog.geometry("240x120")  # Уменьшаем на 40% от 400x200
        self.set_window_icon(dialog)
        
        ttk.Label(dialog, text=LANGUAGES[self.current_language]['decrypt_password']).pack(pady=5)
        password_entry = ttk.Entry(dialog, show="*", width=24)  # Уменьшаем ширину на 40%
        password_entry.pack(pady=5)
        
        def decrypt_text():
            password = password_entry.get()
            if not password:
                messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                     LANGUAGES[self.current_language]['enter_password'])
                return
            
            text = self.text_entry.get()
            if not text or text == LANGUAGES[self.current_language]['enter_text']:
                messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                     LANGUAGES[self.current_language]['enter_text'])
                return
            
            decrypted_text = self.generator.decrypt_data(text, password)
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, decrypted_text)
            self.text_entry.config(foreground='black')
            dialog.destroy()
            
            if decrypted_text.startswith("Неверный пароль"):
                messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                     decrypted_text)
            else:
                messagebox.showinfo(LANGUAGES[self.current_language]['success'], 
                                  LANGUAGES[self.current_language]['decrypt_success'])
        
        ttk.Button(dialog, text="OK", command=decrypt_text).pack(pady=10)
    
    def generate_temp_qr(self, minutes):
        text = self.text_entry.get()
        if not text:
            messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                 LANGUAGES[self.current_language]['enter_text'])
            return
        
        img = self.generator.generate_qr(text, expires_in=minutes)
        self.display_qr(img)
        messagebox.showinfo(LANGUAGES[self.current_language]['info'], 
                          LANGUAGES[self.current_language]['temp_qr_info'].format(minutes=minutes))
    
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title(LANGUAGES[self.current_language]['history_title'])
        history_window.geometry("480x360")  # Уменьшаем на 40% от 800x600
        self.set_window_icon(history_window)
        
        # Создаем таблицу
        columns = (LANGUAGES[self.current_language]['history_text'],
                  LANGUAGES[self.current_language]['history_type'],
                  LANGUAGES[self.current_language]['history_created'],
                  LANGUAGES[self.current_language]['history_expires'],
                  LANGUAGES[self.current_language]['history_encrypted'])
        tree = ttk.Treeview(history_window, columns=columns, show='headings')
        
        # Настраиваем заголовки
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=90)  # Уменьшаем ширину на 40% от 150
        
        # Добавляем данные
        for entry in self.generator.get_history():
            created = datetime.fromisoformat(entry['created_at']).strftime('%Y-%m-%d %H:%M')
            expires = (datetime.fromisoformat(entry['expires_at']).strftime('%Y-%m-%d %H:%M') 
                      if entry.get('expires_at') 
                      else LANGUAGES[self.current_language]['history_permanent'])
            encrypted = LANGUAGES[self.current_language]['yes'] if entry.get('encrypted') else LANGUAGES[self.current_language]['no']
            tree.insert('', 'end', values=(entry['text'], entry['type'], created, expires, encrypted))
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(history_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем элементы
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def clear_history(self):
        if messagebox.askyesno(LANGUAGES[self.current_language]['warning'], 
                              LANGUAGES[self.current_language]['history_clear_confirm']):
            self.generator.clear_history()
            messagebox.showinfo(LANGUAGES[self.current_language]['info'], 
                              LANGUAGES[self.current_language]['history_cleared'])
    
    def change_type(self, qr_type):
        self.generator.set_type(qr_type)
        if qr_type == 'wifi':
            self.show_wifi_dialog()
        elif qr_type == 'location':
            self.show_location_dialog()
    
    def generate_qr(self):
        text = self.text_entry.get()
        if not text or text == LANGUAGES[self.current_language]['enter_text']:
            messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                 LANGUAGES[self.current_language]['enter_text'])
            return
        
        img = self.generator.generate_qr(text)
        self.display_qr(img)
    
    def display_qr(self, img):
        # Изменяем размер изображения для отображения
        display_size = (240, 240)  # Уменьшаем на 40% от 400x400
        img_resized = img.resize(display_size, PIL.Image.Resampling.LANCZOS)
        
        # Конвертируем в формат для Tkinter
        photo = PIL.ImageTk.PhotoImage(img_resized)
        
        # Обновляем изображение
        self.qr_label.configure(image=photo)
        self.qr_label.image = photo
        self.current_image = img
    
    def save_qr(self):
        if not hasattr(self, 'current_image'):
            messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                 LANGUAGES[self.current_language]['enter_text'])
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialdir=self.generator.default_save_dir
        )
        
        if filename:
            saved_path = self.generator.save_qr(self.current_image, filename)
            messagebox.showinfo(LANGUAGES[self.current_language]['success'], 
                              f"QR-код сохранен в {saved_path}")
    
    def choose_qr_color(self):
        color = colorchooser.askcolor(title=LANGUAGES[self.current_language]['qr_color_title'])[1]
        if color:
            self.generator.set_colors(color, self.generator.bg_color)
            if hasattr(self, 'current_image'):
                self.generate_qr()
    
    def choose_bg_color(self):
        color = colorchooser.askcolor(title=LANGUAGES[self.current_language]['bg_color_title'])[1]
        if color:
            self.generator.set_colors(self.generator.qr_color, color)
            if hasattr(self, 'current_image'):
                self.generate_qr()
    
    def add_logo(self):
        logo_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if logo_path:
            self.generator.set_logo(logo_path)
            if hasattr(self, 'current_image'):
                self.generate_qr()
    
    def remove_logo(self):
        self.generator.set_logo(None)
        if hasattr(self, 'current_image'):
            self.generate_qr()
    
    def show_wifi_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(LANGUAGES[self.current_language]['wifi_title'])
        dialog.geometry("276x173")  # Увеличено на 15% от 240x150
        self.set_window_icon(dialog)
        
        ttk.Label(dialog, text=LANGUAGES[self.current_language]['wifi_ssid']).pack(pady=5)
        ssid_entry = ttk.Entry(dialog, width=24)
        ssid_entry.pack(pady=5)
        
        ttk.Label(dialog, text=LANGUAGES[self.current_language]['wifi_password']).pack(pady=5)
        password_entry = ttk.Entry(dialog, show="*", width=24)
        password_entry.pack(pady=5)
        
        def generate_wifi_qr():
            ssid = ssid_entry.get()
            password = password_entry.get()
            if not ssid or not password:
                messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                     LANGUAGES[self.current_language]['wifi_error'])
                return
            
            wifi_string = f"WIFI:S:{ssid};T:WPA;P:{password};;"
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, wifi_string)
            self.text_entry.config(foreground='black')
            dialog.destroy()
            self.generate_qr()
        
        ttk.Button(dialog, text="OK", command=generate_wifi_qr).pack(pady=10)
    
    def show_location_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(LANGUAGES[self.current_language]['location_title'])
        dialog.geometry("276x173")  # Увеличено на 15% от 240x150
        self.set_window_icon(dialog)
        
        ttk.Label(dialog, text=LANGUAGES[self.current_language]['location_lat']).pack(pady=5)
        lat_entry = ttk.Entry(dialog, width=24)
        lat_entry.pack(pady=5)
        
        ttk.Label(dialog, text=LANGUAGES[self.current_language]['location_lon']).pack(pady=5)
        lon_entry = ttk.Entry(dialog, width=24)
        lon_entry.pack(pady=5)
        
        def generate_location_qr():
            try:
                lat = float(lat_entry.get())
                lon = float(lon_entry.get())
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    raise ValueError
            except ValueError:
                messagebox.showwarning(LANGUAGES[self.current_language]['warning'], 
                                     LANGUAGES[self.current_language]['location_error'])
                return
            
            location_string = f"geo:{lat},{lon}"
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, location_string)
            self.text_entry.config(foreground='black')
            dialog.destroy()
            self.generate_qr()
        
        ttk.Button(dialog, text="OK", command=generate_location_qr).pack(pady=10)
    
    def change_language(self, lang):
        self.current_language = lang
        self.root.title(LANGUAGES[lang]['title'])
        self.generate_button.configure(text=LANGUAGES[lang]['generate'])
        self.paste_button.configure(text=LANGUAGES[lang]['paste'])
        
        # Обновляем плейсхолдер
        if self.text_entry.get() == LANGUAGES['ru' if lang == 'en' else 'en']['enter_text']:
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, LANGUAGES[lang]['enter_text'])
        
        # Обновляем меню
        for menu in self.root.winfo_children():
            if isinstance(menu, tk.Menu):
                self.root.config(menu=menu)
                break

    def set_window_icon(self, window):
        """Установка иконки для окна"""
        if os.path.exists(self.icon_path):
            try:
                icon = PIL.Image.open(self.icon_path)
                photo = PIL.ImageTk.PhotoImage(icon)
                window.iconphoto(True, photo)
            except Exception as e:
                print(f"Ошибка загрузки иконки: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRApp(root)
    root.mainloop()