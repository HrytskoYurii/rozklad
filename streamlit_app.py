import streamlit as st
import pandas as pd

# Налаштування сторінки
st.set_page_config(page_title="УЗ Розклад", layout="wide")

# Словник для миттєвої транслітерації
def auto_translit(text):
    if not text or pd.isna(text): return ""
    ukr_to_eng = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 
        'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 
        'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '', 'Ю': 'Yu', 'Я': 'Ya',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 
        'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'yu', 'я': 'ya', '-': '-', ' ': ' '
    }
    return "".join(ukr_to_eng.get(c, c) for c in text)

# Ініціалізація даних з вашого PDF-файлу
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(
        [["", "", "18:38", "Одеса-Головна", "Odesa-Holovna", "08:38", "", ""]],
        columns=["Приб. (1)", "Стоянка (1)", "Відпр. (1)", "Станція", "Station", "Приб. (2)", "Стоянка (2)", "Відпр. (2)"]
    )

st.title("🚉 Генератор розкладу")

# 1. Редактор таблиці з автоматичним оновленням
edited_df = st.data_editor(st.session_state.data, num_rows="dynamic", use_container_width=True)

# ЛОГІКА АВТОМАТИЧНОГО ПЕРЕКЛАДУ:
# Якщо дані в колонці 'Станція' змінилися, оновлюємо 'Station' автоматично
if not edited_df.equals(st.session_state.data):
    edited_df['Station'] = edited_df['Станція'].apply(auto_translit)
    st.session_state.data = edited_df
    st.rerun()

st.markdown("---")

# 2. Формування макету з логотипом та синьою шапкою
html_output = f"""
<div style="width: 210mm; margin: auto; background: white; padding: 10px; color: black; font-family: Arial;">
    
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
            <div style="font-size: 42px; font-weight: bold; color: #1a1a60;">Розклад руху</div>
            <div style="font-size: 28px; color: #1a1a60;">Timetable</div>
        </div>
        <div style="font-size: 50px; font-weight: 900; color: #1a1a60; border-bottom: 8px solid #1a1a60;">УЗ</div>
    </div>

    <style>
        .uz-table {{ width: 100%; border-collapse: collapse; }}
        .uz-table th {{ 
            background-color: #2e2e7a; color: white; border: 1px solid white; 
            padding: 10px 2px; text-align: center; font-size: 14px; 
        }}
        .uz-table th span {{ display: block; font-size: 10px; font-weight: normal; }}
        .uz-table td {{ border: 1px solid #333; padding: 8px; text-align: center; font-size: 13px; }}
        .st-name {{ text-align: left; font-weight: bold; padding-left: 8px; }}
    </style>

    <table class="uz-table">
        <thead>
            <tr>
                <th>Приб.<span>Arrival</span></th>
                <th>Стоянка<span>Stop, min</span></th>
                <th>Відпр.<span>Departure</span></th>
                <th>Станція</th>
                <th>Station</th>
                <th>Приб.<span>Arrival</span></th>
                <th>Стоянка<span>Stop, min</span></th>
                <th>Відпр.<span>Departure</span></th>
            </tr>
        </thead>
        <tbody>
"""

for _, row in edited_df.iterrows():
    html_output += f"""
            <tr>
                <td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td>
                <td class="st-name">{row[3]}</td><td class="st-name" style="font-weight:normal; font-style:italic;">{row[4]}</td>
                <td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td>
            </tr>
    """

html_output += "</tbody></table></div>"

# Відображення HTML макету
st.markdown(html_output, unsafe_allow_html=True)
