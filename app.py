import streamlit as st
import time
import engine_core
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_lottie import st_lottie
import requests

# 1. การตั้งค่าหน้าจอ
st.set_page_config(page_title="มหาเฮง ไซเบอร์", page_icon="⚡", layout="wide")

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

lottie_cyber = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_m6cu96.json")

if 'history' not in st.session_state:
    st.session_state.history = []

astrology_db = {
    "Monday": {"color": "เหลือง/ขาว", "bad": "แดง", "element": "ดิน", "direction": "ทิศตะวันออก"},
    "Tuesday": {"color": "ชมพู", "bad": "ขาว/เหลือง", "element": "ไฟ", "direction": "ทิศตะวันออกเฉียงใต้"},
    "Wednesday": {"color": "เขียว", "bad": "ชมพู", "element": "น้ำ", "direction": "ทิศใต้"},
    "Thursday": {"color": "ส้ม/ทอง", "bad": "ม่วง", "element": "ลม", "direction": "ทิศตะวันตก"},
    "Friday": {"color": "ฟ้า", "bad": "ดำ/เทา", "element": "น้ำ", "direction": "ทิศเหนือ"},
    "Saturday": {"color": "ม่วง/ดำ", "bad": "เขียว", "element": "ไฟ", "direction": "ทิศตะวันตกเฉียงใต้"},
    "Sunday": {"color": "แดง", "bad": "ฟ้า", "element": "ไฟ", "direction": "ทิศตะวันออกเฉียงเหนือ"}
}

# 2. ปรับแต่ง UI (Cyber-Oracle Thai Version)
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        color: #00f2ff;
    }
    
    .cyber-header {
        text-align: center;
        padding: 40px;
        border-bottom: 2px solid #00f2ff;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
        margin-bottom: 30px;
        background: rgba(0, 242, 255, 0.05);
    }
    .cyber-header h1 {
        font-family: 'Sarabun', sans-serif;
        color: #00f2ff !important;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #7b2ff7;
        font-size: 45px;
    }

    .cyber-card {
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid #00f2ff;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: inset 0 0 10px rgba(0, 242, 255, 0.1);
    }

    .lucky-number-display {
        font-size: 140px !important;
        font-weight: bold;
        color: #00f2ff;
        text-align: center;
        text-shadow: 0 0 30px #00f2ff;
        margin: 10px 0;
    }

    .stButton>button {
        background: transparent;
        color: #00f2ff !important;
        border: 2px solid #00f2ff !important;
        border-radius: 0px;
        font-weight: bold;
        font-family: 'Sarabun', sans-serif;
        letter-spacing: 2px;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }
    .stButton>button:hover {
        background: #00f2ff;
        color: black !important;
        box-shadow: 0 0 30px #00f2ff;
    }

    input, select, textarea {
        background-color: #111 !important;
        color: #00f2ff !important;
        border: 1px solid #00f2ff !important;
    }
    label { color: #00f2ff !important; font-family: 'Sarabun', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนหัว ---
st.markdown('<div class="cyber-header"><h1>[ ระบบมหาเฮง v1.0 ]</h1><p style="color:#7b2ff7;">สถานะระบบ: เชื่อมต่อฐานข้อมูลชะตาฟ้า... ออนไลน์</p></div>', unsafe_allow_html=True)

# 3. Layout
col1, col2, col3 = st.columns([1.3, 1.8, 1.2], gap="medium")

with col1:
    st.markdown("### 📡 ข้อมูลผู้ใช้งาน")
    user_name = st.text_input("ชื่อ-นามสกุล", value="", placeholder="ระบุตัวตนของคุณ...")
    
    birth_date = st.date_input("วัน/เดือน/ปีเกิด", value=datetime(2000, 1, 1))
    day_en = birth_date.strftime("%A")
    day_th_map = {
        "Monday": "จันทร์", "Tuesday": "อังคาร", "Wednesday": "พุธ",
        "Thursday": "พฤหัสบดี", "Friday": "ศุกร์", "Saturday": "เสาร์", "Sunday": "อาทิตย์"
    }
    day_th = day_th_map[day_en]
    u_data = astrology_db[day_en]
    
    st.markdown(f"""
    <div class="cyber-card">
        <p style="color:#7b2ff7; font-weight:bold;">> บันทึกดวงชะตา:</p>
        <p>• เกิดวัน: {day_th}</p>
        <p>• ธาตุหลัก: {u_data['element']}</p>
        <p>• สีที่ถูกโฉลก: {u_data['color']}</p>
        <p>• สีต้องห้าม: {u_data['bad']}</p>
        <p>• ทิศเปิดทรัพย์: {u_data['direction']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    dream = st.text_area("✍️ บันทึกนิมิต/ความฝัน", placeholder="กรอกรายละเอียดความฝันเพื่อเข้ารหัสตัวเลข...")

with col2:
    st.markdown("### 🔮 ระบบประมวลผลกลาง")
    user_seed = st.number_input("เลขจิตสัมผัส (0-999)", 0, 999, 168)
    
    if st.button("เริ่มการวิเคราะห์ดวงชะตา"):
        display_name = user_name if user_name else "บุคคลนิรนาม"
        with st.spinner('กำลังเข้ารหัสโชคลาภ...'):
            time.sleep(1.0)
            precise_seed = datetime.now().microsecond + birth_date.day
            lucky_num = engine_core.generate_lucky_number(user_seed + precise_seed)
            score = engine_core.calculate_score(lucky_num)
            
            st.session_state.history.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "num": f"{lucky_num:02d}", "score": score, "name": display_name
            })

            st.markdown(f"""
                <div class="cyber-card" style="text-align: center; border-color: #7b2ff7;">
                    <p style="color:#00f2ff;">ผลลัพธ์ดวงชะตาของ: {display_name}</p>
                    <div class="lucky-number-display">{lucky_num:02d}</div>
                    <p style="font-size: 20px;">ระดับความเฮง: <span style="color:#7b2ff7;">{score}%</span></p>
                </div>
            """, unsafe_allow_html=True)

            # กราฟ Radar ภาษาไทย
            fig = go.Figure(data=go.Scatterpolar(
                r=[score, 80, (lucky_num*9)%100, 95, 70],
                theta=['โชคลาภ', 'อำนาจ', 'การเงิน', 'สุขภาพ', 'เสน่ห์'],
                fill='toself', fillcolor='rgba(0, 242, 255, 0.1)',
                line=dict(color='#00f2ff', width=2)
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=False, range=[0, 100]), bgcolor="rgba(0,0,0,0)"),
                showlegend=False, paper_bgcolor="rgba(0,0,0,0)", height=350,
                font=dict(color="#00f2ff", family='Sarabun')
            )
            st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown("### 📜 ประวัติการวิเคราะห์")
    if st.session_state.history:
        for item in st.session_state.history[:6]:
            st.markdown(f"""
                <div class="cyber-card" style="padding:10px; border-color: rgba(0,242,255,0.3);">
                    <div style="display:flex; justify-content:space-between; font-size:10px; color:#7b2ff7;">
                        <span>[{item['time']}]</span>
                        <span>{item['score']}%</span>
                    </div>
                    <div style="font-size:25px; text-align:center; font-weight:bold; color:#fff;">
                        {item['num']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("ล้างประวัติข้อมูล"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("ยังไม่มีบันทึกข้อมูลในระบบ")

    if lottie_cyber:
        st_lottie(lottie_cyber, height=180)