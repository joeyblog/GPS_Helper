import tkinter as tk
from tkinter import scrolledtext
import gps_helper
from tkinter import scrolledtext, ttk
import pokesearch



def parse_and_display():
    input_text = text_box.get("1.0", tk.END)
    pokemon_data = pokesearch.parse(input_text)

    # 結果を表示
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)

    for idx, pokemon in enumerate(pokemon_data, start=1):
        print(pokemon)
        result_text.insert(tk.END, f"Pokemon {idx}\n")
        result_text.insert(tk.END, f"Name: {pokemon['name']} {gender_icon(pokemon['gender'])}{shiny_icon(pokemon['can_be_shiny'])}\n")
        result_text.insert(tk.END, f"IV: {pokemon['iv']} CP: {pokemon['cp']} Lv: {pokemon['lv']}\n")
        result_text.insert(tk.END, f"Despawn: {pokemon['despawn']}\n")
        result_text.insert(tk.END, f"Location: {pokemon['location']}\n")
        result_text.insert(tk.END, f"Coordinate: {pokemon['coord']['raw']}\n")
        result_text.insert(tk.END, f"Teleport: ")
        teleport_button = tk.Button(
            result_text,
            text="Teleport",
            command=lambda coord=pokemon['coord']: gps_helper.teleport(coord['lat'], coord['lon'])
        )
        result_text.window_create(tk.END, window=teleport_button)
        result_text.insert(tk.END, "\n\n")

    result_text.config(state=tk.DISABLED)

def gender_icon(gender):
    if gender == 'male':
        return '♂️'
    elif gender == 'female':
        return '♀️'
    else:
        return ''

def shiny_icon(can_be_shiny):
    if can_be_shiny:
        return '✨'
    else:
        return ''

def teleport_selected():
    selected_text = result_text.get("sel.first", "sel.last")
    if selected_text:
        lat, lon = map(float, selected_text.split(","))
        gps_helper.teleport(lat, lon)

# GUIの構築
window = tk.Tk()
window.title("Pokemon Info Parser")

# テーマの設定
style = ttk.Style()
style.theme_use("clam")  # "clam" は比較的モダンな外観です

# テキストボックス
text_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10, font=("Helvetica", 10))
text_box.grid(column=0, row=0, padx=10, pady=10)

# パースボタン
parse_button = ttk.Button(window, text="Parse", command=parse_and_display)
parse_button.grid(column=0, row=1, pady=5, sticky="w")

# 結果表示エリア
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=20, state=tk.DISABLED, font=("Helvetica", 10))
result_text.grid(column=0, row=2, padx=10, pady=10)


window.mainloop()
