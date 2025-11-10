# app.py
import streamlit as st
import datetime as dt
import math

st.set_page_config(page_title="Pediatric Dashboard", layout="wide")

# ----------------- THEME FUNCTION -----------------
def get_theme_css(sex):
    """Generate theme CSS based on gender selection"""
    if sex == "Boy":
        # Boy theme - Blue colors
        theme = {
            "bg": "#EFF4F8",
            "panel": "#E8F1FA",
            "border": "#B8D4E8",
            "ink": "#1b1e28",
            "pill": "#EAF3FF",
            "pillborder": "#C7DBFF",
            "hover": "#D6EBFF",
            "selected": "#C7E3FF",
            "card_shadow": "#d0e0f0",
            "panel_border": "#A8C8E0",
            "header_bg": "#A8C8E8",
            "header_border": "#8BB5D8",
            "iconbox1_border": "#7BB3D0",
            "iconbox1_bg": "#C8E3F5",
            "iconbox2_border": "#9DB8C8",
            "iconbox2_bg": "#D0E8F5",
            "iconbox3_border": "#6BA5C8",
            "iconbox3_bg": "#B8DDF5",
            "eventbox_shadow": "#d0e0f0"
        }
    else:
        # Girl theme - Pink colors (default)
        theme = {
            "bg": "#F6EFEF",
            "panel": "#FBECEC",
            "border": "#E1C1C3",
            "ink": "#1b1e28",
            "pill": "#EAF3FF",
            "pillborder": "#C7DBFF",
            "hover": "#EEF4FF",
            "selected": "#FFE7EC",
            "card_shadow": "#f6d8da",
            "panel_border": "#e8c7cf",
            "header_bg": "#f7c8d8",
            "header_border": "#eab2c6",
            "iconbox1_border": "#E7B6C0",
            "iconbox1_bg": "#FFD7E2",
            "iconbox2_border": "#F0C994",
            "iconbox2_bg": "#FFE8C6",
            "iconbox3_border": "#B6D7FF",
            "iconbox3_bg": "#D0E9FF",
            "eventbox_shadow": "#f6d8da"
        }
    
    return f"""
<style>
/* Remove Streamlit chrome + tighten spacing */
header[data-testid="stHeader"]{{display:none !important;}}
#MainMenu, footer{{visibility:hidden !important;}}
.block-container{{padding-top:4px !important; padding-bottom:4px !important; max-width:1320px;}}
[data-testid="stVerticalBlock"] > [style*="width"]{{padding-top:2px !important; padding-bottom:2px !important;}}
[data-testid="column"]{{padding:0 6px !important;}}
h2, h3{{margin-top:4px !important; margin-bottom:8px !important;}}
h3{{font-size:20px !important;}}
[data-testid="stSelectbox"], [data-testid="stDateInput"], [data-testid="stNumberInput"], [data-testid="stTextArea"], [data-testid="stToggle"]{{margin-bottom:8px !important;}}
[data-testid="stMultiSelect"]{{margin-bottom:12px !important;}}
label{{margin-bottom:4px !important; font-weight:700 !important;}}

/* Theme - {'Boy' if sex == 'Boy' else 'Girl'} */
:root{{
  --bg:{theme['bg']}; --panel:{theme['panel']}; --border:{theme['border']}; --ink:{theme['ink']};
  --pill:{theme['pill']}; --pillborder:{theme['pillborder']}; --hover:{theme['hover']}; --selected:{theme['selected']};
}}
[data-testid="stAppViewContainer"]{{background:var(--bg);}}
h1,h2,h3,h4,p,div,span{{color:var(--ink);}}

/* Cards & layout bits */
.card{{background:#fff;border:2px solid var(--border);border-radius:12px;padding:8px 10px;box-shadow:0 2px 0 {theme['card_shadow']} inset;margin-bottom:8px;}}
.pinkpanel{{background:var(--panel);border:2px solid {theme['panel_border']};border-radius:8px;overflow:hidden;}}
.headerpink{{background:{theme['header_bg']};border-bottom:2px solid {theme['header_border']};padding:6px 10px;font-weight:900;text-align:center;font-size:14px;}}
.pill-blue{{display:inline-block;padding:4px 10px;border-radius:999px;background:#d6e7ff;border:1px solid #bcd6ff;font-weight:900;font-size:12px;}}
.iconrow{{display:flex;gap:10px;justify-content:center;padding:6px 0 4px;}}
.iconbox, .iconbox2, .iconbox3{{
  width:70px;height:70px;display:flex;align-items:center;justify-content:center;border-radius:12px;font-size:36px;
}}
.iconbox{{border:2px solid {theme['iconbox1_border']};background:{theme['iconbox1_bg']};}}
.iconbox2{{border:2px solid {theme['iconbox2_border']};background:{theme['iconbox2_bg']};}}
.iconbox3{{border:2px solid {theme['iconbox3_border']};background:{theme['iconbox3_bg']};}}
.sel{{ outline:3px solid #3B82F6; box-shadow:0 0 0 2px #93C5FD inset; }}

.right{{text-align:right;}} .center{{text-align:center;}} .red{{color:#C6002A;font-weight:900;}}

/* Timeline */
.timelinewrap{{padding:6px;}}
.vert{{position:relative;height:400px;margin:0 20px;}}
.vert:before{{content:"";position:absolute;left:50%;top:12px;bottom:12px;width:2px;background:#111;transform:translateX(-50%);}}
.vert:after{{content:"";position:absolute;left:30px;right:30px;top:4px;height:2px;background:#111;}}
.hbot{{position:absolute;left:30px;right:30px;bottom:4px;height:2px;background:#111;}}
.tick{{position:absolute;left:50%;transform:translateX(-50%);}}
.tick .dot{{position:absolute;left:-4px;top:-4px;width:7px;height:7px;background:#111;border-radius:50%;}}
.tick .lbl{{position:absolute;left:16px;top:-8px;width:200px;font-weight:700;font-size:12px;}}

/* Event-look boxes */
.eventbox{{border:2px solid var(--border);border-radius:12px;padding:8px;background:#fff;box-shadow:0 2px 0 {theme['eventbox_shadow']} inset;margin-bottom:8px;}}
.eventtitle{{font-weight:900;margin:4px 0 4px;font-size:15px;}}
.addbtn{{display:inline-block;background:#fff;border:2px solid var(--border);border-radius:999px;padding:6px 16px;font-weight:900;box-shadow:0 2px 0 {theme['eventbox_shadow']} inset;font-size:13px;}}

/* ===== DROPDOWN STYLES - HIGH CONTRAST WHITE BACKGROUND ===== */
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div{{
  background:#FFFFFF !important; 
  background-color:#FFFFFF !important; 
  color:#1B1E28 !important; 
  border-color:#C4C4C4 !important;
  min-height:44px; 
  font-weight:800; 
  border-width:2px !important;
}}
.stSelectbox svg, .stMultiSelect svg{{ 
  fill:#1B1E28 !important; 
  color:#1B1E28 !important; 
}}
div[data-baseweb="select"] input{{ 
  color:#1B1E28 !important; 
  font-weight:800; 
  background:#FFFFFF !important;
  background-color:#FFFFFF !important;
}}
div[data-baseweb="select"] input::placeholder{{ 
  color:#8A8A8A !important; 
}}

/* Dropdown menu popover - FORCE WHITE BACKGROUND */
div[data-baseweb="popover"]{{ 
  z-index: 9999 !important; 
  background:#FFFFFF !important;
  background-color:#FFFFFF !important;
}}
div[data-baseweb="popover"] > div{{
  background:#FFFFFF !important;
  background-color:#FFFFFF !important;
}}
div[data-baseweb="menu"]{{
  background:#FFFFFF !important; 
  background-color:#FFFFFF !important;
  color:#1B1E28 !important; 
  border:2px solid #C4C4C4 !important;
  border-radius:12px !important; 
  box-shadow:0 12px 30px rgba(0,0,0,0.25) !important;
}}
div[data-baseweb="menu"] ul{{ 
  background:#FFFFFF !important; 
  background-color:#FFFFFF !important;
  padding:6px !important; 
}}
div[data-baseweb="menu"] li, 
div[data-baseweb="menu"] [role="option"],
div[data-baseweb="menu"] > ul > li,
div[data-baseweb="menu"] ul li{{
  background:#FFFFFF !important; 
  background-color:#FFFFFF !important;
  color:#1B1E28 !important; 
  font-weight:900 !important;
  font-size:15px !important; 
  padding:10px 12px !important; 
  border-radius:8px !important;
}}
div[data-baseweb="menu"] li:hover, 
div[data-baseweb="menu"] [role="option"]:hover,
div[data-baseweb="menu"] > ul > li:hover,
div[data-baseweb="menu"] ul li:hover{{
  background:#E8E8E8 !important; 
  background-color:#E8E8E8 !important;
  color:#1B1E28 !important;
}}
div[data-baseweb="menu"] li[aria-selected="true"], 
div[data-baseweb="menu"] [role="option"][aria-selected="true"],
div[data-baseweb="menu"] > ul > li[aria-selected="true"],
div[data-baseweb="menu"] ul li[aria-selected="true"]{{
  background:#3B82F6 !important; 
  background-color:#3B82F6 !important;
  color:#FFFFFF !important; 
  box-shadow: inset 4px 0 0 #1E40AF;
}}

/* Force text color in dropdown options - override ALL nested elements */
div[data-baseweb="menu"] li *,
div[data-baseweb="menu"] [role="option"] *,
div[data-baseweb="menu"] span,
div[data-baseweb="menu"] div,
div[data-baseweb="menu"] p,
div[data-baseweb="menu"] li span,
div[data-baseweb="menu"] li div{{
  color:#1B1E28 !important;
}}

/* Override any dark theme styles on popover children - but preserve hover/selected */
div[data-baseweb="popover"] > div{{
  background-color:#FFFFFF !important;
}}
div[data-baseweb="popover"] ul{{
  background-color:#FFFFFF !important;
}}
div[data-baseweb="popover"] li:not(:hover):not([aria-selected="true"]){{
  background-color:#FFFFFF !important;
  color:#1B1E28 !important;
}}

/* Target BaseWeb select dropdown specifically */
[data-baseweb="select"] [role="listbox"],
[data-baseweb="select"] [role="option"]{{
  background:#FFFFFF !important;
  background-color:#FFFFFF !important;
  color:#1B1E28 !important;
}}

/* Multiselect tags */
.stMultiSelect [data-baseweb="tag"]{{
  background:#3B82F6 !important; 
  background-color:#3B82F6 !important;
  color:#FFFFFF !important; 
  border-radius:12px !important; 
  font-weight:900 !important;
}}
</style>
"""

