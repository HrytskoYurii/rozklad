import streamlit as st
import pandas as pd
from datetime import datetime

# Налаштування сторінки
st.set_page_config(page_title="УЗ Розклад", layout="wide")

# 1. Функція для автоматичного розрахунку стоянки
def get_stop_time(arr, dep):
    try:
        if not arr or not dep or arr == "—" or dep == "—":
            return ""
        t1 = datetime.strptime(arr.strip(), '%H:%M')
        t2 = datetime.strptime(dep.strip(), '%H:%M')
        delta = (t2 - t1).total_seconds() / 60
        if delta < 0: delta += 1440  # перехід через північ
        return str(int(delta)) if delta > 0 else ""
    except:
        return ""

# 2. Функція автоматичного перекладу (трансліт)
def to_translit(text):
    if not text: return ""
    ukr = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    eng = "abvh hdeiezhzyiiyk lmnoprstufkhts ch sh shch yu yaABVH HDEIEZHZYIIYK LMNOPRSTUFKHTS CH SH SHCH YU YA"
    # Спрощена логіка для надійності
    trans = str.maketrans(ukr, eng)
    return text.translate(trans)

st.title("🚉 Автоматичний генератор розкладу")

# Початкові дані
if 'main_df' not in st.session_state:
    st.session_state.main_df = pd.DataFrame(
        [["—", "", "18:38", "Одеса-Головна", "Odesa-Holovna", "08:38", "", "—"]],
        columns=["Приб.1", "Стоянка.1", "Відпр.1", "Станція", "Station", "Приб.2", "Стоянка.2", "Відпр.2"]
    )

# 3. Таблиця для введення даних
# Ми забороняємо редагувати Стоянку та Station, бо вони рахуються самі
edited_df = st.data_editor(
    st.session_state.main_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Стоянка.1": st.column_config.Column(disabled=True),
        "Стоянка.2": st.column_config.Column(disabled=True),
        "Station": st.column_config.Column(disabled=True),
    }
)

# АВТОМАТИЗАЦІЯ: Перерахунок при будь-якій зміні
if not edited_df.equals(st.session_state.main_df):
    for i, row in edited_df.iterrows():
        # Авто-переклад
        edited_df.at[i, "Station"] = to_translit(row["Станція"])
        # Авто-стоянка 1
        edited_df.at[i, "Стоянка.1"] = get_stop_time(row["Приб.1"], row["Відпр.1"])
        # Авто-стоянка 2
        edited_df.at[i, "Стоянка.2"] = get_stop_time(row["Приб.2"], row["Відпр.2"])
    
    st.session_state.main_df = edited_df
    st.rerun()

st.markdown("---")

# 4. ВІДОБРАЖЕННЯ ТАБЛИЦІ (точно як на фото)
# Використовуємо st.html для безпечного виводу без помилок
st.write("### Попередній перегляд (А4)")

html_layout = f"""
<div style="background-color: white; padding: 20px; color: black; font-family: Arial;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <div style="color: #1a1a60;">
            <div style="font-size: 32px; font-weight: bold;">Розклад руху</div>
            <div style="font-size: 20px;">Timetable</div>
        </div>
        <div style="font-size: 40px; font-weight: 900; color: #1a1a60; border-bottom: 5px solid #1a1a60;">УЗ</div>
    </div>

    <style>
        .uz-table {{ width: 100%; border-collapse: collapse; }}
        .uz-table th {{ background-color: #2e2e7a; color: white; border: 1px solid white; padding: 8px 2px; text-align: center; font-size: 13px; }}
        .uz-table th span {{ display: block; font-size: 9px; font-weight: normal; }}
        .uz-table td {{ border: 1px solid #333; padding: 5px; text-align: center; font-size: 12px; color: black; }}
        .st-bold {{ text-align: left; font-weight: bold; padding-left: 5px; }}
    </style>

    <table class="uz-table">
        <thead>
            <tr>
                <th>Приб.<span>Arrival</span></th>
                <th>Стоянка<span>Stop, min</span></th>
                <th>Відпр.<span>Departure</span></th>
                <th style="width: 25%;">Станція</th>
                <th style="width: 25%;">Station</th>
                <th>Приб.<span>Arrival</span></th>
                <th>Стоянка<span>Stop, min</span></th>
                <th>Відпр.<span>Departure</span></th>
            </tr>
        </thead>
        <tbody>
"""

for _, row in edited_df.iterrows():
    html_layout += f"""
        <tr>
            <td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td>
            <td class="st-bold">{row[3]}</td><td style="text-align:left; font-style:italic;">{row[4]}</td>
            <td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td>
        </tr>
    """

html_layout += "</tbody></table></div>"

# ВИКОРИСТОВУЄМО НОВИЙ МЕТОД STREAMLIT ДЛЯ HTML
st.html(html_layout)
