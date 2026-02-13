import streamlit as st
import pandas as pd

# Налаштування сторінки
st.set_page_config(page_title="UZ Generator", layout="wide")

def translit(text):
    symbols = str.maketrans(
        "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя",
        "ABVHHDEIEZHZYIIYK LMNOPRSTUFKHTS CH SH SHCH YU YA abvhhdeiezhzyiiyk lmnoprstufkhts ch sh shch yu ya"
    )
    return text.translate(symbols)

st.write("### 🚉 Генератор розкладу руху")

# Створення початкових даних (8 колонок згідно з фото)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(
        [["", "", "", "", "", "", "", ""]],
        columns=["Приб.1", "Стоянка.1", "Відпр.1", "Станція", "Station", "Приб.2", "Стоянка.2", "Відпр.2"]
    )

# Інтерфейс редагування
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)

# Кнопка для авто-перекладу
if st.button("🔄 Оновити Station (Auto-translate)"):
    edited_df['Station'] = edited_df['Станція'].apply(translit)
    st.session_state.df = edited_df
    st.rerun()

# HTML макет для друку А4 (стиль вашого фото)
st.markdown("---")
st.write("#### Попередній перегляд (А4)")

html_content = f"""
<style>
    @media print {{
        .no-print {{ display: none; }}
        @page {{ size: A4; margin: 10mm; }}
    }}
    .uz-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: 'Segoe UI', Arial, sans-serif;
    }}
    .uz-table th {{
        background-color: #2e2e7a;
        color: white;
        border: 1px solid white;
        padding: 10px 5px;
        text-align: center;
        font-size: 14px;
    }}
    .uz-table th span {{
        display: block;
        font-size: 11px;
        font-weight: normal;
        opacity: 0.9;
    }}
    .uz-table td {{
        border: 1px solid #333;
        padding: 8px;
        text-align: center;
        font-size: 13px;
    }}
    .st-ukr {{ text-align: left; font-weight: bold; }}
    .st-eng {{ text-align: left; font-style: italic; color: #444; }}
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
    html_content += f"""
        <tr>
            <td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td>
            <td class="st-ukr">{row[3]}</td><td class="st-eng">{row[4]}</td>
            <td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td>
        </tr>
    """

html_content += "</tbody></table>"

st.markdown(html_content, unsafe_allow_content_allowed=True)