# ----------------- GET CURRENT SEX AND APPLY THEME -----------------
# Get sex from session state (will be updated when user changes selectbox)
current_sex = st.session_state.get("sex", "Girl")
st.markdown(get_theme_css(current_sex), unsafe_allow_html=True)

# ----------------- TITLE -----------------
st.subheader("Pediatric Dashboard")

# ----------------- HELPERS -----------------
def gauge_svg(score_0_to_10: float, large: bool = False) -> str:
    """Generate gauge SVG - larger version for top display"""
    if large:
        angle_deg = 180 - max(0, min(10, score_0_to_10)) * 18.0
        cx, cy, r = 200, 180, 100
        x2 = cx + r * math.cos(math.radians(angle_deg))
        y2 = cy - r * math.sin(math.radians(angle_deg))
        return f"""
        <svg width="400" height="220" viewBox="0 0 400 220">
          <path d="M30 180 A170 170 0 0 1 370 180" fill="none" stroke="#FFE0E0" stroke-width="40" />
          <path d="M30 180 A170 170 0 0 1 250 50" fill="none" stroke="#E15259" stroke-width="40" stroke-linecap="round"/>
          <path d="M250 50 A170 170 0 0 1 370 180" fill="none" stroke="#9DB7FF" stroke-width="40" stroke-linecap="round"/>
          <line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" stroke="#1B1E28" stroke-width="8" stroke-linecap="round"/>
          <circle cx="{cx}" cy="{cy}" r="14" fill="#1B1E28"/>
        </svg>
        """
    else:
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

