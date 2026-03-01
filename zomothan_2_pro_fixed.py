import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import joblib

# ═══════════════════════════════════════════════════════════
# PAGE SETUP
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Cart Add-On Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

PRIMARY   = "#FF6B35"
SECONDARY = "#2C3E50"
SUCCESS   = "#27AE60"
WARNING   = "#F39C12"
DANGER    = "#E74C3C"
DARK      = "#1A1A2E"
PALETTE   = ["#FF6B35","#3498DB","#27AE60","#F39C12","#E74C3C","#8E44AD","#1ABC9C","#E67E22"]

# ═══════════════════════════════════════════════════════════
# PROFESSIONAL CSS
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* ── TRUE BLACK BACKGROUND ── */
  html { background: #000 !important; }
  body { background: #000 !important; }
  * { scrollbar-color: #FF6B35 #111; }

  /* Streamlit shell */
  .stApp,
  .stApp > div:first-child,
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"],
  [data-testid="stHeader"],
  .main,
  .main > div,
  .main .block-container,
  .block-container,
  .css-1d391kg, .css-fg4pbf, .css-12oz5g7,
  .css-1y4p8pa, .css-k1ih3n, .css-z5fcl4,
  .css-18e3th9, .css-1lcbmhc,
  section[data-testid="stMain"],
  div[data-testid="stDecoration"] {
    background-color: #000000 !important;
    background: #000000 !important;
  }

  /* Tabs and content panels — transparent so black bg shows through */
  .stTabs,
  [data-testid="stTabsContent"],
  [data-baseweb="tab-panel"],
  [data-testid="stVerticalBlock"],
  [data-testid="stHorizontalBlock"],
  [data-testid="column"],
  [data-testid="stMarkdownContainer"],
  .element-container {
    background-color: transparent !important;
    background: transparent !important;
  }

  /* ── Hero Banner ── */
  .hero {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 40%, #16213e 70%, #0f3460 100%);
    padding: 40px 44px;
    border-radius: 20px;
    color: white;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,107,53,0.2);
  }
  .hero::before {
    content: "";
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(255,107,53,0.18) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero::after {
    content: "";
    position: absolute;
    bottom: -60px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(52,152,219,0.12) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0 0 8px;
    background: linear-gradient(90deg, #ffffff 0%, #FF6B35 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
  }
  .hero p { margin: 0; color: #8899aa; font-size: .9rem; font-weight: 300; }


  /* ── KPI Cards ── */
  .kpi-wrap { height: 100%; }
  .kpi-card {
    background: #111111;
    border-radius: 16px;
    padding: 22px 20px;
    border: 1px solid #2a2a2a;
    box-shadow: 0 2px 12px rgba(255,107,53,.08);
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform .2s, box-shadow .2s;
    height: 100%;
  }
  .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.1); }
  .kpi-card::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #FF6B35, #ff9060);
  }
  .kpi-card .icon { font-size: 1.6rem; margin-bottom: 6px; display: block; }
  .kpi-card .val  { font-family:'Syne',sans-serif; font-size:1.75rem; font-weight:700; color:#FF6B35; display:block; }
  .kpi-card .lbl  { font-size:.8rem; color:#aaa; margin-top:4px; font-weight:500; }
  .kpi-card .sub  { font-size:.72rem; color:#27AE60; font-weight:600; margin-top:3px; }

  /* ── Section Titles ── */
  .sec-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
    padding-bottom: 8px;
    margin: 20px 0 16px;
    border-bottom: 3px solid #FF6B35;
    display: inline-block;
  }

  /* ── Insight Pills ── */
  .insight-pill {
    background: linear-gradient(135deg, #1a0f0a 0%, #1f1208 100%);
    border: 1px solid #3a2010;
    border-left: 4px solid #FF6B35;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: .88rem;
    color: #ccc;
    margin: 10px 0;
    line-height: 1.6;
  }
  .insight-pill strong { color: #FF6B35; }

  /* ── Chart Containers ── */
  .chart-box {
    background: #111111;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #222222;
    box-shadow: 0 2px 10px rgba(255,107,53,.06);
    margin-bottom: 16px;
  }

  /* ── Prediction Result Cards ── */
  .pred-accept {
    background: linear-gradient(135deg, #d4edda, #c3e6cb);
    border: 2px solid #27AE60;
    border-radius: 14px;
    padding: 22px;
    text-align: center;
  }
  .pred-reject {
    background: linear-gradient(135deg, #f8d7da, #f5c6cb);
    border: 2px solid #E74C3C;
    border-radius: 14px;
    padding: 22px;
    text-align: center;
  }
  .pred-label { font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:700; }
  .pred-prob  { font-size:2.5rem; font-weight:800; font-family:'Syne',sans-serif; }

  /* ── Probability Gauge Bar ── */
  .prob-bar-bg {
    background: #e9ecef; border-radius: 8px; height: 14px; margin-top: 10px; overflow: hidden;
  }
  .prob-bar-fill {
    height: 14px; border-radius: 8px;
    background: linear-gradient(90deg, #FF6B35, #ff9060);
    transition: width .6s ease;
  }

  /* ── Table Styling ── */
  .styled-table { width: 100%; border-collapse: collapse; font-size: .87rem; }
  .styled-table th {
    background: #1A1A2E; color: white;
    padding: 10px 14px; text-align: left; font-weight: 600; font-size: .8rem;
  }
  .styled-table td { padding: 9px 14px; border-bottom: 1px solid #222; color: #ccc; }
  .styled-table tr:hover td { background: #1a0f0a; }

  /* ── Sidebar — true black ── */
  div[data-testid="stSidebar"],
  div[data-testid="stSidebar"] > div,
  div[data-testid="stSidebar"] > div:first-child,
  section[data-testid="stSidebar"],
  [data-testid="stSidebarNav"],
  [data-testid="stSidebarContent"] {
    background-color: #000000 !important;
    background: #000000 !important;
    border-right: 1px solid #1f1f1f !important;
  }
  div[data-testid="stSidebar"] * { color: #cccccc !important; }
  div[data-testid="stSidebar"] h2,
  div[data-testid="stSidebar"] h3 { color: #ffffff !important; font-weight: 700 !important; }
  div[data-testid="stSidebar"] hr { border-color: #222222 !important; }
  div[data-testid="stSidebar"] .stSlider .stMarkdown { color: #aaa !important; }
  /* multiselect tags stay orange on black */
  div[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #FF6B35 !important;
    border: none !important;
  }
  /* multiselect input bg */
  div[data-testid="stSidebar"] [data-baseweb="select"] > div,
  div[data-testid="stSidebar"] [data-baseweb="input"] {
    background-color: #111111 !important;
    border-color: #333 !important;
  }
  /* slider track */
  div[data-testid="stSidebar"] [data-testid="stSlider"] > div > div {
    background-color: #222222 !important;
  }

  /* ── Tab Styling ── */
  .stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #111111;
    padding: 6px 8px;
    border-radius: 12px;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 18px;
    font-size: .85rem;
    font-weight: 600;
    color: #aaa !important;
  }
  .stTabs [aria-selected="true"] {
    background: #FF6B35 !important;
    color: white !important;
  }

  /* ── Dataframe dark theme ── */
  [data-testid="stDataFrame"] { background-color: #111111 !important; }
  [data-testid="stDataFrame"] * { color: #cccccc !important; }

  /* ── General text on black bg ── */
  p, span, label, div { color: #cccccc; }
  h1, h2, h3, h4 { color: #ffffff; }
  .stMarkdown p { color: #cccccc; }
  .stMarkdown li { color: #cccccc; }

  /* ── Download Button ── */
  .stDownloadButton button {
    background: linear-gradient(135deg, #FF6B35, #ff8c5a) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    width: 100%;
    font-weight: 600 !important;
  }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# CHART STYLING HELPER
# ═══════════════════════════════════════════════════════════
def style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor("#080808")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["left"].set_color("#333333")
    ax.spines["bottom"].set_color("#333333")
    ax.tick_params(colors="#aaaaaa", labelsize=9)
    ax.set_xlabel(xlabel, fontsize=10, color="#bbbbbb", labelpad=8)
    ax.set_ylabel(ylabel, fontsize=10, color="#bbbbbb", labelpad=8)
    if title:
        ax.set_title(title, fontsize=11, fontweight="700", color="#ffffff", pad=12)
    ax.yaxis.grid(True, color="#222222", linewidth=0.8)
    ax.set_axisbelow(True)

def style_fig(fig):
    fig.patch.set_facecolor("#000000")
    fig.patch.set_edgecolor("none")

# ═══════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("csao_model_ready.csv")
    meal_map = {0:"Breakfast",1:"Lunch",2:"Evening Snack",3:"Dinner",4:"Late Night"}
    seg_map  = {0:"Budget",1:"Frequent",2:"Premium"}
    pr_map   = {0:"Low",1:"Medium",2:"High"}
    cat_fn   = lambda r: ("Dessert" if r["cat_dessert"] else
                          "Drink"   if r["cat_drink"]   else
                          "Main"    if r["cat_main_course"] else "Side")
    df["meal_label"]    = df["meal_time"].map(meal_map)
    df["segment_label"] = df["user_segment"].map(seg_map)
    df["price_label"]   = df["rest_price_range"].map(pr_map)
    df["item_category"] = df.apply(cat_fn, axis=1)
    df["veg_label"]     = df["candidate_is_veg"].map({0:"Non-Veg",1:"Veg"})
    df["accepted"]      = df["label"].map({0:"Rejected",1:"Accepted"})
    try:
        feat_imp = pd.read_csv("csao_feature_importance.csv")
    except:
        feat_imp = None
    return df, feat_imp

df, feat_imp = load_data()

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎛️ Dashboard Filters")
    st.markdown("---")
    seg_filter   = st.multiselect("👤 User Segment",    ["Budget","Frequent","Premium"],
                                   default=["Budget","Frequent","Premium"])
    meal_filter  = st.multiselect("🕐 Meal Time",       ["Breakfast","Lunch","Evening Snack","Dinner","Late Night"],
                                   default=["Breakfast","Lunch","Evening Snack","Dinner","Late Night"])
    price_filter = st.multiselect("💰 Price Range",     ["Low","Medium","High"],
                                   default=["Low","Medium","High"])
    cat_filter   = st.multiselect("🍔 Item Category",   ["Main","Drink","Side","Dessert"],
                                   default=["Main","Drink","Side","Dessert"])
    st.markdown("---")
    price_range  = st.slider("Candidate Price (₹)", 50, 420, (50, 420))
    st.markdown("---")
    st.markdown("### 📥 Export Filtered Data")
    mask_dl = (
        df["segment_label"].isin(seg_filter) &
        df["meal_label"].isin(meal_filter) &
        df["price_label"].isin(price_filter) &
        df["item_category"].isin(cat_filter) &
        df["candidate_price"].between(price_range[0], price_range[1])
    )
    csv_data = df[mask_dl].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered CSV",
        data=csv_data,
        file_name="csao_filtered_report.csv",
        mime="text/csv",
    )

# ═══════════════════════════════════════════════════════════
# APPLY FILTERS
# ═══════════════════════════════════════════════════════════
mask = (
    df["segment_label"].isin(seg_filter) &
    df["meal_label"].isin(meal_filter) &
    df["price_label"].isin(price_filter) &
    df["item_category"].isin(cat_filter) &
    df["candidate_price"].between(price_range[0], price_range[1])
)
filtered = df[mask].copy()

# ═══════════════════════════════════════════════════════════
# HERO BANNER
# ═══════════════════════════════════════════════════════════

st.markdown(f"""
<div class="hero">
  <h1>Cart Add-On Analytics<br>Dashboard</h1>
  <p>Real-time insights on Cart Add-On recommendation performance · ML-powered intelligence</p>

</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# KPI CARDS
# ═══════════════════════════════════════════════════════════
acc_rate  = filtered["label"].mean() * 100
avg_price = filtered["candidate_price"].mean()
avg_cooc  = filtered["max_co_occur_confidence"].mean()
prev_ord  = filtered["candidate_ordered_before"].mean() * 100
acc_recs  = int(filtered["label"].sum())
avg_acc_p = filtered[filtered["label"]==1]["candidate_price"].mean()
if np.isnan(avg_acc_p): avg_acc_p = 0
est_rev   = acc_recs * avg_acc_p

k1,k2,k3,k4,k5,k6 = st.columns(6)
kpis = [
    ("📦", f"{len(filtered):,}",       "Filtered Records",    f"of {len(df):,} total"),
    ("✅", f"{acc_rate:.1f}%",          "Acceptance Rate",     "recommendation accepted"),
    ("💵", f"₹{avg_price:.0f}",         "Avg Item Price",      "candidate add-on price"),
    ("🔗", f"{avg_cooc:.3f}",           "Avg Pairing Score",   "co-occurrence strength"),
    ("⭐", f"{prev_ord:.1f}%",          "Prev. Ordered",       "personalization signal"),
    ("📈", f"₹{est_rev:,.0f}",          "Est. Revenue Lift",   "accepted × avg price"),
]
for col,(icon,val,lbl,sub) in zip([k1,k2,k3,k4,k5,k6], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <span class="icon">{icon}</span>
          <span class="val">{val}</span>
          <div class="lbl">{lbl}</div>
          <div class="sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6= st.tabs([
    "📈 Acceptance Analysis",
    "💰 Price & Cart",
    "👤 User & Segment",
    "🍔 Top Pairings",
    "🔮 Live Predictor",
    "🧠 AI Insights",
   
])

# ── TAB 1: ACCEPTANCE ANALYSIS ─────────────────────────────
with tab1:
    st.markdown('<div class="sec-title">📈 Acceptance Rate Deep Dive</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        meal_acc = filtered.groupby("meal_label")["label"].mean().reset_index()
        meal_acc.columns = ["meal_time","rate"]
        meal_acc["pct"] = (meal_acc["rate"]*100).round(2)
        order = ["Breakfast","Lunch","Evening Snack","Dinner","Late Night"]
        meal_acc["meal_time"] = pd.Categorical(meal_acc["meal_time"], categories=order, ordered=True)
        meal_acc = meal_acc.sort_values("meal_time")

        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        colors = [PRIMARY if v == meal_acc["pct"].max() else "#c0d4e8" for v in meal_acc["pct"]]
        bars = ax.bar(meal_acc["meal_time"], meal_acc["pct"], color=colors, width=0.55, edgecolor="none", zorder=3)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2, h+0.4, f"{h:.1f}%",
                    ha="center", va="bottom", fontsize=9, fontweight="600", color="#333")
        style_ax(ax, "Acceptance Rate by Meal Time", "", "Acceptance %")
        plt.xticks(rotation=25, ha="right")
        ax.set_ylim(0, meal_acc["pct"].max()+7)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with c2:
        cat_acc = filtered.groupby("item_category")["label"].mean().reset_index()
        cat_acc.columns = ["category","rate"]
        cat_acc["pct"] = (cat_acc["rate"]*100).round(2)
        cat_acc = cat_acc.sort_values("pct")

        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        cat_colors = [PALETTE[i % len(PALETTE)] for i in range(len(cat_acc))]
        bars = ax.barh(cat_acc["category"], cat_acc["pct"],
                       color=cat_colors, height=0.5, edgecolor="none", zorder=3)
        for bar in bars:
            w = bar.get_width()
            ax.text(w+0.3, bar.get_y()+bar.get_height()/2, f"{w:.1f}%",
                    va="center", fontsize=9, fontweight="600", color="#333")
        style_ax(ax, "Acceptance Rate by Item Category", "Acceptance %", "")
        ax.set_xlim(0, cat_acc["pct"].max()+7)
        ax.xaxis.grid(True, color="#efefef", linewidth=0.8)
        ax.yaxis.grid(False)
        ax.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    hour_acc = filtered.groupby("hour")["label"].mean().reset_index()
    hour_acc.columns = ["hour","rate"]
    hour_acc["pct"] = (hour_acc["rate"]*100).round(2)

    fig, ax = plt.subplots(figsize=(12,3.5))
    style_fig(fig)
    ax.fill_between(hour_acc["hour"], hour_acc["pct"], alpha=0.15, color=PRIMARY)
    ax.plot(hour_acc["hour"], hour_acc["pct"], color=PRIMARY, linewidth=2.5, zorder=3)
    ax.scatter(hour_acc["hour"], hour_acc["pct"], color=PRIMARY, s=50, zorder=4, edgecolors="white", linewidths=1.5)
    style_ax(ax, "Acceptance Rate by Hour of Day", "Hour of Day (0–23)", "Acceptance %")
    ax.set_xticks(range(0,24,1))
    ax.set_xticklabels([str(h) for h in range(24)], fontsize=8)
    ax.set_ylim(0, hour_acc["pct"].max()+8)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    best_meal = meal_acc.sort_values("pct", ascending=False).iloc[0]
    best_cat  = cat_acc.sort_values("pct", ascending=False).iloc[0]
    st.markdown(f"""
    <div class="insight-pill">
      💡 <strong>{best_meal['meal_time']}</strong> achieves the highest acceptance at
      <strong>{best_meal['pct']}%</strong>. Among categories,
      <strong>{best_cat['category']}</strong> items perform best at
      <strong>{best_cat['pct']}%</strong> acceptance — these are your highest-ROI slots.
    </div>""", unsafe_allow_html=True)

# ── TAB 2: PRICE & CART ───────────────────────────────────
with tab2:
    st.markdown('<div class="sec-title">💰 Price Sensitivity & Cart Behavior</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        ax.hist(filtered[filtered["label"]==0]["candidate_price"], bins=25,
                alpha=0.65, color="#3498DB", label="Rejected", edgecolor="none", zorder=3)
        ax.hist(filtered[filtered["label"]==1]["candidate_price"], bins=25,
                alpha=0.80, color=PRIMARY, label="Accepted", edgecolor="none", zorder=4)
        ax.axvline(filtered[filtered["label"]==1]["candidate_price"].mean(),
                   color=PRIMARY, linestyle="--", linewidth=1.5, alpha=0.9)
        ax.axvline(filtered[filtered["label"]==0]["candidate_price"].mean(),
                   color="#3498DB", linestyle="--", linewidth=1.5, alpha=0.9)
        # FIX: create legend manually instead of using legend= in barplot
        patch_acc = mpatches.Patch(color=PRIMARY,   alpha=0.8, label="Accepted")
        patch_rej = mpatches.Patch(color="#3498DB", alpha=0.65, label="Rejected")
        ax.legend(handles=[patch_acc, patch_rej], fontsize=9)
        style_ax(ax, "Price Distribution: Accepted vs Rejected", "Candidate Price (₹)", "Count")
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with c2:
        avg_cart = filtered.groupby("accepted")["cart_total_value"].mean().reset_index()

        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        bar_colors = [PRIMARY if a=="Accepted" else "#3498DB" for a in avg_cart["accepted"]]
        bars = ax.bar(avg_cart["accepted"], avg_cart["cart_total_value"],
                      color=bar_colors, width=0.45, edgecolor="none", zorder=3)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2, h+2, f"₹{h:.0f}",
                    ha="center", va="bottom", fontsize=10, fontweight="700", color="#333")
        style_ax(ax, "Average Cart Value by Recommendation Outcome", "Outcome", "Avg Cart Value (₹)")
        ax.set_ylim(0, avg_cart["cart_total_value"].max()+40)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    c3, c4 = st.columns(2)

    with c3:
        sample = filtered.sample(min(3000, len(filtered)), random_state=42)

        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        for outcome, color in [("Rejected","#3498DB"), ("Accepted",PRIMARY)]:
            sub = sample[sample["accepted"]==outcome]
            ax.scatter(sub["candidate_price"], sub["candidate_price_vs_cart_avg"],
                       color=color, alpha=0.35, s=18, label=outcome, edgecolors="none", zorder=3)
        ax.axhline(1.0, linestyle="--", color="#999", linewidth=1.2, alpha=0.8, label="Cart Avg Line")
        ax.legend(fontsize=9)
        style_ax(ax, "Item Price vs Price Relative to Cart Avg",
                 "Candidate Price (₹)", "Price ÷ Cart Avg")
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with c4:
        cooc = filtered.copy()
        cooc["confidence_range"] = pd.cut(
            cooc["max_co_occur_confidence"],
            bins=[0,0.1,0.3,0.5,0.7,1.0],
            labels=["0–0.1","0.1–0.3","0.3–0.5","0.5–0.7","0.7–1.0"]
        )
        cooc_s = cooc.groupby("confidence_range", observed=True)["label"].mean().reset_index()
        cooc_s["pct"] = (cooc_s["label"]*100).round(1)

        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        ax.plot(cooc_s["confidence_range"].astype(str), cooc_s["pct"],
                marker="o", linewidth=2.5, color=PRIMARY,
                markersize=9, markerfacecolor="white", markeredgewidth=2.5,
                markeredgecolor=PRIMARY, zorder=3)
        ax.fill_between(range(len(cooc_s)), cooc_s["pct"], alpha=0.1, color=PRIMARY)
        for i, (x, y) in enumerate(zip(range(len(cooc_s)), cooc_s["pct"])):
            ax.text(x, y+0.8, f"{y:.1f}%", ha="center", fontsize=9, fontweight="600", color=PRIMARY)
        style_ax(ax, "Acceptance Rate by Co-occurrence Confidence",
                 "Co-occurrence Range", "Acceptance Rate (%)")
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    ap = filtered[filtered["label"]==1]["candidate_price"].mean()
    rp = filtered[filtered["label"]==0]["candidate_price"].mean()
    st.markdown(f"""
    <div class="insight-pill">
      💡 Accepted items average <strong>₹{ap:.0f}</strong> vs
      <strong>₹{rp:.0f}</strong> for rejected. Acceptance increases sharply with
      co-occurrence confidence — items with high cart pairing scores should always be prioritised.
    </div>""", unsafe_allow_html=True)

# ── TAB 3: USER & SEGMENT ─────────────────────────────────
with tab3:
    st.markdown('<div class="sec-title">👤 User Segment Behavior Analysis</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        seg_d = filtered.groupby("segment_label")["label"].mean().reset_index()
        seg_d["pct"] = (seg_d["label"]*100).round(1)

        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        seg_colors = ["#3498DB","#FF6B35","#27AE60"]
        bars = ax.bar(seg_d["segment_label"], seg_d["pct"],
                      color=seg_colors[:len(seg_d)], width=0.45, edgecolor="none", zorder=3)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2, h+0.4, f"{h:.1f}%",
                    ha="center", va="bottom", fontsize=10, fontweight="700", color="#333")
        style_ax(ax, "Acceptance Rate by User Segment", "User Segment", "Acceptance %")
        ax.set_ylim(0, seg_d["pct"].max()+8)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with c2:
        seg_aov = filtered.groupby(["segment_label","accepted"])["user_avg_order_value"].mean().reset_index()
        pivot   = seg_aov.pivot(index="segment_label", columns="accepted", values="user_avg_order_value")

        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        x     = np.arange(len(pivot.index))
        width = 0.35
        if "Accepted" in pivot.columns:
            ax.bar(x - width/2, pivot["Accepted"], width, color=PRIMARY,   label="Accepted", edgecolor="none", zorder=3)
        if "Rejected" in pivot.columns:
            ax.bar(x + width/2, pivot["Rejected"], width, color="#3498DB", label="Rejected", edgecolor="none", zorder=3)
        ax.set_xticks(x); ax.set_xticklabels(pivot.index, fontsize=10)
        ax.legend(fontsize=9)
        style_ax(ax, "Average Order Value by Segment", "User Segment", "Avg Order Value (₹)")
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    c3, c4 = st.columns(2)

    with c3:
        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        ax.hist(filtered[filtered["label"]==0]["user_veg_preference_ratio"],
                bins=20, alpha=0.6, color="#3498DB", label="Rejected", edgecolor="none", zorder=3)
        ax.hist(filtered[filtered["label"]==1]["user_veg_preference_ratio"],
                bins=20, alpha=0.75, color=PRIMARY, label="Accepted", edgecolor="none", zorder=4)
        patch_a = mpatches.Patch(color=PRIMARY,   alpha=0.75, label="Accepted")
        patch_r = mpatches.Patch(color="#3498DB", alpha=0.6,  label="Rejected")
        ax.legend(handles=[patch_a, patch_r], fontsize=9)
        style_ax(ax, "Veg Preference Distribution",
                 "Veg Preference Ratio (0=Non-Veg, 1=Veg)", "Count")
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with c4:
        sample2 = filtered.sample(min(3000, len(filtered)), random_state=42)
        fig, ax = plt.subplots(figsize=(6,4))
        style_fig(fig)
        for outcome, color in [("Rejected","#BDC3C7"), ("Accepted",PRIMARY)]:
            sub = sample2[sample2["accepted"]==outcome]
            ax.scatter(sub["user_order_frequency"], sub["days_since_last_order"],
                       color=color, alpha=0.4, s=20, label=outcome, edgecolors="none", zorder=3)
        ax.legend(fontsize=9)
        style_ax(ax, "Order Frequency vs Recency",
                 "Total Orders by User", "Days Since Last Order")
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    st.markdown('<div class="sec-title">Segment Summary Table</div>', unsafe_allow_html=True)
    seg_table = filtered.groupby("segment_label").agg(
        Records=("label","count"), Acceptance=("label","mean"),
        Avg_Price=("candidate_price","mean"), Cart_Value=("cart_total_value","mean"),
        User_AOV=("user_avg_order_value","mean"), Co_occur=("max_co_occur_confidence","mean")
    ).reset_index()
    seg_table["Acceptance"]  = (seg_table["Acceptance"]*100).round(1).astype(str)+"%"
    seg_table["Avg_Price"]   = "₹"+seg_table["Avg_Price"].round(0).astype(int).astype(str)
    seg_table["Cart_Value"]  = "₹"+seg_table["Cart_Value"].round(0).astype(int).astype(str)
    seg_table["User_AOV"]    = "₹"+seg_table["User_AOV"].round(0).astype(int).astype(str)
    seg_table["Co_occur"]    = seg_table["Co_occur"].round(3)
    st.dataframe(seg_table.rename(columns={"segment_label":"User Segment"}), use_container_width=True)

# ── TAB 4: TOP PAIRINGS ───────────────────────────────────
with tab4:
    st.markdown('<div class="sec-title">🍔 Cross-Sell Secrets & Top Pairings</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1])

    with c1:
        st.markdown("**🔥 Acceptance Heatmap: Meal Time × Add-on Category**")
        pivot = (filtered.pivot_table(index="meal_label", columns="item_category",
                                      values="label", aggfunc="mean") * 100)
        meal_order = ["Breakfast","Lunch","Evening Snack","Dinner","Late Night"]
        pivot = pivot.reindex([m for m in meal_order if m in pivot.index])

        fig, ax = plt.subplots(figsize=(7,5))
        style_fig(fig)
        sns.heatmap(pivot, annot=True, fmt=".1f", cmap="Oranges",
                    linewidths=1.5, linecolor="white",
                    cbar_kws={"label":"Acceptance Rate (%)","shrink":0.8}, ax=ax)
        ax.set_ylabel("Meal Time", fontsize=10, color="#444")
        ax.set_xlabel("Add-on Category", fontsize=10, color="#444")
        ax.set_title("Which Add-on Works Best at What Time?",
                     fontsize=11, fontweight="700", color="#1a1a2e", pad=12)
        ax.tick_params(colors="#aaaaaa", labelsize=9)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with c2:
        st.markdown("**🤝 Strongest Cart Pairings by Category**")
        top_pairs = filtered.groupby("item_category").agg(
            Pairing_Strength=("max_co_occur_confidence","mean"),
            Acceptance_Rate=("label","mean"),
            Volume=("label","count")
        ).reset_index()
        top_pairs["Acceptance_Rate"] = (top_pairs["Acceptance_Rate"]*100).round(1).astype(str)+"%"
        top_pairs["Pairing_Strength"] = top_pairs["Pairing_Strength"].round(3)
        top_pairs = top_pairs.sort_values("Pairing_Strength", ascending=False)
        st.dataframe(
            top_pairs.rename(columns={"item_category":"Category"}),
            use_container_width=True, hide_index=True
        )
        st.markdown("""
        <div class="insight-pill">
          💡 <strong>Pro Insight:</strong> High Pairing Strength = high Success Rate.
          Dark orange boxes in the heatmap are your most profitable cross-sell opportunities.
          Target these combos first in the CSAO rail.
        </div>""", unsafe_allow_html=True)

# ── TAB 5: LIVE PREDICTOR ─────────────────────────────────
with tab5:
    st.markdown('<div class="sec-title">🔮 Live Prediction Helper</div>', unsafe_allow_html=True)
    st.markdown("Simulate any scenario and see what the recommendation model would decide.")

    try:
        model         = joblib.load("csao_model.joblib")
        features_list = joblib.load("csao_features.joblib")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**1️⃣ Cart Scenario**")
            u_seg    = st.selectbox("User Segment",  ["Budget","Frequent","Premium"], index=1)
            m_time   = st.selectbox("Meal Time",     ["Breakfast","Lunch","Evening Snack","Dinner","Late Night"], index=3)
            cart_val = st.number_input("Cart Total Value (₹)", 50, 2000, 350)
            co_occur = st.slider("Pairing Strength", 0.0, 1.0, 0.15)

        with c2:
            st.markdown("**2️⃣ Candidate Add-on**")
            c_price       = st.number_input("Add-on Price (₹)", 10, 500, 99)
            ordered_before= st.radio("User ordered this before?", ["Yes","No"])
            i_cat         = st.selectbox("Item Category", ["Dessert","Drink","Side","Main Course"])

        u_seg_map  = {"Budget":0,"Frequent":1,"Premium":2}
        m_time_map = {"Breakfast":0,"Lunch":1,"Evening Snack":2,"Dinner":3,"Late Night":4}

        base = df[features_list].median(numeric_only=True).to_dict()
        base["user_segment"]               = u_seg_map[u_seg]
        base["meal_time"]                  = m_time_map[m_time]
        base["cart_total_value"]           = cart_val
        base["max_co_occur_confidence"]    = co_occur
        base["candidate_price"]            = c_price
        base["candidate_ordered_before"]   = 1 if ordered_before=="Yes" else 0
        base["cat_dessert"]                = 1 if i_cat=="Dessert"     else 0
        base["cat_drink"]                  = 1 if i_cat=="Drink"       else 0
        base["cat_main_course"]            = 1 if i_cat=="Main Course" else 0
        base["cat_side"]                   = 1 if i_cat=="Side"        else 0
        base["candidate_price_vs_cart_avg"]= c_price/cart_val if cart_val>0 else 0

        prob       = model.predict_proba(pd.DataFrame([base])[features_list])[0][1]
        pred_class = 1 if prob >= 0.5 else 0
        pct        = prob*100
        bar_color  = "#27AE60" if pred_class==1 else "#E74C3C"

        st.markdown("---")
        st.markdown("### 📊 Model Decision")
        r1, r2 = st.columns([1.2, 1])

        with r1:
            if pred_class==1:
                st.markdown(f"""
                <div class="pred-accept">
                  <div class="pred-label" style="color:#155724">✅ RECOMMEND</div>
                  <div class="pred-prob" style="color:#27AE60">{pct:.1f}%</div>
                  <div style="font-size:.85rem;color:#155724;margin-top:6px">Likely to Accept</div>
                  <div class="prob-bar-bg">
                    <div class="prob-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#27AE60,#2ecc71)"></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="pred-reject">
                  <div class="pred-label" style="color:#721c24">❌ DO NOT RECOMMEND</div>
                  <div class="pred-prob" style="color:#E74C3C">{pct:.1f}%</div>
                  <div style="font-size:.85rem;color:#721c24;margin-top:6px">Likely to Reject</div>
                  <div class="prob-bar-bg">
                    <div class="prob-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#E74C3C,#e74c3c88)"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
            <div class="kpi-card" style="text-align:left;padding:20px;background:#111111;border:1px solid #2a2a2a">
              <div style="font-size:.85rem;color:#888;font-weight:600;margin-bottom:12px">INPUT SUMMARY</div>
              <div style="font-size:.88rem;line-height:2;color:#ccc">
                👤 Segment: <strong>{u_seg}</strong><br>
                🕐 Meal: <strong>{m_time}</strong><br>
                🛒 Cart Value: <strong>₹{cart_val}</strong><br>
                💵 Item Price: <strong>₹{c_price}</strong><br>
                🔗 Pairing: <strong>{co_occur:.2f}</strong><br>
                ⭐ Prev. Ordered: <strong>{ordered_before}</strong>
              </div>
            </div>""", unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"⚠️ Model files not found. Please run `csao_train_and_save.py` first.")
        st.info(f"Details: {e}")

# ── TAB 6: AI INSIGHTS ────────────────────────────────────
with tab6:
    st.markdown('<div class="sec-title">🧠 AI Model Insights & Key Drivers</div>', unsafe_allow_html=True)
    st.markdown("Understanding which factors the ML model values most in making recommendations.")

    if feat_imp is not None:
        top_feats = feat_imp.head(15).sort_values("importance", ascending=True)

        fig = px.bar(
            top_feats, x="importance", y="feature", orientation="h",
            title="Top 15 Most Important Features for AI Prediction",
            color="importance",
            color_continuous_scale=[[0,"#ffe4d6"],[0.5,"#ff9060"],[1,"#FF6B35"]],
            labels={"importance":"Importance Score","feature":""},
        )
        fig.update_layout(
            paper_bgcolor="#000000", plot_bgcolor="#0d0d0d",
            font=dict(color="#cccccc", family="Inter"),
            title_font=dict(size=14, color="#ffffff"),
            coloraxis_showscale=False,
            margin=dict(l=180, r=40, t=60, b=20),
            height=520,
            xaxis=dict(gridcolor="#222222"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        )
        fig.update_traces(
            text=[f"{v:.4f}" for v in top_feats["importance"]],
            textposition="outside",
            textfont_size=10,
        )
        st.plotly_chart(fig, use_container_width=True)

        t1 = feat_imp.iloc[0]; t2 = feat_imp.iloc[1]; t3 = feat_imp.iloc[2]
        total3 = (t1["importance"]+t2["importance"]+t3["importance"])*100

        
    else:
        st.warning("Feature importance file `csao_feature_importance.csv` not found. Run `csao_train_and_save.py` first.")


    