# languages.py - Localization support

translations = {
    "en": {
        "window_title": "QR Code Generator",
        "content_label": "Content to encode:",
        "generate_button": "Generate QR Code",
        "save_button": "Save QR Code",
        "size_label": "QR Code Size:",
        "error_title": "Error",
        "error_empty": "Please enter content to encode",
        "save_title": "Save QR Code",
        "success_title": "Success",
        "success_message": "QR code saved successfully"
    },
    "ru": {
        "window_title": "Генератор QR кодов",
        "content_label": "Содержимое для кодирования:",
        "generate_button": "Сгенерировать QR код",
        "save_button": "Сохранить QR код",
        "size_label": "Размер QR кода:",
        "error_title": "Ошибка",
        "error_empty": "Пожалуйста, введите содержимое для кодирования",
        "save_title": "Сохранить QR код",
        "success_title": "Успех",
        "success_message": "QR код успешно сохранён"
    }
}

def get_translation(lang="en"):
    """Return translations for the selected language"""
    return translations.get(lang, translations["en"])