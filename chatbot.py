import tkinter as tk
from tkinter import ttk, scrolledtext

# --- Налаштування кольорів і стилю ---
BG_COLOR = "#fefefe"
BOT_COLOR = "#e9f5ff"
USER_COLOR = "#dfffdc"
FONT = ("Segoe UI", 12)

# --- Функція відповідей ---
def get_bot_response(user_input, state):
    user_input = user_input.strip().lower()
    response = ""
    next_state = state

    if state == "start":
        if user_input == "так":
            response = "Пацієнт має тільки АНН, чи кропив’янку/АНН? (введіть: кропив’янка або АНН)"
            next_state = "path_choice"
        else:
            response = "➡️ Спочатку потрібно виключити провокуючі фактори."
            next_state = "end"

    elif state == "path_choice":
        if "кроп" in user_input:
            response = "Чи тривають симптоми понад 6 тижнів? (так/ні)"
            next_state = "urticaria_duration"
        elif "анн" in user_input:
            response = "Чи приймає пацієнт інгібітори АПФ? (так/ні)"
            next_state = "ann_apf"
        else:
            response = "⚠️ Введіть 'кропив’янка' або 'АНН'"

    elif state == "urticaria_duration":
        if user_input == "так":
            response = "Чи є супутня аутоімунна патологія? (так/ні)"
            next_state = "urticaria_autoimmune"
        else:
            response = "➡️ Ймовірна гостра кропив’янка."
            next_state = "end"

    elif state == "urticaria_autoimmune":
        response = "Чи є позитивний BHRA або BAT тест? (так/ні)"
        next_state = "bhra"

    elif state == "bhra":
        if user_input == "так":
            response = "Чи наявні ≥1 маркер (ASST+, IgG-anti-FcεRI/IgE+, ↓IgE, ↑IgG-anti-TPO, ↓IgA, базопенія, еозинопенія)? (так/ні)"
            next_state = "markers"
        else:
            response = "➡️ Type IIb aiCSU малоймовірний. Краща відповідь на антигістамінні та омалізумаб."
            next_state = "end"

    elif state == "markers":
        if user_input == "так":
            response = "➡️ Type IIb aiCSU ймовірний. Погана відповідь на антигістамінні та омалізумаб, добра відповідь на циклоспорин."
        else:
            response = "➡️ Type IIb aiCSU можливий. Переглянути через 6–12 місяців."
        next_state = "end"

    elif state == "ann_apf":
        if user_input == "так":
            response = "➡️ Можлива асоціація з інгібітором АПФ."
            next_state = "end"
        else:
            response = "Чи знижений рівень C4? (так/ні)"
            next_state = "c4"

    elif state == "c4":
        if user_input == "так":
            response = "Чи знижений рівень C1-інгібітора? (так/ні)"
            next_state = "c1"
        else:
            response = "➡️ Можлива ідіопатична ангіоедема."
            next_state = "end"

    elif state == "c1":
        if user_input == "так":
            response = "➡️ Можлива спадкова ангіоедема."
        else:
            response = "➡️ Можлива набута ангіоедема (C1-інгібітор)."
        next_state = "end"

    return response, next_state

# --- Головний GUI ---
def launch_gui():
    window = tk.Tk()
    window.title("Діагностичний бот: Хронічна кропив’янка / АНН")
    window.configure(bg=BG_COLOR)

    style = ttk.Style()
    style.configure("TButton", font=FONT, padding=6)
    style.configure("TEntry", font=FONT)

    chat = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=30, font=FONT, bg=BG_COLOR)
    chat.pack(padx=15, pady=10)
    chat.insert(tk.END, "🤖 Бот: 🔍 Діагностика ХК/АНН\nЧи виключено всі відомі провокуючі фактори? (так/ні)\n")
    chat.config(state='disabled')

    entry = tk.Entry(window, font=FONT, width=50)
    entry.pack(padx=10, pady=5)

    state = {"step": "start"}

    def send():
        user_input = entry.get().strip()
        if not user_input:
            return
        entry.delete(0, tk.END)

        chat.config(state='normal')
        chat.insert(tk.END, f"\n👤 Ви: {user_input}\n", 'user')
        response, next_step = get_bot_response(user_input, state["step"])
        chat.insert(tk.END, f"🤖 Бот: {response}\n", 'bot')
        chat.config(state='disabled')
        chat.see(tk.END)

        state["step"] = next_step

    entry.bind("<Return>", lambda e: send())
    send_button = ttk.Button(window, text="Надіслати", command=send)
    send_button.pack(pady=10)

    window.mainloop()

# --- Запуск ---
if __name__ == "__main__":
    launch_gui()
