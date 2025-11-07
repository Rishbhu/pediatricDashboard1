# app.py
import streamlit as st
import datetime as dt
import math

st.set_page_config(page_title="Pediatric Dashboard", layout="wide")

# ----------------- GLOBAL CSS -----------------
st.markdown("""
<style>
/* Remove Streamlit chrome + tighten spacing */
header[data-testid="stHeader"]{display:none !important;}
#MainMenu, footer{visibility:hidden !important;}
.block-container{padding-top:6px !important; max-width:1320px;}

/* Theme (high contrast) */
:root{
  --bg:#F6EFEF; --panel:#FBECEC; --border:#E1C1C3; --ink:#1b1e28;
  --pill:#EAF3FF; --pillborder:#C7DBFF; --hover:#EEF4FF; --selected:#FFE7EC;
}
[data-testid="stAppViewContainer"]{background:var(--bg);}
h1,h2,h3,h4,p,div,span{color:var(--ink);}

/* Cards & layout bits */
.card{background:#fff;border:2px solid var(--border);border-radius:16px;padding:12px 14px;box-shadow:0 2px 0 #f6d8da inset;margin-bottom:12px;}
.pinkpanel{background:var(--panel);border:2px solid #e8c7cf;border-radius:10px;overflow:hidden;}
.headerpink{background:#f7c8d8;border-bottom:2px solid #eab2c6;padding:10px 14px;font-weight:900;text-align:center;}
.pill-blue{display:inline-block;padding:6px 14px;border-radius:999px;background:#d6e7ff;border:1px solid #bcd6ff;font-weight:900;}
.iconrow{display:flex;gap:14px;justify-content:center;padding:12px 0 6px;}
.iconbox, .iconbox2, .iconbox3{
  width:70px;height:70px;display:flex;align-items:center;justify-content:center;border-radius:12px;font-size:36px;
}
.iconbox{border:2px solid #E7B6C0;background:#FFD7E2;}
.iconbox2{border:2px solid #F0C994;background:#FFE8C6;}
.iconbox3{border:2px solid #B6D7FF;background:#D0E9FF;}
.sel{ outline:3px solid #3B82F6; box-shadow:0 0 0 2px #93C5FD inset; }

.right{text-align:right;} .center{text-align:center;} .red{color:#C6002A;font-weight:900;}

/* Timeline */
.timelinewrap{padding:12px;}
.vert{position:relative;height:520px;margin:0 24px;}
.vert:before{content:"";position:absolute;left:50%;top:18px;bottom:18px;width:2px;background:#111;transform:translateX(-50%);}
.vert:after{content:"";position:absolute;left:40px;right:40px;top:6px;height:2px;background:#111;}
.hbot{position:absolute;left:40px;right:40px;bottom:6px;height:2px;background:#111;}
.tick{position:absolute;left:50%;transform:translateX(-50%);}
.tick .dot{position:absolute;left:-4px;top:-4px;width:8px;height:8px;background:#111;border-radius:50%;}
.tick .lbl{position:absolute;left:20px;top:-10px;width:230px;font-weight:700;}

/* Event-look boxes */
.eventbox{border:2px solid var(--border);border-radius:16px;padding:12px;background:#fff;box-shadow:0 2px 0 #f6d8da inset;}
.eventtitle{font-weight:900;margin:10px 0 6px;}
.addbtn{display:inline-block;background:#fff;border:2px solid var(--border);border-radius:999px;padding:8px 20px;font-weight:900;box-shadow:0 2px 0 #f6d8da inset;}

/* ===== DROPDOWN STYLES - DARK THEME WITH RED BORDERS ===== */
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div{
  background:#1A1A1A !important; 
  background-color:#1A1A1A !important; 
  color:#FFFFFF !important; 
  border-color:#333333 !important;
  min-height:44px; 
  font-weight:800; 
  border-width:2px !important;
  border-style:solid !important;
}
.stSelectbox div[data-baseweb="select"] > div:focus,
.stSelectbox div[data-baseweb="select"] > div:focus-within,
.stMultiSelect div[data-baseweb="select"] > div:focus,
.stMultiSelect div[data-baseweb="select"] > div:focus-within,
.stSelectbox div[data-baseweb="select"][aria-expanded="true"] > div,
.stMultiSelect div[data-baseweb="select"][aria-expanded="true"] > div{
  border-color:#FF0000 !important;
}
/* When popover is open, highlight the parent select */
div[data-baseweb="popover"]:not([style*="display: none"]) ~ * .stSelectbox div[data-baseweb="select"] > div,
div[data-baseweb="popover"]:not([style*="display: none"]) ~ * .stMultiSelect div[data-baseweb="select"] > div{
  border-color:#FF0000 !important;
}
.stSelectbox svg, .stMultiSelect svg{ 
  fill:#FFFFFF !important; 
  color:#FFFFFF !important; 
}
div[data-baseweb="select"] input{ 
  color:#FFFFFF !important; 
  font-weight:800; 
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
}
div[data-baseweb="select"] input::placeholder{ 
  color:#B0B0B0 !important; 
}

/* Dropdown menu popover - DARK BACKGROUND */
div[data-baseweb="popover"]{ 
  z-index: 9999 !important; 
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
}
div[data-baseweb="popover"] > div{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
}
div[data-baseweb="menu"]{
  background:#1A1A1A !important; 
  background-color:#1A1A1A !important;
  color:#FFFFFF !important; 
  border:1px solid #333333 !important;
  border-radius:8px !important; 
  box-shadow:0 12px 30px rgba(0,0,0,0.5) !important;
}
div[data-baseweb="menu"] ul{ 
  background:#1A1A1A !important; 
  background-color:#1A1A1A !important;
  padding:6px !important; 
}
div[data-baseweb="menu"] li, 
div[data-baseweb="menu"] [role="option"],
div[data-baseweb="menu"] > ul > li,
div[data-baseweb="menu"] ul li{
  background:#1A1A1A !important; 
  background-color:#1A1A1A !important;
  color:#FFFFFF !important; 
  font-weight:900 !important;
  font-size:15px !important; 
  padding:10px 12px !important; 
  border-radius:6px !important;
  border:1px solid transparent !important;
}
div[data-baseweb="menu"] li:hover, 
div[data-baseweb="menu"] [role="option"]:hover,
div[data-baseweb="menu"] > ul > li:hover,
div[data-baseweb="menu"] ul li:hover{
  background:#2A2A2A !important; 
  background-color:#2A2A2A !important;
  color:#FFFFFF !important;
}
div[data-baseweb="menu"] li[aria-selected="true"], 
div[data-baseweb="menu"] [role="option"][aria-selected="true"],
div[data-baseweb="menu"] > ul > li[aria-selected="true"],
div[data-baseweb="menu"] ul li[aria-selected="true"]{
  background:#333333 !important; 
  background-color:#333333 !important;
  color:#FFFFFF !important; 
  border:2px solid #FF0000 !important;
}

/* Force text color in dropdown options - override ALL nested elements */
div[data-baseweb="menu"] li *,
div[data-baseweb="menu"] [role="option"] *,
div[data-baseweb="menu"] span,
div[data-baseweb="menu"] div,
div[data-baseweb="menu"] p,
div[data-baseweb="menu"] li span,
div[data-baseweb="menu"] li div{
  color:#FFFFFF !important;
}

/* Override any light theme styles on popover children */
div[data-baseweb="popover"] > div{
  background-color:#1A1A1A !important;
}
div[data-baseweb="popover"] ul{
  background-color:#1A1A1A !important;
}
div[data-baseweb="popover"] li:not(:hover):not([aria-selected="true"]){
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
}

/* Target BaseWeb select dropdown specifically */
[data-baseweb="select"] [role="listbox"],
[data-baseweb="select"] [role="option"]{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
}

/* Multiselect tags */
.stMultiSelect [data-baseweb="tag"]{
  background:#333333 !important; 
  background-color:#333333 !important;
  color:#FFFFFF !important; 
  border:1px solid #FF0000 !important;
  border-radius:12px !important; 
  font-weight:900 !important;
}

/* ===== DATE INPUT - DARK THEME WITH RED BORDERS ===== */
.stDateInput > div > div,
.stDateInput div[data-baseweb="input"]{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
  border-color:#333333 !important;
  border-width:2px !important;
  border-style:solid !important;
  min-height:44px !important;
  font-weight:800 !important;
}
.stDateInput > div > div:focus,
.stDateInput > div > div:focus-within,
.stDateInput div[data-baseweb="input"]:focus,
.stDateInput div[data-baseweb="input"]:focus-within{
  border-color:#FF0000 !important;
}
.stDateInput input{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
  font-weight:800 !important;
}
.stDateInput svg{
  fill:#FFFFFF !important;
  color:#FFFFFF !important;
}

/* Date picker calendar popup - DARK THEME */
div[data-baseweb="popover"][id*="date"],
div[data-baseweb="popover"] [role="dialog"]{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  border:1px solid #333333 !important;
  border-radius:8px !important;
  box-shadow:0 12px 30px rgba(0,0,0,0.5) !important;
}
div[data-baseweb="popover"][id*="date"] *,
div[data-baseweb="popover"] [role="dialog"] *{
  color:#FFFFFF !important;
}
div[data-baseweb="popover"][id*="date"] [role="gridcell"],
div[data-baseweb="popover"] [role="dialog"] [role="gridcell"]{
  background:#1A1A1A !important;
  color:#FFFFFF !important;
}
div[data-baseweb="popover"][id*="date"] [role="gridcell"]:hover,
div[data-baseweb="popover"] [role="dialog"] [role="gridcell"]:hover{
  background:#2A2A2A !important;
  color:#FFFFFF !important;
}
div[data-baseweb="popover"][id*="date"] [role="gridcell"][aria-selected="true"],
div[data-baseweb="popover"] [role="dialog"] [role="gridcell"][aria-selected="true"]{
  background:#333333 !important;
  color:#FFFFFF !important;
  border:2px solid #FF0000 !important;
}

/* ===== NUMBER INPUT - DARK THEME WITH RED BORDERS ===== */
.stNumberInput > div > div,
.stNumberInput div[data-baseweb="input"]{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
  border-color:#333333 !important;
  border-width:2px !important;
  border-style:solid !important;
  min-height:44px !important;
  font-weight:800 !important;
}
.stNumberInput > div > div:focus,
.stNumberInput > div > div:focus-within,
.stNumberInput div[data-baseweb="input"]:focus,
.stNumberInput div[data-baseweb="input"]:focus-within{
  border-color:#FF0000 !important;
}
.stNumberInput input{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
  font-weight:800 !important;
}
.stNumberInput button{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
  border-color:#333333 !important;
}
.stNumberInput button:hover{
  background:#2A2A2A !important;
  background-color:#2A2A2A !important;
}
.stNumberInput svg{
  fill:#FFFFFF !important;
  color:#FFFFFF !important;
}

/* ===== TEXT AREA - DARK THEME WITH RED BORDERS ===== */
.stTextArea > div > div > textarea,
.stTextArea textarea{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
  border:2px solid #333333 !important;
  border-radius:8px !important;
  font-weight:800 !important;
  padding:10px 12px !important;
}
.stTextArea textarea:focus{
  border-color:#FF0000 !important;
  outline:none !important;
}
.stTextArea textarea::placeholder{
  color:#B0B0B0 !important;
}

/* ===== TOGGLE - DARK THEME ===== */
.stToggle label{
  color:#FFFFFF !important;
  font-weight:900 !important;
}
.stToggle [data-baseweb="switch"]{
  background:#333333 !important;
}
.stToggle [data-baseweb="switch"][aria-checked="true"]{
  background:#FF0000 !important;
}

/* ===== ALL INPUT FIELDS - DARK THEME UNIFIED BASE STYLES ===== */
.stTextInput > div > div > input,
.stTextInput input{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
  border:2px solid #333333 !important;
  border-radius:8px !important;
  min-height:44px !important;
  font-weight:800 !important;
  padding:10px 12px !important;
}
.stTextInput input:focus{
  border-color:#FF0000 !important;
  outline:none !important;
}
.stTextInput input::placeholder{
  color:#B0B0B0 !important;
}

/* Ensure all form elements have consistent label styling - DARK THEME */
.stSelectbox label,
.stMultiSelect label,
.stDateInput label,
.stNumberInput label,
.stTextArea label,
.stTextInput label,
.stToggle label{
  color:#FFFFFF !important;
  font-weight:900 !important;
  font-size:14px !important;
}

/* ===== BORDERED CONTAINERS - DARK THEME ===== */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[data-testid="element-container"] > div[data-baseweb="block"],
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[data-testid="element-container"] > div[data-baseweb="block"][data-testid="stVerticalBlockBorderWrapper"]{
  border:2px solid #333333 !important;
  border-radius:12px !important;
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  padding:12px 14px !important;
}

/* ===== BUTTONS - DARK THEME (if any are used) ===== */
.stButton > button{
  background:#1A1A1A !important;
  background-color:#1A1A1A !important;
  color:#FFFFFF !important;
  border:2px solid #FF0000 !important;
  border-radius:8px !important;
  font-weight:800 !important;
  padding:10px 20px !important;
  min-height:44px !important;
}
.stButton > button:hover{
  background:#2A2A2A !important;
  background-color:#2A2A2A !important;
  border-color:#FF3333 !important;
}
.stButton > button:focus{
  outline:2px solid #FF0000 !important;
  outline-offset:2px !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------- TITLE -----------------
st.subheader("Pediatric Dashboard")

# ----------------- HELPERS -----------------
def gauge_svg(score_0_to_10: float) -> str:
    angle_deg = 180 - max(0, min(10, score_0_to_10)) * 18.0
    cx, cy, r = 130, 120, 65
    x2 = cx + r * math.cos(math.radians(angle_deg))
    y2 = cy - r * math.sin(math.radians(angle_deg))
    return f"""
    <svg width="260" height="140" viewBox="0 0 260 140">
      <path d="M20 120 A110 110 0 0 1 240 120" fill="none" stroke="#FFE0E0" stroke-width="26" />
      <path d="M20 120 A110 110 0 0 1 160 35" fill="none" stroke="#E15259" stroke-width="26" stroke-linecap="round"/>
      <path d="M160 35 A110 110 0 0 1 240 120" fill="none" stroke="#9DB7FF" stroke-width="26" stroke-linecap="round"/>
      <line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" stroke="#1B1E28" stroke-width="6" stroke-linecap="round"/>
      <circle cx="{cx}" cy="{cy}" r="10" fill="#1B1E28"/>
    </svg>
    """

# ----------------- COLUMNS -----------------
col_left, col_mid, col_right = st.columns([1.1, 1.2, 1.2])

# ================= LEFT COLUMN =================
with col_left:
    st.markdown('<div class="pinkpanel">', unsafe_allow_html=True)
    st.markdown('<div style="padding:6px 10px;"><span style="display:inline-block;padding:6px 12px;border-radius:999px;background:#EEF0F3;border:1px solid #D7DBE0;font-weight:800;font-size:12px;">Premature</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="headerpink">Patient Info</div>', unsafe_allow_html=True)

    # --- Sex selector (Girl/Boy) + highlight icon ---
    sex = st.selectbox("Sex", ["Girl","Boy"], index=0, key="sex")
    sel_girl = " sel" if sex == "Girl" else ""
    sel_boy  = " sel" if sex == "Boy" else ""

    st.markdown(f"""
    <div class="iconrow">
      <div class="iconbox{sel_girl}">♀️</div>
      <div class="iconbox2">👶</div>
      <div class="iconbox3{sel_boy}">♂️</div>
    </div>
    """, unsafe_allow_html=True)

    # Inner white card with ONLY the inputs
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.selectbox("Race", ["White","Black","Asian","Native American","Pacific Islander","Other"], index=0, key="race")
        st.selectbox("Ethnicity", ["German","Hispanic/Latino","Non-Hispanic","Other"], index=1, key="eth")
        st.date_input("Date of Birth", value=dt.date(2025,4,21), key="dob")
        st.number_input("Age at Surgery (days)", min_value=0, value=7, step=1, key="age_days")

        # --- REMOVED mass/mode mini-tiles section (per your request) ---

        # Shunt size scale (visual)
        st.markdown("""
        <div style="margin-top:10px;">
          <div><b>Shunt Size</b></div>
          <div class="card" style="border-radius:14px;">
            <svg width="300" height="70" viewBox="0 0 300 70">
              <line x1="20" y1="45" x2="280" y2="45" stroke="#111" stroke-width="2"/>
              <g fill="#111" font-size="12" text-anchor="middle">
                <line x1="20" y1="38" x2="20" y2="52" stroke="#111" stroke-width="2"/><text x="20" y="65">0</text>
                <line x1="95" y1="38" x2="95" y2="52" stroke="#111" stroke-width="2"/><text x="95" y="65">1</text>
                <line x1="170" y1="38" x2="170" y2="52" stroke="#111" stroke-width="2"/><text x="170" y="65">2</text>
                <line x1="245" y1="38" x2="245" y2="52" stroke="#111" stroke-width="2"/><text x="245" y="65">3</text>
                <line x1="280" y1="38" x2="280" y2="52" stroke="#111" stroke-width="2"/><text x="280" y="65">4</text>
              </g>
              <polygon points="262,18 268,30 256,30" fill="#111"/>
              <line x1="262" y1="30" x2="262" y2="46" stroke="#111" stroke-width="2"/>
            </svg>
            <div class="center"><span class="red">3.5 MM</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # close white card
    st.markdown('</div>', unsafe_allow_html=True)      # close pinkpanel

# ================= MIDDLE COLUMN =================
with col_mid:
    st.markdown('<div class="eventtitle">Cardiac Event</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eventbox">'
        '<div class="right" style="font-size:20px;font-weight:900;">💔 &nbsp; 6/15/2025</div>'
        '<div style="height:10px;"></div>'
        '<div style="height:1px;background:#111;margin:0 4px 8px;"></div>'
        '<div class="center" style="font-style:italic;font-weight:700;">*Details*</div>'
        '</div>', unsafe_allow_html=True)

    st.markdown('<div class="eventtitle">Septic Event</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eventbox">'
        '<div class="right" style="font-size:20px;font-weight:900;">🚩 &nbsp; 5/15/2025</div>'
        '<div style="height:10px;"></div>'
        '<div style="height:1px;background:#111;margin:0 4px 8px;"></div>'
        '<div class="center" style="font-style:italic;font-weight:700;">*Details*</div>'
        '</div>', unsafe_allow_html=True)

    # Risk Factors box (dropdown directly above gauge)
    st.markdown('<div class="eventtitle">Risk Factors</div>', unsafe_allow_html=True)
    with st.container(border=True):
        risk_selection = st.multiselect(
            "Select risk factors",
            ["Premature","Low birth weight","Co-morbidity","Genetic syndrome","Recent infection","Post-op bleed"],
            default=[]
        )
        weights = {"Premature":2.5,"Low birth weight":2.0,"Co-morbidity":1.5,"Genetic syndrome":1.5,"Recent infection":1.0,"Post-op bleed":3.0}
        score = max(0.0, min(10.0, sum(weights.get(x,0) for x in risk_selection)))
        st.write(f"**Score:** {score:.1f} / 10")
        st.markdown('<div class="center" style="font-weight:900;margin:6px 0;">Risk Score</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(gauge_svg(score), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= RIGHT COLUMN =================
with col_right:
    st.markdown('<div class="card"><div class="center" style="font-weight:900;">Vertical<br>Timeline of<br>Events</div>'
                '<div class="timelinewrap"><div class="vert">'
                '<div class="hbot"></div>'
                '<div class="tick" style="top:40px;"><div class="dot"></div><div class="lbl"><b>Discharge</b><br>5-21-25</div></div>'
                '<div class="tick" style="top:170px;"><div class="dot"></div><div class="lbl"><b>Sepsis Found and Treated</b><br>5-15-25</div></div>'
                '<div class="tick" style="top:300px;"><div class="dot"></div><div class="lbl"><b>Bleed Present</b><br>5-03-25</div></div>'
                '<div class="tick" style="top:420px;"><div class="dot"></div><div class="lbl"><b>Surgery Completion</b><br>4-28-25</div></div>'
                '</div></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="center" style="margin:8px 0;"><span class="addbtn">Additional Info</span></div>', unsafe_allow_html=True)
    syn = st.toggle("Syndrome Present", value=True)

    # CHANGED: Fetal Drug Exposure -> Yes/No dropdown
    fd = st.selectbox("Fetal Drug Exposure", ["No","Yes"], index=0)

    ab = st.text_area("Abnormalities / Etc.", value="—", height=80)
    st.markdown(
        f'<div class="card">'
        f'<div style="text-decoration:underline;font-weight:900;">Syndrome Present: {syn}</div>'
        f'Sex: {st.session_state.get("sex","—")}<br>'
        f'Fetal Drug Exposure: {fd}<br>'
        f'Abnormalities: {ab}'
        f'</div>',
        unsafe_allow_html=True
    )