# ================= RISK SECTION - TOP PRIORITY =================
st.markdown('<div style="margin-bottom:12px;"><h2 style="font-size:28px;font-weight:900;color:#C6002A;margin:4px 0 8px 0;text-align:center;text-shadow:1px 1px 2px rgba(0,0,0,0.1);">⚠️ PATIENT RISK ASSESSMENT ⚠️</h2></div>', unsafe_allow_html=True)

# Calculate risk score first (needed for display)
weights = {"Premature":2.5,"Low birth weight":2.0,"Co-morbidity":1.5,"Genetic syndrome":1.5,"Recent infection":1.0,"Post-op bleed":3.0}
risk_selection = st.multiselect(
    "**🔴 SELECT RISK FACTORS**",
    ["Premature","Low birth weight","Co-morbidity","Genetic syndrome","Recent infection","Post-op bleed"],
    default=[],
    key="risk_factors_top"
)
risk_score = max(0.0, min(10.0, sum(weights.get(x,0) for x in risk_selection)))
risk_percentage = int((risk_score / 10.0) * 100)

# Large risk display at top - MAIN ATTRACTION
st.markdown('<div style="background:linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);border:3px solid #C6002A;border-radius:16px;padding:16px 8px;margin:8px 0 20px 0;box-shadow:0 4px 12px rgba(198,0,42,0.15);">', unsafe_allow_html=True)
risk_col1, risk_col2, risk_col3 = st.columns([1.5, 1.4, 1])
with risk_col1:
    st.markdown(f'<div style="text-align:center;padding:12px 0;"><div style="font-size:72px;font-weight:900;color:#C6002A;line-height:1;text-shadow:2px 2px 4px rgba(0,0,0,0.1);">{risk_percentage}%</div><div style="font-size:24px;font-weight:800;margin-top:8px;color:#8B0000;letter-spacing:2px;">RISK LEVEL</div></div>', unsafe_allow_html=True)
