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
.iconbox{width:70px;height:70px;display:flex;align-items:center;justify-content:center;border-radius:12px;border:2px solid #E7B6C0;background:#FFD7E2;font-size:36px;}
.iconbox2{width:70px;height:70px;display:flex;align-items:center;justify-content:center;border-radius:12px;border:2px solid #F0C994;background:#FFE8C6;font-size:36px;}
.iconbox3{width:70px;height:70px;display:flex;align-items:center;justify-content:center;border-radius:12px;border:2px solid #B6D7FF;background:#D0E9FF;font-size:36px;}
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

/* ===== High-contrast dropdowns (selectbox & multiselect) ===== */
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div{
  background:#ffffff !important; color:#111 !important; border-color:#cfd6e0 !important;
  min-height:44px; font-weight:700;
}
.stSelectbox svg, .stMultiSelect svg{ fill:#111 !important; color:#111 !important; }
div[data-baseweb="select"] input{ color:#111 !important; font-weight:700; }
div[data-baseweb="select"] input::placeholder{ color:#6b7280 !important; }
.stMultiSelect [data-baseweb="tag"]{ background:#eaf2ff !important; color:#0b3c91 !important; border-radius:12px !important; font-weight:800 !important; }
div[data-baseweb="popover"]{ z-index: 9999 !important; }
div[data-baseweb="menu"]{
  background:#ffffff !important; color:#111 !important; border:1px solid #cfd6e0 !important;
  border-radius:12px !important; box-shadow:0 12px 30px rgba(0,0,0,0.18) !important;
}
div[data-baseweb="menu"] ul{ background:#ffffff !important; padding:6px !important; }
div[data-baseweb="menu"] li, div[data-baseweb="menu"] [role="option"]{
  background:#ffffff !important; color:#111 !important; font-weight:800 !important;
  font-size:15px !important; padding:10px 12px !important; border-radius:8px !important;
}
div[data-baseweb="menu"] li:hover, div[data-baseweb="menu"] [role="option"]:hover{
  background:var(--hover) !important; color:#111 !important;
}
div[data-baseweb="menu"] li[aria-selected="true"], div[data-baseweb="menu"] [role="option"][aria-selected="true"]{
  background:var(--selected) !important; color:#111 !important; box-shadow: inset 3px 0 0 #E15259;
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

# ================= LEFT COLUMN (only widgets; no mirrored pills) =================
with col_left:
    st.markdown('<div class="pinkpanel">', unsafe_allow_html=True)
    st.markdown('<div style="padding:6px 10px;"><span style="display:inline-block;padding:6px 12px;border-radius:999px;background:#EEF0F3;border:1px solid #D7DBE0;font-weight:800;font-size:12px;">Premature</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="headerpink">Patient Info</div>', unsafe_allow_html=True)

    # icons row (visual)
    st.markdown("""
    <div style="display:flex;gap:14px;justify-content:center;padding:12px 0 6px;">
      <div class="iconbox">♀️</div>
      <div class="iconbox2">👶</div>
      <div class="iconbox3">♂️</div>
    </div>
    """, unsafe_allow_html=True)

    # Inner white card with ONLY the inputs (no duplicate labels rendered)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.selectbox("Race", ["White","Black","Asian","Native American","Pacific Islander","Other"], index=0, key="race")
        st.selectbox("Ethnicity", ["German","Hispanic/Latino","Non-Hispanic","Other"], index=0, key="eth")
        st.date_input("Date of Birth", value=dt.date(2025,4,21), key="dob")
        st.number_input("Age at Surgery (days)", min_value=0, value=7, step=1, key="age_days")

        # weight + mini tiles (visual only)
        st.markdown("""
        <div style="display:flex;gap:10px;margin-top:8px;">
          <div class="card" style="width:120px;height:96px;border-radius:14px;display:flex;align-items:center;justify-content:center;">
            <div class="center">
              <div style="font-weight:800;">🧪</div>
              <div style="font-size:12px;color:#555;">Mass/Mode</div>
            </div>
          </div>
          <div style="flex:1;display:flex;flex-direction:column;gap:8px;">
            <div class="card" style="border-radius:14px;padding:10px;">
              <div style="font-size:12px;"><b>Pt @ Birth – 6.4 lbs</b><br><b>Pt @ Surgery – 9.4 lbs</b></div>
            </div>
            <div style="display:flex;gap:8px;">
              <div class="card" style="flex:1;padding:8px;border-radius:12px;text-align:center;font-size:12px;">Mean, Mode Wt<br>Birth</div>
              <div class="card" style="flex:1;padding:8px;border-radius:12px;text-align:center;font-size:12px;">Mean, Mode Wt<br>Surgery</div>
              <div class="pill-blue" style="flex:1;text-align:center;display:flex;align-items:center;justify-content:center;">UP Shunt</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # shunt size scale (visual)
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
    fd = st.text_input("Fetal Drug Exposure", value="—")
    ab = st.text_area("Abnormalities / Etc.", value="—", height=80)
    st.markdown(f'<div class="card"><div style="text-decoration:underline;font-weight:900;">Syndrome Present: {syn}</div>'
                f'Fetal Drug Exposure: {fd}<br>Abnormalities: {ab}</div>', unsafe_allow_html=True)
