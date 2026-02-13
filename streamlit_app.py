import streamlit as st
import pandas as pd

# Налаштування сторінки
st.set_page_config(page_title="UZ Timetable", layout="wide")

# Функція для автоматичного перекладу назв станцій
def translit_ukr_to_eng(text):
    if not text: return ""
    dic = {
        'А':'A','Б':'B','В':'V','Г':'H','Ґ':'G','Д':'D','Е':'E','Є':'Ye','Ж':'Zh','З':'Z','И':'Y','І':'I','Ї':'Yi','Й':'Y',
        'К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'Kh','Ц':'Ts','Ч':'Ch',
        'Ш':'Sh','Щ':'Shch','Ь':'','Ю':'Yu','Я':'Ya','а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ye','ж':'zh',
        'з':'z','и':'y','і':'i','ї':'yi','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t',
        'у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch','ь':'','ю':'yu','я':'ya'
    }
    return "".join([dic.get(c, c) for c in text])

st.title("🚉 Генератор розкладу руху")

# Створення структури таблиці (8 колонок як на фото)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(
        [["", "", "", "Одеса", "", "", "", ""]], 
        columns=["Приб.1", "Стоянка.1", "Відпр.1", "Станція", "Station", "Приб.2", "Стоянка.2", "Відпр.2"]
    )

st.subheader("1. Введіть дані")
# Редактор таблиці
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)

# Автоматичне оновлення колонки Station
if st.button("🔄 Оновити Station (трансліт)"):
    edited_df['Station'] = edited_df['Станція'].apply(translit_ukr_to_eng)
    st.session_state.df = edited_df
    st.rerun()

st.markdown("---")
st.subheader("2. Попередній перегляд (А4)")

# HTML/CSS макет точно за вашим фото
html_table = f"""
<style>
    .print-container {{ width: 210mm; background: white; padding: 10px; margin: auto; }}
    .uz-table {{ width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; }}
    .uz-table th {{ 
        background-color: #2e2e7a; color: white; border: 1px solid white; 
        padding: 8px 4px; text-align: center; font-size: 14px; line-height: 1.2;
    }}
    .uz-table th span {{ display: block; font-size: 11px; font-weight: normal; }}
    .uz-table td {{ border: 1px solid #333; padding: 6px; text-align: center; font-size: 13px; }}
    .st-name {{ text-align: left; font-weight: bold; padding-left: 10px; }}
    @media print {{ .no-print {{ display: none; }} }}
</style>

<div class="print-container">
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
            <td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td>
            <td class="st-name">{row[3]}</td><td class="st-name" style="font-weight:normal; font-style:italic;">{row[4]}</td>
            <td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td>
        </tr>
    """

html_table += "</tbody></table></div>"

# ВИПРАВЛЕНО: параметр unsafe_allow_html=True
st.markdown(html_table, unsafe_allow_html=True)

st.info("💡 Для друку натисніть Ctrl+P та оберіть 'Зберегти як PDF'. Не забудьте ввімкнути 'Фонову графіку'.")
