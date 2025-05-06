# QR-код генератор

Приложение для генерации QR-кодов с поддержкой шифрования и мультиязычности.

## Возможности

- Генерация QR-кодов из текста
- Шифрование QR-кодов
- Поддержка Wi-Fi QR-кодов
- Поддержка геолокации
- Мультиязычный интерфейс
- Настройка цветов QR-кода
- Добавление логотипа
- Временные QR-коды
- История генерации

## Поддерживаемые платформы

- Windows
- Linux
- macOS

## Установка

1. Установите Poetry, если он еще не установлен:
```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -
```

2. Клонируйте репозиторий:
```bash
git clone https://github.com/RuOuroborous/QR2.git
cd QR2
```

3. Установите зависимости с помощью Poetry:
```bash
poetry install
```

## Использование

1. Запустите приложение:
```bash
poetry run python frontend.py
```

2. Введите текст в поле ввода
3. Нажмите кнопку "Сгенерировать" или используйте меню для дополнительных функций

## Требования

- Python 3.8 или выше
- Poetry
- Pillow
- qrcode
- cryptography

## Примечания для разных ОС

### Windows
- Иконка приложения должна быть в формате `.ico`
- Файл иконки должен находиться в папке `icon/icona.ico`

### Linux/macOS
- Иконка приложения должна быть в формате `.png`
- Файл иконки должен находиться в папке `icon/icona.png`
- Убедитесь, что у вас установлены необходимые системные зависимости для работы с GUI:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  ```
- Все пути к файлам чувствительны к регистру 