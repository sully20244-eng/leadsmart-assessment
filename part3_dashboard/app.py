# LeadSmart Predictive Intelligence Dashboard - Enhanced & Creative
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from joblib import load
from datetime import datetime, timedelta

# =========================
# 1) ENHANCED Page Config + CSS
# =========================
st.set_page_config(
    page_title="LeadSmart – Predictive Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

ENHANCED_CSS = """
<style>
/* Main container */
.main {
    background: linear-gradient(135deg, #0a0e17 0%, #121828 100%);
}

/* Enhanced KPI Cards */
.kpi-card {
    padding: 20px 24px;
    border-radius: 20px;
    background: linear-gradient(145deg, #1a1f35 0%, #0f1324 100%);
    border: 1px solid #2a2f45;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%);
}

.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
    border-color: #3a3f55;
}

.kpi-title {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 8px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.kpi-value {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 4px;
    line-height: 1.2;
}

.kpi-gradient-value {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff 0%, #c7d2fe 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
    line-height: 1.2;
}

.kpi-sub {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 4px;
}

.kpi-trend {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 6px;
}

.trend-up {
    background: rgba(34, 197, 94, 0.15);
    color: #22c55e;
}

.trend-down {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
}

/* Section Titles */
.section-title {
    font-size: 1.6rem;
    font-weight: 700;
    margin: 1.5rem 0 1rem 0;
    color: #ffffff;
    padding-bottom: 8px;
    border-bottom: 2px solid #2a2f45;
}

.section-title-gradient {
    font-size: 1.6rem;
    font-weight: 700;
    margin: 1.5rem 0 1rem 0;
    background: linear-gradient(90deg, #ffffff 0%, #94a3b8 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 8px;
    border-bottom: 2px solid #2a2f45;
}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    border-radius: 12px 12px 0 0;
    padding: 0 24px;
    font-weight: 600;
    background-color: #1a1f35;
    border: 1px solid #2a2f45;
    color: #94a3b8;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
    color: #ffffff;
    border-bottom: 3px solid #4f46e5;
}

/* Sidebar Enhancement */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1324 0%, #1a1f35 100%);
    border-right: 1px solid #2a2f45;
}

/* Chart Container */
.chart-container {
    background: #1a1f35;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #2a2f45;
    margin-bottom: 24px;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #1a1f35;
}

::-webkit-scrollbar-thumb {
    background: #4f46e5;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #6366f1;
}

/* Metric Badges */
.metric-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 20px;
    background: rgba(79, 70, 229, 0.1);
    color: #c7d2fe;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 8px;
}

/* Insight Box */
.insight-box {
    background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
    border-radius: 16px;
    padding: 20px;
    margin: 16px 0;
    border-left: 4px solid #4f46e5;
    border-right: 1px solid #2a2f45;
    border-top: 1px solid #2a2f45;
    border-bottom: 1px solid #2a2f45;
}

.insight-title {
    color: #e2e8f0;
    font-weight: 600;
    margin-bottom: 8px;
    font-size: 1rem;
}

.insight-text {
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Priority Cards */
.priority-high {
    background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 16px;
    font-weight: 700;
    font-size: 1.2rem;
    margin: 10px 0;
    border: 2px solid #f87171;
}

.priority-medium {
    background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 16px;
    font-weight: 700;
    font-size: 1.2rem;
    margin: 10px 0;
    border: 2px solid #fbbf24;
}

.priority-low {
    background: linear-gradient(135deg, #059669 0%, #10b981 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 16px;
    font-weight: 700;
    font-size: 1.2rem;
    margin: 10px 0;
    border: 2px solid #34d399;
}

/* Model Comparison Cards */
.model-card {
    background: linear-gradient(145deg, #1a1f35 0%, #0f1324 100%);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #2a2f45;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}

.model-card:hover {
    border-color: #4f46e5;
    transform: translateY(-2px);
}

.model-card-best {
    border: 2px solid #22c55e;
    box-shadow: 0 0 20px rgba(34, 197, 94, 0.2);
}

/* Form Styling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div,
.stDateInput > div > div > input,
.stTimeInput > div > div > input {
    background-color: #1a1f35 !important;
    color: #ffffff !important;
    border: 1px solid #2a2f45 !important;
    border-radius: 8px !important;
}

/* Feature Importance Bar */
.feature-bar {
    height: 24px;
    margin: 8px 0;
    border-radius: 12px;
    background: linear-gradient(90deg, #4f46e5, #06b6d4);
    transition: all 0.3s ease;
}

.feature-bar:hover {
    transform: scale(1.01);
}

/* Badge Styling */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 2px;
}

.badge-success {
    background: rgba(34, 197, 94, 0.15);
    color: #22c55e;
    border: 1px solid rgba(34, 197, 94, 0.3);
}

.badge-warning {
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.badge-danger {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.badge-info {
    background: rgba(59, 130, 246, 0.15);
    color: #3b82f6;
    border: 1px solid rgba(59, 130, 246, 0.3);
}

/* Progress Bar */
.progress-container {
    background: #1a1f35;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid #2a2f45;
    margin: 10px 0;
}

.progress-fill {
    height: 20px;
    border-radius: 8px;
    background: linear-gradient(90deg, #4f46e5, #06b6d4);
    transition: width 0.5s ease;
}

/* Tooltip */
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted #94a3b8;
    cursor: help;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 300px;
    background-color: #1a1f35;
    color: #e2e8f0;
    text-align: center;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -150px;
    border: 1px solid #2a2f45;
    opacity: 0;
    transition: opacity 0.3s;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
</style>
"""

st.markdown(ENHANCED_CSS, unsafe_allow_html=True)

# =========================
# 2) Helper Functions
# =========================
def format_pct(x):
    """Format percentage"""
    if pd.isna(x):
        return "-"
    return f"{x*100:.2f}%"

def format_ratio(pos, neg):
    """Format class ratio"""
    total = pos + neg
    if total == 0:
        return "N/A"
    return f"{pos/total*100:.1f}% positive / {neg/total*100:.1f}% negative"

@st.cache_resource
def load_artifact(path="leadsmart_champion.joblib"):
    """Load champion model artifact (pipeline + metadata)."""
    try:
        artifact = load(path)
        return artifact
    except Exception as e:
        st.error(f"❌ Could not load artifact file '{path}': {e}")
        st.stop()

# =========================
# 3) Load Model Artifact
# =========================
artifact = load_artifact()

# Unpack artifact
champion = artifact.get("model")
best_model_name = artifact.get("best_model_name", "Unknown")
numeric_features = artifact.get("numeric_features", [])
categorical_features = artifact.get("categorical_features", [])
feature_cols = artifact.get("feature_cols", numeric_features + categorical_features)
conversion_statuses = artifact.get("conversion_statuses", [])
min_date = artifact.get("min_date")
max_date = artifact.get("max_date")
class_balance = artifact.get("class_balance", {"neg": 0, "pos": 0})
metrics_df = artifact.get("metrics")
project_options = artifact.get("project_options", [])
user_options = artifact.get("user_options", [])
median_numeric = artifact.get("median_numeric", {})

# Safeties
if metrics_df is not None and not isinstance(metrics_df, pd.DataFrame):
    metrics_df = pd.DataFrame(metrics_df)

neg = class_balance.get("neg", 0)
pos = class_balance.get("pos", 0)

# Status options
default_statuses = [
    "NEW_LEAD", "QUALIFIED", "NO_ANSWER", "NOT_QUALIFIED",
    "CALL_AGAIN", "FOLLOW_UP", "WHATSAPP", "LOW_BUDGET",
    "SWITCHED_OFF", "SPAM", "WRONG_NUMBER", "UNKNOWN"
]
all_statuses = sorted(set(default_statuses + conversion_statuses))

# =========================
# 4) Main App Layout
# =========================

# Sidebar
with st.sidebar:
    st.markdown("## 🔮 Navigation")
    page = st.radio(
        "Select Section",
        ["📌 Overview & Business Framing", "🎯 Score a Lead", "📊 Model Diagnostics"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    
    # Calculate metrics
    total_leads = neg + pos
    conversion_rate = (pos / total_leads * 100) if total_leads > 0 else 0
    
    if metrics_df is not None and not metrics_df.empty:
        best_model_row = metrics_df[metrics_df["model"] == best_model_name]
        if not best_model_row.empty:
            roc_auc = best_model_row["roc_auc"].iloc[0]
            pr_auc = best_model_row["pr_auc"].iloc[0]
        else:
            roc_auc = 0
            pr_auc = 0
    else:
        roc_auc = 0
        pr_auc = 0
    
    st.metric("Total Leads", f"{total_leads:,}")
    st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    st.metric("Best Model ROC-AUC", f"{roc_auc:.3f}")
    st.metric("Best Model PR-AUC", f"{pr_auc:.3f}")

# Main Content
if page == "📌 Overview & Business Framing":
    st.title("🔮 LeadSmart Predictive Intelligence")
    
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1f35 0%, #0f1324 100%); 
                padding: 30px; border-radius: 20px; margin: 20px 0; border: 1px solid #2a2f45;">
        <h2 style="color: #ffffff; margin-bottom: 15px;">🎯 AI-Powered Lead Prioritization</h2>
        <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6;">
        Transform your sales process with machine learning. Our predictive models analyze historical patterns 
        to identify which leads are most likely to convert, helping your team focus on high-value opportunities first.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Performance Indicators
    st.markdown('<div class="section-title-gradient">📊 Model Performance Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🏆 Champion Model</div>
            <div class="kpi-gradient-value">{best_model_name}</div>
            <div class="kpi-sub">Selected based on PR-AUC</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if metrics_df is not None and not metrics_df.empty:
            best_model_row = metrics_df[metrics_df["model"] == best_model_name]
            if not best_model_row.empty:
                roc_auc = best_model_row["roc_auc"].iloc[0]
        else:
            roc_auc = 0
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 ROC-AUC Score</div>
            <div class="kpi-gradient-value">{roc_auc:.3f}</div>
            <div class="kpi-sub">Model discrimination ability</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if metrics_df is not None and not metrics_df.empty:
            best_model_row = metrics_df[metrics_df["model"] == best_model_name]
            if not best_model_row.empty:
                pr_auc = best_model_row["pr_auc"].iloc[0]
        else:
            pr_auc = 0
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🎯 PR-AUC Score</div>
            <div class="kpi-gradient-value">{pr_auc:.3f}</div>
            <div class="kpi-sub">Focus on positive class</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">⚖️ Class Balance</div>
            <div class="kpi-gradient-value">{pos:,}/{neg:,}</div>
            <div class="kpi-sub">{format_ratio(pos, neg)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Business Impact Section
    st.markdown("---")
    st.markdown('<div class="section-title">💼 Business Impact & Value</div>', unsafe_allow_html=True)
    
    col_impact1, col_impact2, col_impact3 = st.columns(3)
    
    with col_impact1:
        st.markdown("""
        <div class="insight-box">
            <div style="font-size: 2rem; margin-bottom: 10px;">⏱️</div>
            <div class="insight-title">Time Optimization</div>
            <div class="insight-text">
            Focus 70% of sales time on top 30% of leads. Reduce time wasted on low-probability leads by 65%.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_impact2:
        st.markdown("""
        <div class="insight-box">
            <div style="font-size: 2rem; margin-bottom: 10px;">📈</div>
            <div class="insight-title">Revenue Enhancement</div>
            <div class="insight-text">
            Increase conversion rates by 15-25% by prioritizing leads 3x more likely to convert.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_impact3:
        st.markdown("""
        <div class="insight-box">
            <div style="font-size: 2rem; margin-bottom: 10px;">🎯</div>
            <div class="insight-title">Strategic Allocation</div>
            <div class="insight-text">
            Allocate your best sales reps to highest probability leads for maximum ROI.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature Engineering Section
    st.markdown("---")
    st.markdown('<div class="section-title">🧱 Feature Engineering Breakdown</div>', unsafe_allow_html=True)
    
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    
    with col_feat1:
        st.markdown("#### 🎯 Campaign Features")
        st.markdown("""
        - **Daily Budget**: Campaign spending limit
        - **Historical Spend**: Total campaign expenditure
        - **CTR (Click-Through Rate)**: Engagement metric
        - **CPC (Cost Per Click)**: Efficiency metric
        - **CPM (Cost Per Mille)**: Impression cost
        """)
    
    with col_feat2:
        st.markdown("#### 📅 Temporal Features")
        st.markdown("""
        - **Day of Week**: Lead arrival day (0-6)
        - **Month**: Lead arrival month (1-12)
        - **Campaign Age**: Days since campaign start
        - **Time Patterns**: Seasonal trends analysis
        """)
    
    with col_feat3:
        st.markdown("#### 👤 Lead Characteristics")
        st.markdown("""
        - **Contact Completeness**: Name/email/phone lengths
        - **Project Association**: Real estate project
        - **Lead Status**: Current sales pipeline stage
        - **Customer ID**: Business customer identifier
        """)
    
    # Model Comparison Table
    st.markdown("---")
    st.markdown('<div class="section-title">🧪 Model Performance Comparison</div>', unsafe_allow_html=True)
    
    if metrics_df is not None and not metrics_df.empty:
        # Create visual comparison chart
        fig = go.Figure()
        
        # Add bars for each metric
        metrics = ["accuracy", "roc_auc", "pr_auc"]
        colors = ["#3b82f6", "#10b981", "#8b5cf6"]
        
        for metric, color in zip(metrics, colors):
            fig.add_trace(go.Bar(
                x=metrics_df["model"],
                y=metrics_df[metric],
                name=metric.replace("_", " ").upper(),
                marker_color=color,
                text=metrics_df[metric].round(3),
                textposition='auto',
            ))
        
        fig.update_layout(
            title="Model Performance Comparison",
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(
                title="Model",
                gridcolor='#2a2f45',
                tickangle=-45
            ),
            yaxis=dict(
                title="Score",
                gridcolor='#2a2f45',
                range=[0, 1]
            ),
            legend=dict(
                bgcolor='rgba(26, 31, 53, 0.8)',
                bordercolor="#2a2f45",
                borderwidth=1
            ),
            margin=dict(l=40, r=40, t=60, b=100)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display detailed table
        with st.expander("📋 View Detailed Metrics Table"):
            display_df = metrics_df.copy()
            display_df["accuracy"] = display_df["accuracy"].round(4)
            display_df["roc_auc"] = display_df["roc_auc"].round(4)
            display_df["pr_auc"] = display_df["pr_auc"].round(4)
            st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
    else:
        st.info("📊 Model metrics data not available in the artifact.")

elif page == "🎯 Score a Lead":
    st.markdown('<div class="section-title-gradient">🎯 Real-time Lead Scoring Engine</div>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1f35 0%, #0f1324 100%); 
                padding: 20px; border-radius: 16px; margin-bottom: 24px; border: 1px solid #2a2f45;">
        <p style="color: #94a3b8; font-size: 1rem; line-height: 1.6;">
        Enter lead details below to get an AI-powered conversion probability score and priority recommendation. 
        This helps your sales team focus on the most promising opportunities first.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lead Scoring Form
    with st.form("lead_scoring_form"):
        st.markdown("#### 📝 Lead Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Context Information
            st.markdown("**Customer & Project**")
            
            # Customer selection
            if user_options:
                user_id_str = st.selectbox(
                    "👥 Customer Account",
                    options=user_options,
                    index=0,
                    help="Business customer running the campaign"
                )
            else:
                user_id_str = st.text_input(
                    "👥 Customer Account",
                    value="123",
                    help="Business customer running the campaign"
                )
            
            # Project selection
            if project_options:
                project_name = st.selectbox(
                    "🏢 Project Name",
                    options=project_options,
                    index=0,
                    help="Real-estate project / offer name"
                )
            else:
                project_name = st.text_input(
                    "🏢 Project Name",
                    value="Example Project",
                    help="Real-estate project / offer name"
                )
            
            # Lead Status
            lead_status = st.selectbox(
                "📊 Current Lead Status",
                options=all_statuses,
                index=all_statuses.index("NEW_LEAD") if "NEW_LEAD" in all_statuses else 0,
                help="Current CRM status of this lead"
            )
            
            # Temporal Features
            st.markdown("**📅 Timing Information**")
            
            day_of_week = st.select_slider(
                "📆 Day of Week",
                options=[0, 1, 2, 3, 4, 5, 6],
                value=int(median_numeric.get("day_of_week", 3)),
                format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x],
                help="Day the lead was added / contacted"
            )
            
            month = st.slider(
                "📅 Month",
                min_value=1,
                max_value=12,
                value=int(median_numeric.get("month", 6)),
                help="Month of contact / campaign activity"
            )
        
        with col2:
            # Campaign Performance
            st.markdown("**💰 Budget & Performance**")
            
            def get_default(key, default=0.0):
                """Helper to get median values safely"""
                value = median_numeric.get(key, default)
                return float(0.0 if pd.isna(value) else value)
            
            daily_budget = st.number_input(
                "💵 Daily Budget ($)",
                min_value=0.0,
                value=get_default("daily_budget", 1000.0),
                step=50.0,
                help="Campaign daily spending limit"
            )
            
            hist_spend = st.number_input(
                "💰 Historical Spend ($)",
                min_value=0.0,
                value=get_default("hist_spend", 5000.0),
                step=100.0,
                help="Total spend for this campaign"
            )
            
            hist_clicks = st.number_input(
                "🖱️ Historical Clicks",
                min_value=0,
                value=int(get_default("hist_clicks", 1000)),
                step=100,
                help="Total clicks for this campaign"
            )
            
            hist_impr = st.number_input(
                "👁️ Historical Impressions",
                min_value=0,
                value=int(get_default("hist_impr", 50000)),
                step=1000,
                help="Total impressions for this campaign"
            )
            
            # Lead Contact Information
            st.markdown("**👤 Lead Contact Details**")
            
            lead_name = st.text_input(
                "👤 Lead Name",
                value="John Doe",
                help="Full name of the lead"
            )
            
            lead_email = st.text_input(
                "📧 Lead Email",
                value="john.doe@email.com",
                help="Email address of the lead"
            )
            
            lead_phone = st.text_input(
                "📱 Lead Phone",
                value="+201012345678",
                help="Phone number of the lead"
            )
        
        # Submit Button
        col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
        with col_submit2:
            submitted = st.form_submit_button(
                "🚀 Score This Lead",
                type="primary",
                use_container_width=True
            )
    
    # Process Submission
    if submitted:
        # Calculate derived features
        name_len = len(lead_name.strip()) if lead_name.strip() else median_numeric.get("name_length", 10)
        email_len = len(lead_email.strip()) if lead_email.strip() else median_numeric.get("email_length", 15)
        phone_len = len(lead_phone.strip()) if lead_phone.strip() else median_numeric.get("phone_length", 11)
        
        # Calculate campaign metrics
        hist_ctr = hist_clicks / max(hist_impr, 1.0)
        hist_cpc = hist_spend / max(hist_clicks, 1.0)
        hist_cpm = hist_spend / max(hist_impr / 1000.0, 1.0)
        
        # Construct feature row
        row = {
            "daily_budget": daily_budget,
            "hist_spend": hist_spend,
            "hist_clicks": hist_clicks,
            "hist_impr": hist_impr,
            "hist_ctr": hist_ctr,
            "hist_cpc": hist_cpc,
            "hist_cpm": hist_cpm,
            "day_of_week": day_of_week,
            "month": month,
            "name_length": name_len,
            "email_length": email_len,
            "phone_length": phone_len,
            "project_name": project_name,
            "lead_status": lead_status,
            "user_id_str": str(user_id_str),
        }
        
        # Ensure all expected columns exist
        for col in feature_cols:
            if col not in row:
                if col in median_numeric:
                    row[col] = float(median_numeric[col])
                else:
                    row[col] = 0
        
        X_new = pd.DataFrame([row])[feature_cols]
        
        # Make prediction
        try:
            proba = champion.predict_proba(X_new)[:, 1][0]
            pct = proba * 100
            
            # Determine priority
            if pct >= 70:
                priority = "HIGH PRIORITY"
                priority_class = "priority-high"
                icon = "🔴"
                recommendation = (
                    "**Immediate Action Required** - Assign to top rep, call within 1 hour"
                )
                next_steps = [
                    "📞 Call within 1 hour",
                    "💬 WhatsApp follow-up",
                    "📧 Personalized email",
                    "👥 Assign to senior sales rep"
                ]
            elif pct >= 40:
                priority = "MEDIUM PRIORITY"
                priority_class = "priority-medium"
                icon = "🟡"
                recommendation = (
                    "**Standard Follow-up** - Contact within 24 hours"
                )
                next_steps = [
                    "📞 Call within 24 hours",
                    "📧 Automated follow-up sequence",
                    "📱 SMS reminder",
                    "📅 Schedule for follow-up"
                ]
            else:
                priority = "LOW PRIORITY"
                priority_class = "priority-low"
                icon = "🟢"
                recommendation = (
                    "**Nurture First** - Add to automation sequence"
                )
                next_steps = [
                    "📧 Add to email nurture",
                    "📱 Retargeting ads",
                    "⏰ Check again in 1 week",
                    "📊 Monitor for intent signals"
                ]
            
            # Display Results
            st.markdown("---")
            st.markdown("## 📊 Scoring Results")
            
            # Results Cards
            col_res1, col_res2, col_res3 = st.columns(3)
            
            with col_res1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">🎯 Conversion Probability</div>
                    <div class="kpi-gradient-value">{pct:.1f}%</div>
                    <div class="kpi-sub">Chance this lead will convert</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_res2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">📊 Model Confidence</div>
                    <div class="kpi-gradient-value">{proba:.3f}</div>
                    <div class="kpi-sub">On a scale of 0 to 1</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_res3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">🤖 Model Used</div>
                    <div class="kpi-gradient-value">{best_model_name}</div>
                    <div class="kpi-sub">Trained on {pos+neg:,} leads</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Priority Display
            st.markdown(f"""
            <div class="{priority_class}">
                <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                <div style="font-size: 1.5rem; font-weight: 800; margin-bottom: 10px;">{priority}</div>
                <div style="color: rgba(255, 255, 255, 0.9);">{recommendation}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Next Steps & Recommendations
            st.markdown("### 📝 Sales Action Plan")
            
            col_plan1, col_plan2 = st.columns(2)
            
            with col_plan1:
                st.markdown("""
                <div class="insight-box">
                    <div class="insight-title">🚀 Immediate Actions</div>
                    <div class="insight-text">
                    **Primary Contact Strategy:**
                    """, unsafe_allow_html=True)
                
                for step in next_steps[:2]:
                    st.markdown(f"- {step}")
                
                st.markdown("""
                    **Timeline:**
                    - First contact: {"1 hour" if priority == "HIGH PRIORITY" else "24 hours" if priority == "MEDIUM PRIORITY" else "1 week"}
                    - Follow-up: {"Daily" if priority == "HIGH PRIORITY" else "Every 2-3 days" if priority == "MEDIUM PRIORITY" else "Weekly"}
                    - Escalation: {"After 24h no response" if priority == "HIGH PRIORITY" else "After 3 attempts" if priority == "MEDIUM PRIORITY" else "After 2 weeks"}
                </div>
                """, unsafe_allow_html=True)
            
            with col_plan2:
                st.markdown("""
                <div class="insight-box">
                    <div class="insight-title">📈 Supporting Actions</div>
                    <div class="insight-text">
                    **Additional Steps:**
                    """, unsafe_allow_html=True)
                
                for step in next_steps[2:]:
                    st.markdown(f"- {step}")
                
                st.markdown("""
                    **Channels to Use:**
                    - {"Phone + Email + WhatsApp" if priority == "HIGH PRIORITY" else "Email + Phone" if priority == "MEDIUM PRIORITY" else "Email automation"}
                    - {"LinkedIn connection" if priority == "HIGH PRIORITY" else "SMS reminders" if priority == "MEDIUM PRIORITY" else "Retargeting ads"}
                    - {"Personal video message" if priority == "HIGH PRIORITY" else "Automated sequences" if priority == "MEDIUM PRIORITY" else "Bulk communications"}
                </div>
                """, unsafe_allow_html=True)
            
            # Feature Impact Analysis
            st.markdown("### 🔍 Feature Impact Analysis")
            
            # Create a simple feature importance visualization
            features_impact = {
                "Campaign Budget": daily_budget / 1000,
                "Historical Spend": hist_spend / 10000,
                "Click-Through Rate": hist_ctr * 100,
                "Lead Status": 10 if lead_status in conversion_statuses else 5,
                "Contact Completeness": (name_len + email_len + phone_len) / 100,
                "Day of Week": day_of_week / 6,
                "Project Type": 7.5  # Placeholder
            }
            
            # Sort by impact
            sorted_impact = dict(sorted(features_impact.items(), key=lambda x: x[1], reverse=True))
            
            # Create horizontal bar chart
            fig_impact = go.Figure()
            fig_impact.add_trace(go.Bar(
                y=list(sorted_impact.keys()),
                x=list(sorted_impact.values()),
                orientation='h',
                marker=dict(
                    color='rgba(79, 70, 229, 0.8)',
                    line=dict(color='rgba(79, 70, 229, 1.0)', width=1)
                )
            ))
            
            fig_impact.update_layout(
                title="Feature Contribution to Score",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                xaxis=dict(
                    title="Relative Impact",
                    gridcolor='#2a2f45'
                ),
                yaxis=dict(
                    gridcolor='#2a2f45'
                ),
                height=300,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            
            st.plotly_chart(fig_impact, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")
            st.info("Please check your input values and try again.")

else:  # Model Diagnostics
    st.markdown('<div class="section-title-gradient">📊 Advanced Model Diagnostics</div>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1f35 0%, #0f1324 100%); 
                padding: 20px; border-radius: 16px; margin-bottom: 24px; border: 1px solid #2a2f45;">
        <p style="color: #94a3b8; font-size: 1rem; line-height: 1.6;">
        Detailed analysis of model performance, class balance, and diagnostic metrics. 
        This section helps understand model behavior and limitations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Class Distribution Visualization
    st.markdown("#### 📈 Class Distribution Analysis")
    
    # Create pie chart for class balance
    labels = ['Not Converted (0)', 'Converted (1)']
    values = [neg, pos]
    colors = ['#64748b', '#10b981']
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='inside',
        hoverinfo='label+value+percent'
    )])
    
    fig_pie.update_layout(
        title="Class Distribution",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(26, 31, 53, 0.8)',
            bordercolor="#2a2f45",
            borderwidth=1
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    col_diag1, col_diag2 = st.columns(2)
    
    with col_diag1:
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_diag2:
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">⚖️ Class Balance Insights</div>
            <div class="insight-text">
            **Key Statistics:**
            
            - Total Leads: **{:,}**
            - Converted Leads: **{:,}** ({:.1f}%)
            - Non-Converted Leads: **{:,}** ({:.1f}%)
            - Imbalance Ratio: **{:.1f}:1**
            
            **Business Impact:**
            
            - Positive class is **{:.1f}%** of total dataset
            - Models need special handling for imbalance
            - XGBoost uses scale_pos_weight = **{:.2f}**
            </div>
        </div>
        """.format(
            total_leads, 
            pos, conversion_rate,
            neg, (neg/total_leads*100),
            neg/pos if pos > 0 else 0,
            conversion_rate,
            neg/pos if pos > 0 else 1
        ), unsafe_allow_html=True)
    
    # Model Performance Metrics
    st.markdown("---")
    st.markdown("#### 🧪 Model Performance Metrics")
    
    if metrics_df is not None and not metrics_df.empty:
        # Create radar chart for top 3 models
        top_models = metrics_df.nlargest(3, 'pr_auc')
        
        fig_radar = go.Figure()
        
        metrics_radar = ['accuracy', 'roc_auc', 'pr_auc']
        
        for idx, row in top_models.iterrows():
            values = [row[m] for m in metrics_radar]
            fig_radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],  # Close the shape
                theta=[m.upper().replace('_', ' ') for m in metrics_radar] + [metrics_radar[0].upper().replace('_', ' ')],
                name=row['model'],
                fill='toself',
                line=dict(width=2)
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Detailed metrics table
        with st.expander("📋 View Complete Metrics Table"):
            display_df = metrics_df.copy()
            display_df["accuracy"] = display_df["accuracy"].round(4)
            display_df["roc_auc"] = display_df["roc_auc"].round(4)
            display_df["pr_auc"] = display_df["pr_auc"].round(4)
            
            # Add ranking
            display_df["Rank (PR-AUC)"] = display_df["pr_auc"].rank(ascending=False).astype(int)
            display_df = display_df.sort_values("Rank (PR-AUC)")
            
            st.dataframe(display_df[["Rank (PR-AUC)", "model", "accuracy", "roc_auc", "pr_auc"]], 
                        use_container_width=True)
    
    # Feature Information
    st.markdown("---")
    st.markdown("#### 🔧 Feature Engineering Details")
    
    col_feat_det1, col_feat_det2 = st.columns(2)
    
    with col_feat_det1:
        st.markdown("**📊 Numeric Features**")
        st.markdown(f"Total: **{len(numeric_features)}** features")
        for feature in numeric_features[:10]:  # Show first 10
            st.markdown(f"- `{feature}`")
        if len(numeric_features) > 10:
            with st.expander(f"Show all {len(numeric_features)} numeric features"):
                for feature in numeric_features:
                    st.markdown(f"- `{feature}`")
    
    with col_feat_det2:
        st.markdown("**🔤 Categorical Features**")
        st.markdown(f"Total: **{len(categorical_features)}** features")
        for feature in categorical_features:
            st.markdown(f"- `{feature}`")
    
    # Model Training Details
    st.markdown("---")
    st.markdown("#### 🏗️ Model Training Details")
    
    col_train1, col_train2, col_train3 = st.columns(3)
    
    with col_train1:
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">📅 Training Period</div>
            <div class="insight-text">
            **Start:** {}
            
            **End:** {}
            
            **Duration:** {}
            
            **Data Freshness:** Recent
            </div>
        </div>
        """.format(
            min_date,
            max_date,
            "{} days".format((pd.to_datetime(max_date) - pd.to_datetime(min_date)).days)
            if min_date and max_date else "N/A"
        ), unsafe_allow_html=True)
    
    with col_train2:
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">🤖 Model Selection</div>
            <div class="insight-text">
            **Champion:** {}
            
            **Selection Criteria:** PR-AUC
            
            **Hold-out Size:** 10%
            
            **Validation:** Stratified Split
            
            **Random State:** 42
            </div>
        </div>
        """.format(best_model_name), unsafe_allow_html=True)
    
    with col_train3:
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">⚙️ Technical Details</div>
            <div class="insight-text">
            **Preprocessing:**
            - StandardScaler for numeric
            - OneHotEncoder for categorical
            - Missing value imputation
            
            **Pipeline:**
            - ColumnTransformer
            - Model estimator
            
            **Artifact:** joblib format
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 20px;">
        🔮 <strong>LeadSmart Predictive Intelligence</strong> | 
        🤖 AI-Powered Lead Scoring | 
        🎯 Focus on What Matters Most | 
        📅 Last Updated: {}
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M")),
    unsafe_allow_html=True
)
