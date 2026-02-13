import streamlit as st
import pandas as pd

# Налаштування сторінки
st.set_page_config(page_title="UZ Timetable Generator", layout="wide")

# Функція транслітерації для автоматичного заповнення Station
def translit(text):
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

st.title("📋 Генератор розкладу руху")

# Створюємо початкову таблицю з 8 колонками як на вашому макеті
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(
        [["", "", "", "Одеса-Головна", "Odesa-Holovna", "", "", ""]],
        columns=["Приб.1", "Стоянка.1", "Відпр.1", "Станція", "Station", "Приб.2", "Стоянка.2", "Відпр.2"]
    )

st.subheader("1. Введіть дані")
# Редактор таблиці
edited_df = st.data_editor(st.session_state.df if 'df' in st.session_state else st.session_state.data, 
                           num_rows="dynamic", use_container_width=True)

# Кнопка для автозаповнення Station
if st.button("🔄 Оновити Station (трансліт)"):
    edited_df['Station'] = edited_df['Станція'].apply(translit)
    st.session_state.df = edited_df
    st.rerun()

st.markdown("---")
st.subheader("2. Попередній перегляд (А4)")

# Формування HTML-таблиці з синьою шапкою як на фото
html_table = f"""
<style>
    .uz-table {{ width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; }}
    .uz-table thead th {{ 
        background-color: #2e2e7a; color: white; border: 1px solid white; 
        padding: 10px 5px; text-align: center; font-size: 14px; 
    }}
    .uz-table thead th span {{ display: block; font-size: 10px; font-weight: normal; margin-top: 2px; }}
    .uz-table td {{ border: 1px solid #333; padding: 8px; text-align: center; font-size: 13px; }}
    .st-name {{ text-align: left; font-weight: bold; padding-left: 10px; }}
    .st-eng {{ text-align: left; font-style: italic; color: #444; padding-left: 10px; }}
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
    html_table += f"""
        <tr>
            <td>{row[0] if row[0] else ''}</td><td>{row[1] if row[1] else ''}</td><td>{row[2] if row[2] else ''}</td>
            <td class="st-name">{row[3] if row[3] else ''}</td><td class="st-eng">{row[4] if row[4] else ''}</td>
            <td>{row[5] if row[5] else ''}</td><td>{row[6] if row[6] else ''}</td><td>{row[7] if row[7] else ''}</td>
        </tr>
    """

html_table += "</tbody></table>"

# Використовуємо правильний параметр для відображення HTML
st.markdown(html_table, unsafe_allow_html=True)
