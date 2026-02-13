import sys
import os
import tkinter as tk
from tkinter import messagebox

try:
    from plyer import notification
except Exception:
    notification = None

import ttkbootstrap as tb


def resource_path(relative):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


class PomodoroApp(tb.Window):
    def __init__(self):
        # Темы
        self.light_theme = "flatly"
        self.dark_theme = "darkly"
        self.is_dark = False

        super().__init__(themename=self.light_theme)

        # Окно
        self.title("Pomodoro")
        self.geometry("600x420")
        self.minsize(520, 360)

        # Иконка (PNG)
        self.app_icon = tk.PhotoImage(file=resource_path("bitcoin_astronaut.png"))
        self.iconphoto(False, self.app_icon)

        # Фон-градиент (Canvas)
        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Дебаунс перерисовки фона при ресайзе
        self._bg_after = None
        self.bind("<Configure>", self._on_resize)

        # Логика таймера
        self.work_min = 25
        self.break_min = 5

        self.is_running = False
        self.is_work = True

        self.phase_total_seconds = self.work_min * 60
        self.remaining_seconds = self.phase_total_seconds
        self.after_id = None

        # Grid корня
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)

        # UI
        self._build_ui()

        # Поднимаем UI поверх canvas (canvas всегда будет самым нижним)
        self._lift_ui()

        # Стартовый рендер
        self._apply_progress_style()
        self._render_time()
        self._render_progress()
        self.update_background()

    # ---------- Z-ORDER ----------
    def _lift_ui(self):
        # поднимаем фреймы поверх canvas
        for w in (self.header, self.timer_card, self.settings, self.buttons):
            w.lift()

    # ---------- BACKGROUND ----------
    def _on_resize(self, event):
        if self._bg_after:
            self.after_cancel(self._bg_after)
        self._bg_after = self.after(60, self._redraw_everything_after_resize)

    def _redraw_everything_after_resize(self):
        self.update_background()
        self._lift_ui()

    def draw_gradient(self, canvas, color1, color2):
        canvas.delete("gradient")
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        r1, g1, b1 = self.winfo_rgb(color1)
        r2, g2, b2 = self.winfo_rgb(color2)

        r_ratio = (r2 - r1) / height
        g_ratio = (g2 - g1) / height
        b_ratio = (b2 - b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr // 256:02x}{ng // 256:02x}{nb // 256:02x}"
            canvas.create_line(0, i, width, i, tags=("gradient",), fill=color)

        # опускаем слой градиента внутри canvas
        canvas.tag_lower("gradient")

    def update_background(self):
        if self.is_dark:
            self.draw_gradient(self.bg_canvas, "#1e1e2f", "#2b2b45")
        else:
            self.draw_gradient(self.bg_canvas, "#f7f9fc", "#dce3f0")

    # ---------- UI ----------
    def _build_ui(self):
        self.header = tb.Frame(self, padding=16)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=0)

        self.status_label = tb.Label(self.header, text="Фокусировка", font=("Segoe UI", 16), anchor="center")
        self.status_label.grid(row=0, column=0, sticky="ew")

        self.theme_btn = tb.Button(
            self.header,
            text="",
            bootstyle="secondary",
            width=4,
            command=self.toggle_theme
        )
        self.theme_btn.grid(row=0, column=1, padx=(10, 0))
        self._sync_theme_button_icon()

        self.timer_card = tb.Frame(self, padding=18, bootstyle="secondary")
        self.timer_card.grid(row=1, column=0, padx=16, pady=12, sticky="nsew")
        self.timer_card.columnconfigure(0, weight=1)
        self.timer_card.rowconfigure(0, weight=4)
        self.timer_card.rowconfigure(1, weight=0)

        self.time_label = tb.Label(
            self.timer_card,
            text="25:00",
            font=("Segoe UI", 56, "bold"),
            anchor="center"
        )
        self.time_label.grid(row=0, column=0, sticky="nsew")

        self.progress = tb.Progressbar(
            self.timer_card,
            maximum=100,
            value=0
        )
        self.progress.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        self.settings = tb.Frame(self, padding=(16, 0, 16, 0))
        self.settings.grid(row=2, column=0, sticky="ew")
        for c in range(6):
            self.settings.columnconfigure(c, weight=1)

        tb.Label(self.settings, text="Работа (мин):").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.work_var = tk.IntVar(value=self.work_min)
        tb.Spinbox(self.settings, from_=1, to=180, textvariable=self.work_var, width=6, bootstyle="info").grid(
            row=0, column=1, sticky="w", padx=6, pady=6
        )

        tb.Label(self.settings, text="Перерыв (мин):").grid(row=0, column=2, sticky="e", padx=6, pady=6)
        self.break_var = tk.IntVar(value=self.break_min)
        tb.Spinbox(self.settings, from_=1, to=60, textvariable=self.break_var, width=6, bootstyle="info").grid(
            row=0, column=3, sticky="w", padx=6, pady=6
        )

        self.apply_btn = tb.Button(
            self.settings,
            text="⚙️ Применить",
            bootstyle="secondary-outline",
            command=self.apply_settings
        )
        self.apply_btn.grid(row=0, column=4, columnspan=2, sticky="ew", padx=6, pady=6)

        self.buttons = tb.Frame(self, padding=16)
        self.buttons.grid(row=3, column=0, sticky="ew")
        for c in range(3):
            self.buttons.columnconfigure(c, weight=1)

        self.start_btn = tb.Button(self.buttons, text="▶ Старт", command=self.start, bootstyle="success")
        self.start_btn.grid(row=0, column=0, padx=6, sticky="ew")

        self.pause_btn = tb.Button(self.buttons, text="⏸ Пауза", command=self.pause, bootstyle="warning",
                                   state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=6, sticky="ew")

        self.reset_btn = tb.Button(self.buttons, text="↻ Сброс", command=self.reset, bootstyle="danger-outline")
        self.reset_btn.grid(row=0, column=2, padx=6, sticky="ew")

        # Хоткеи
        self.bind("<space>", lambda e: self.pause() if self.is_running else self.start())
        self.bind("<Escape>", lambda e: self.reset())
        self.bind("t", lambda e: self.toggle_theme())

    def _sync_theme_button_icon(self):
        # Кнопка показывает действие: что включим
        self.theme_btn.config(text="☀️" if self.is_dark else "🌙")

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        new_theme = self.dark_theme if self.is_dark else self.light_theme
        self.style.theme_use(new_theme)

        self._sync_theme_button_icon()
        self._apply_progress_style()
        self.update_background()
        self._lift_ui()

    def _apply_progress_style(self):
        if self.is_work:
            self.progress.configure(bootstyle="success-striped")
        else:
            self.progress.configure(bootstyle="info-striped")

    # ---------- LOGIC ----------
    def _notify(self, title, message):
        # 1) Win11 toast через winotify (обычно надежнее)
        try:
            from winotify import Notification, audio

            toast = Notification(
                app_id="PomodoroTimer",  # важно: стабильный AppID
                title=title,
                msg=message,
                icon=resource_path("bitcoin_astronaut.png")  # если добавляешь через --add-data
            )
            toast.set_audio(audio.Default, loop=False)
            toast.show()
            return
        except Exception:
            pass

        # 2) Fail-safe: звук + модальное окно
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception:
            pass

        try:
            messagebox.showinfo(title, message)
        except Exception:
            pass

    def apply_settings(self):
        try:
            self.work_min = int(self.work_var.get())
            self.break_min = int(self.break_var.get())
        except ValueError:
            # если ввели что-то странное — просто игнорируем
            self.work_var.set(str(self.work_min))
            self.break_var.set(str(self.break_min))
            return

        if self.work_min < 1:
            self.work_min = 1
            self.work_var.set("1")

        if self.break_min < 1:
            self.break_min = 1
            self.break_var.set("1")

        if not self.is_running:
            new_total = (self.work_min if self.is_work else self.break_min) * 60
            self.phase_total_seconds = new_total
            self.remaining_seconds = min(self.remaining_seconds, new_total)
            self._render_time()
            self._render_progress()

    def _render_time(self):
        m = self.remaining_seconds // 60
        s = self.remaining_seconds % 60
        self.time_label.config(text=f"{m:02d}:{s:02d}")
        self.status_label.config(text="Работа" if self.is_work else "Перерыв")

    def _render_progress(self):
        if self.phase_total_seconds <= 0:
            self.progress.configure(value=0)
            return
        done = self.phase_total_seconds - self.remaining_seconds
        pct = (done / self.phase_total_seconds) * 100
        pct = max(0, min(100, pct))
        self.progress.configure(value=pct)

    def _tick(self):
        if not self.is_running:
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self._render_time()
            self._render_progress()
            self.after_id = self.after(1000, self._tick)
            return

        self.is_work = not self.is_work
        self.apply_settings()

        self.phase_total_seconds = (self.work_min if self.is_work else self.break_min) * 60
        self.remaining_seconds = self.phase_total_seconds

        self._apply_progress_style()
        self._render_time()
        self._render_progress()

        if self.is_work:
            self._notify("Pomodoro", "Перерыв закончился. Время работать.")
        else:
            self._notify("Pomodoro", "Помодоро завершён. Время отдохнуть.")

        self.after_id = self.after(1000, self._tick)

    def start(self):
        if self.is_running:
            return

        self.apply_settings()
        if self.remaining_seconds <= 0:
            self.phase_total_seconds = (self.work_min if self.is_work else self.break_min) * 60
            self.remaining_seconds = self.phase_total_seconds

        self.is_running = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")

        self._apply_progress_style()
        self._tick()

    def pause(self):
        self.is_running = False
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")

        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

    def reset(self):
        self.pause()
        self.is_work = True
        self.apply_settings()

        self.phase_total_seconds = self.work_min * 60
        self.remaining_seconds = self.phase_total_seconds

        self._apply_progress_style()
        self._render_time()
        self._render_progress()


if __name__ == "__main__":
    PomodoroApp().mainloop()
