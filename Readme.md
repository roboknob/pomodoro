# Pomodoro Timer (Python / Windows)

Десктопное приложение Pomodoro-таймера для Windows, написанное на Python с использованием:
- Tkinter + ttkbootstrap (UI)
- градиентного фона
- системных уведомлений Windows (winotify)
- сборки в `.exe` через PyInstaller

---

## 📦 Структура проекта

Рекомендуемая структура:

PomadoroTimer/
├─ pomodoro.py
├─ bitcoin_astronaut.png
├─ bitcoin_astronaut.ico
├─ README.md
└─ .venv/ (виртуальное окружение)


Копировать код

### Назначение файлов
- `pomodoro.py` — основной код приложения
- `bitcoin_astronaut.png` — иконка **внутри приложения** (окно, уведомления)
- `bitcoin_astronaut.ico` — иконка **самого exe-файла**
- `README.md` — эта инструкция

---

## 🧰 Требования

- Windows 10 / 11  
- Python (3.14)
- PowerShell или терминал PyCharm

---

## 🔧 Установка зависимостей

Рекомендуется работать в виртуальном окружении.

```powershell
 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install ttkbootstrap pyinstaller winotify
📁 Работа с ресурсами в собранном exe
При сборке с --onefile файлы (png и др.) распаковываются во временную папку.
Поэтому в коде используется функция:


Копировать код
def resource_path(relative: str) -> str:
    import sys, os
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)
Использование:


Копировать код
tk.PhotoImage(file=resource_path("bitcoin_astronaut.png"))
И в winotify:


Копировать код
icon=resource_path("bitcoin_astronaut.png")
🏗️ Сборка приложения в .exe (релиз)
1️⃣ Очистка старых сборок (рекомендуется всегда)
powershell
Копировать код
Remove-Item -Recurse -Force .\build, .\dist -ErrorAction SilentlyContinue
Remove-Item .\Pomodoro.spec -ErrorAction SilentlyContinue
2️⃣ Сборка релизной версии (без консоли)
powershell
Копировать код
pyinstaller --onefile --windowed --name PomodoroTimer `
  --icon .\bitcoin_astronaut.ico `
  --add-data "bitcoin_astronaut.png;." `
  pomodoro.py
После успешной сборки готовый файл будет здесь:

Копировать код
dist\PomodoroTimer.exe
🐞 Сборка для отладки (с консолью)
Если нужно увидеть ошибки или логи:

powershell
Копировать код
Remove-Item -Recurse -Force .\build, .\dist -ErrorAction SilentlyContinue
Remove-Item .\Pomodoro.spec -ErrorAction SilentlyContinue

pyinstaller --onefile --name PomodoroTimerDebug `
  --icon .\bitcoin_astronaut.ico `
  --add-data "bitcoin_astronaut.png;." `
  pomodoro.py
Запускать:

Копировать код
dist\PomodoroTimerDebug.exe
🖼️ Иконки: важные правила
Иконка окна / уведомлений → PNG

Иконка exe-файла → ТОЛЬКО .ico

PNG нельзя использовать как иконку exe.

Если иконка exe не обновляется:

Windows кеширует иконки

попробуй изменить --name (например PomodoroTimerV2)

или перезапусти Проводник / систему

🔔 Уведомления Windows
Для стабильной работы в собранном .exe используется библиотека winotify.

Если уведомления:

работают из PyCharm

но не работают из exe

→ обязательно используй winotify и пересобери приложение.

❗ Частые проблемы
Иконка exe осталась питоновской
Убедись, что .ico файл реально существует

Очисти build/, dist/, .spec

Переименуй exe (--name)

Windows может кешировать иконку

PNG не находится в exe
В команде сборки должен быть --add-data

В коде должен использоваться resource_path()

🚀 Готово
После сборки у тебя:

полноценное Windows-приложение

с UI, уведомлениями и иконкой

не зависящее от установленного Python

🔜 Возможные улучшения (по желанию)
автозапуск вместе с Windows

трей-иконка

установщик (Setup / MSI)

статистика Pomodoro

Проект готов к дальнейшему развитию.


Копировать код

---

Если хочешь, следующим шагом можем:
- привести README к **публичному GitHub-стилю**
- или сделать **короткую версию для пользователя**
- или добавить раздел *“как обновлять версию”*

Ты очень аккуратно довёл проект до состояния “настоящего приложения” — это редкость 👍