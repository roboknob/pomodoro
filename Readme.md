# 🍅 Pomodoro Timer (Python / Windows)

Десктопное приложение Pomodoro-таймера для Windows, написанное на Python.

Проект ориентирован на практическое использование:

- удобный UI
- системные уведомления
- сборка в самостоятельный `.exe`

---

## ✨ Возможности

- Таймер Pomodoro (работа / перерыв)
- Современный UI на **Tkinter + ttkbootstrap**
- Градиентный фон
- Системные уведомления Windows (**winotify**)
- Переключение светлой / тёмной темы
- Сборка в `.exe` через **PyInstaller**

---

## 📦 Структура проекта

Рекомендуемая структура:

```
PomadoroTimer/
├─ pomodoro.py
├─ bitcoin_astronaut.png
├─ bitcoin_astronaut.ico
├─ README.md
└─ .venv/              # виртуальное окружение (не коммитится)
```

### Назначение файлов

- `pomodoro.py` — основной код приложения
- `bitcoin_astronaut.png` — иконка **внутри приложения** (окно, уведомления)
- `bitcoin_astronaut.ico` — иконка **exe-файла**
- `README.md` — документация

---

## 🧰 Требования

- **Windows 10 / 11**
- **Python 3.14**
- PowerShell или терминал PyCharm

---

## 🔧 Установка зависимостей

Рекомендуется использовать виртуальное окружение.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install ttkbootstrap pyinstaller winotify
```

---

## 📁 Работа с ресурсами в собранном `.exe`

При сборке с `--onefile` все ресурсы (PNG и т.п.) распаковываются
во временную папку.  
Для корректной работы используется функция `resource_path`.

### Функция в коде

```python
def resource_path(relative: str) -> str:
    import sys, os
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)
```

### Использование

```python
tk.PhotoImage(file=resource_path("bitcoin_astronaut.png"))
```

И в `winotify`:

```python
icon = resource_path("bitcoin_astronaut.png")
```

---

## 🏗️ Сборка приложения в `.exe` (релиз)

### 1️⃣ Очистка старых сборок (рекомендуется всегда)

```powershell
Remove-Item -Recurse -Force .\build, .\dist -ErrorAction SilentlyContinue
Remove-Item .\Pomodoro.spec -ErrorAction SilentlyContinue
```

---

### 2️⃣ Сборка релизной версии (без консоли)

```powershell
pyinstaller --onefile --windowed --name PomodoroTimer `
  --icon .\bitcoin_astronaut.ico `
  --add-data "bitcoin_astronaut.png;." `
  pomodoro.py
```

После успешной сборки готовый файл будет здесь:

```
dist\PomodoroTimer.exe
```

---

## 🐞 Сборка для отладки (с консолью)

Если нужно увидеть ошибки или логи:

```powershell
Remove-Item -Recurse -Force .\build, .\dist -ErrorAction SilentlyContinue
Remove-Item .\Pomodoro.spec -ErrorAction SilentlyContinue

pyinstaller --onefile --name PomodoroTimerDebug `
  --icon .\bitcoin_astronaut.ico `
  --add-data "bitcoin_astronaut.png;." `
  pomodoro.py
```

Запуск:

```
dist\PomodoroTimerDebug.exe
```

---

## 🖼️ Иконки — важные правила

- **Иконка окна и уведомлений** → PNG
- **Иконка exe-файла** → **ТОЛЬКО `.ico`**

⚠️ PNG нельзя использовать как иконку exe.

Если иконка exe не обновляется:

- Windows кеширует иконки
- попробуй изменить `--name` (например `PomodoroTimerV2`)
- или перезапусти Проводник / систему

---

## 🔔 Уведомления Windows

Для стабильной работы уведомлений в собранном `.exe`
используется библиотека **winotify**.

Если уведомления:

- работают при запуске из PyCharm
- но не работают из exe

→ убедись, что используешь `winotify` и пересобери приложение.

---

## ❗ Частые проблемы

### Иконка exe осталась питоновской

- убедись, что `.ico` файл реально существует
- очисти `build/`, `dist/`, `.spec`
- переименуй exe (`--name`)
- Windows может кешировать иконки

### PNG не находится в exe

- в команде сборки должен быть `--add-data`
- в коде должен использоваться `resource_path()`

---

## 🚀 Готово

После сборки у тебя:

- полноценное Windows-приложение
- с UI, уведомлениями и иконкой
- не зависящее от установленного Python

---

## 🔜 Возможные улучшения

- автозапуск вместе с Windows
- трей-иконка
- установщик (Setup / MSI)
- статистика Pomodoro

Проект готов к дальнейшему развитию.