with risk_col2:
    st.markdown('<div style="text-align:center;padding:8px 0;">', unsafe_allow_html=True)
    st.markdown(gauge_svg(risk_score, large=True), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with risk_col3:
    st.markdown(f'<div style="text-align:center;padding:12px 0;"><div style="font-size:48px;font-weight:900;color:#1B1E28;line-height:1.1;">{risk_score:.1f}</div><div style="font-size:20px;font-weight:700;margin-top:6px;color:#555;">/ 10.0</div><div style="font-size:15px;font-weight:700;margin-top:10px;color:#666;text-transform:uppercase;letter-spacing:1px;">Risk Score</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:2px;background:linear-gradient(to right, transparent, #ddd, transparent);margin:8px 0 12px 0;"></div>', unsafe_allow_html=True)

# ----------------- COMPACT COLUMNS -----------------
col_left, col_mid, col_right = st.columns([1.1, 1.2, 1.2])

# ================= LEFT COLUMN =================
with col_left:
    st.markdown('<div class="pinkpanel">', unsafe_allow_html=True)
    st.markdown('<div style="padding:4px 8px;"><span style="display:inline-block;padding:4px 10px;border-radius:999px;background:#EEF0F3;border:1px solid #D7DBE0;font-weight:800;font-size:11px;">Premature</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="headerpink">Patient Info</div>', unsafe_allow_html=True)

    # --- Sex selector (Girl/Boy) + highlight icon ---
    sex = st.selectbox("Sex", ["Girl","Boy"], key="sex")
    sel_girl = " sel" if sex == "Girl" else ""
    sel_boy  = " sel" if sex == "Boy" else ""

    st.markdown(f"""
    <div class="iconrow" style="padding:8px 0 4px;">
      <div class="iconbox{sel_girl}" style="width:60px;height:60px;font-size:30px;">♀️</div>
      <div class="iconbox2" style="width:60px;height:60px;font-size:30px;">👶</div>
      <div class="iconbox3{sel_boy}" style="width:60px;height:60px;font-size:30px;">♂️</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card" style="padding:8px 12px;margin-bottom:8px;">', unsafe_allow_html=True)
        st.selectbox("Race", ["White","Black","Asian","American Indian","Asian","Native Hawaiian", "Other Pacific Islander"], index=0, key="race")
        st.selectbox("Ethnicity", ["German","Hispanic/Latino","Non-Hispanic","Other"], index=1, key="eth")
        st.date_input("Date of Birth", value=dt.date(2025,4,21), key="dob")
        st.number_input("Age at Surgery (days)", min_value=0, value=7, step=1, key="age_days")

        st.markdown("""
        <div style="margin-top:6px;">
          <div style="font-size:13px;font-weight:700;margin-bottom:4px;"><b>Shunt Size</b></div>
          <div class="card" style="border-radius:12px;padding:6px;">
            <svg width="280" height="60" viewBox="0 0 300 70">
              <line x1="20" y1="45" x2="280" y2="45" stroke="#111" stroke-width="2"/>
              <g fill="#111" font-size="11" text-anchor="middle">
                <line x1="20" y1="38" x2="20" y2="52" stroke="#111" stroke-width="2"/><text x="20" y="65">0</text>
                <line x1="95" y1="38" x2="95" y2="52" stroke="#111" stroke-width="2"/><text x="95" y="65">1</text>
                <line x1="170" y1="38" x2="170" y2="52" stroke="#111" stroke-width="2"/><text x="170" y="65">2</text>
                <line x1="245" y1="38" x2="245" y2="52" stroke="#111" stroke-width="2"/><text x="245" y="65">3</text>
                <line x1="280" y1="38" x2="280" y2="52" stroke="#111" stroke-width="2"/><text x="280" y="65">4</text>
              </g>
              <polygon points="262,18 268,30 256,30" fill="#111"/>
              <line x1="262" y1="30" x2="262" y2="46" stroke="#111" stroke-width="2"/>
            </svg>
            <div class="center" style="margin-top:4px;"><span class="red" style="font-size:14px;">3.5 MM</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= MIDDLE COLUMN =================
with col_mid:
    st.markdown('<div class="eventtitle" style="font-size:16px;margin:4px 0;">Cardiac Event</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eventbox" style="padding:8px;">'
        '<div class="right" style="font-size:18px;font-weight:900;">💔 &nbsp; 6/15/2025</div>'
        '<div style="height:6px;"></div>'
        '<div style="height:1px;background:#111;margin:0 4px 6px;"></div>'
        '<div class="center" style="font-style:italic;font-weight:700;font-size:13px;">*Details*</div>'
        '</div>', unsafe_allow_html=True)

    st.markdown('<div class="eventtitle" style="font-size:16px;margin:4px 0;">Septic Event</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eventbox" style="padding:8px;">'
        '<div class="right" style="font-size:18px;font-weight:900;">🚩 &nbsp; 5/15/2025</div>'
        '<div style="height:6px;"></div>'
        '<div style="height:1px;background:#111;margin:0 4px 6px;"></div>'
        '<div class="center" style="font-style:italic;font-weight:700;font-size:13px;">*Details*</div>'
        '</div>', unsafe_allow_html=True)

# ================= RIGHT COLUMN =================
with col_right:
    st.markdown('<div class="card" style="padding:8px;"><div class="center" style="font-weight:900;font-size:14px;">Vertical Timeline of Events</div>'
                '<div class="timelinewrap" style="padding:8px;"><div class="vert" style="height:400px;margin:0 20px;">'
                '<div class="hbot"></div>'
                '<div class="tick" style="top:30px;"><div class="dot"></div><div class="lbl" style="font-size:12px;width:200px;"><b>Discharge</b><br>5-21-25</div></div>'
                '<div class="tick" style="top:130px;"><div class="dot"></div><div class="lbl" style="font-size:12px;width:200px;"><b>Sepsis Found and Treated</b><br>5-15-25</div></div>'
                '<div class="tick" style="top:230px;"><div class="dot"></div><div class="lbl" style="font-size:12px;width:200px;"><b>Bleed Present</b><br>5-03-25</div></div>'
                '<div class="tick" style="top:330px;"><div class="dot"></div><div class="lbl" style="font-size:12px;width:200px;"><b>Surgery Completion</b><br>4-28-25</div></div>'
                '</div></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="center" style="margin:6px 0;"><span class="addbtn" style="padding:6px 16px;font-size:13px;">Additional Info</span></div>', unsafe_allow_html=True)
    syn = st.toggle("Syndrome Present", value=True)
    fd = st.selectbox("Fetal Drug Exposure", ["No","Yes"], index=0)
    ab = st.text_area("Abnormalities / Etc.", value="—", height=60, key="abnormalities")
    st.markdown(
        f'<div class="card" style="padding:8px 12px;font-size:13px;">'
        f'<div style="text-decoration:underline;font-weight:900;">Syndrome Present: {syn}</div>'
        f'Sex: {st.session_state.get("sex","—")}<br>'
        f'Fetal Drug Exposure: {fd}<br>'
        f'Abnormalities: {ab}'
        f'</div>',
        unsafe_allow_html=True
    )
