import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="УЗ Розклад", layout="wide")

# Функція для обчислення стоянки
def calc_stop(arr, dep):
    try:
        if not arr or not dep or arr in ["—", "-"] or dep in ["—", "-"]:
            return ""
        t1 = datetime.strptime(str(arr).strip(), '%H:%M')
        t2 = datetime.strptime(str(dep).strip(), '%H:%M')
        diff = (t2 - t1).total_seconds() / 60
        if diff < 0: diff += 1440
        return str(int(diff)) if diff > 0 else ""
    except:
        return ""

# Надійна функція транслітерації (виправляє помилку ValueError)
def auto_translate(text):
    if not text or pd.isna(text): return ""
    tr = {'А':'A','Б':'B','В':'V','Г':'H','Ґ':'G','Д':'D','Е':'E','Є':'Ye','Ж':'Zh','З':'Z','И':'Y','І':'I','Ї':'Yi','Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'Kh','Ц':'Ts','Ч':'Ch','Ш':'Sh','Щ':'Shch','Ь':'','Ю':'Yu','Я':'Ya','а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ye','ж':'zh','з':'z','и':'y','і':'i','ї':'yi','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch','ь':'','ю':'yu','я':'ya'}
    return "".join([tr.get(c, c) for c in str(text)])

st.title("🚉 Автоматичний генератор розкладу")

if 'main_data' not in st.session_state:
    st.session_state.main_data = pd.DataFrame(
        [["—", "", "18:38", "Одеса-Головна", "Odesa-Holovna", "08:38", "", "—"]],
        columns=["Приб.1", "Стоянка.1", "Відпр.1", "Станція", "Station", "Приб.2", "Стоянка.2", "Відпр.2"]
    )

# Редактор таблиці: Стоянка та Station заблоковані для вводу
edited_df = st.data_editor(
    st.session_state.main_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Стоянка.1": st.column_config.Column(disabled=True),
        "Стоянка.2": st.column_config.Column(disabled=True),
        "Station": st.column_config.Column(disabled=True),
    }
)

# АВТОМАТИЗАЦІЯ
if not edited_df.equals(st.session_state.main_data):
    for i, row in edited_df.iterrows():
        edited_df.at[i, "Station"] = auto_translate(row["Станція"])
        edited_df.at[i, "Стоянка.1"] = calc_stop(row["Приб.1"], row["Відпр.1"])
        edited_df.at[i, "Стоянка.2"] = calc_stop(row["Приб.2"], row["Відпр.2"])
    st.session_state.main_data = edited_df
    st.rerun()

st.markdown("---")

# Візуальний макет (точно як на фото)
html_code = f"""
<div style="background: white; padding: 20px; font-family: Arial; color: black; border-radius: 10px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <div style="color: #1a1a60;">
            <div style="font-size: 36px; font-weight: bold;">Розклад руху</div>
            <div style="font-size: 24px;">Timetable</div>
        </div>
        <div style="font-size: 45px; font-weight: 900; color: #1a1a60; border-bottom: 6px solid #1a1a60;">УЗ</div>
    </div>
    <style>
        .uz-t {{ width: 100%; border-collapse: collapse; }}
        .uz-t th {{ background-color: #2e2e7a; color: white; border: 1px solid white; padding: 10px 2px; text-align: center; font-size: 14px; }}
        .uz-t th span {{ display: block; font-size: 10px; font-weight: normal; }}
        .uz-t td {{ border: 1px solid #333; padding: 8px; text-align: center; font-size: 13px; color: black; }}
    </style>
    <table class="uz-t">
        <thead>
            <tr>
                <th>Приб.<span>Arrival</span></th><th>Стоянка<span>Stop, min</span></th><th>Відпр.<span>Departure</span></th>
                <th style="width:25%">Станція</th><th style="width:25%">Station</th>
                <th>Приб.<span>Arrival</span></th><th>Стоянка<span>Stop, min</span></th><th>Відпр.<span>Departure</span></th>
            </tr>
        </thead>
        <tbody>
"""
for _, r in edited_df.iterrows():
    html_code += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td style='text-align:left;font-weight:bold;'>{r[3]}</td><td style='text-align:left;font-style:italic;'>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td><td>{r[7]}</td></tr>"

html_code += "</tbody></table></div>"
st.html(html_code)
