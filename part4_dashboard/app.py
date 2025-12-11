# Campaign Strategic Decision System - Enhanced Version
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
BASE_DIR = os.path.dirname(__file__)


# =========================
# 1) ENHANCED Page Config + CSS
# =========================
st.set_page_config(
    page_title="LeadSmart – Campaign Decision System",
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

/* Health Status Badges */
.health-hero {
    background: linear-gradient(135deg, #059669 0%, #10b981 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
}

.health-good {
    background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
}

.health-mixed {
    background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
}

.health-bad {
    background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
}

.health-needs-data {
    background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
}

/* Form Styling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div,
.stDateInput > div > div > input {
    background-color: #1a1f35 !important;
    color: #ffffff !important;
    border: 1px solid #2a2f45 !important;
    border-radius: 8px !important;
}

/* Action Cards */
.action-card {
    background: linear-gradient(145deg, #1a1f35 0%, #0f1324 100%);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #2a2f45;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}

.action-card:hover {
    border-color: #4f46e5;
    transform: translateY(-2px);
}

.action-scale {
    border-left: 4px solid #10b981;
}

.action-keep {
    border-left: 4px solid #3b82f6;
}

.action-optimize {
    border-left: 4px solid #f59e0b;
}

.action-stop {
    border-left: 4px solid #ef4444;
}

.action-monitor {
    border-left: 4px solid #6b7280;
}

/* Campaign Card */
.campaign-card {
    background: linear-gradient(145deg, #1a1f35 0%, #0f1324 100%);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #2a2f45;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}

.campaign-card:hover {
    border-color: #4f46e5;
    transform: translateY(-2px);
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
</style>
"""

st.markdown(ENHANCED_CSS, unsafe_allow_html=True)

# =========================
# 2) Helper Functions
# =========================
def format_money(x: float) -> str:
    """Format money values"""
    if pd.isna(x) or x == 0:
        return "$0"
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:.2f}M"
    if abs(x) >= 1_000:
        return f"${x/1_000:.1f}K"
    return f"${x:,.0f}"

def format_pct(x: float) -> str:
    """Format percentage values"""
    if pd.isna(x):
        return "0.0%"
    return f"{x*100:.1f}%"

def get_health_color(health_bucket):
    """Get color for health bucket"""
    colors = {
        "HERO": "#10b981",
        "GOOD": "#3b82f6",
        "MIXED": "#f59e0b",
        "BAD": "#ef4444",
        "NEEDS_MORE_DATA": "#6b7280"
    }
    return colors.get(health_bucket, "#6b7280")

def get_action_icon(action):
    """Get icon for action"""
    icons = {
        "Scale Up": "🚀",
        "Keep Running": "📈",
        "Optimize (Targeting / Creative / Audience)": "🔧",
        "Stop / Reallocate": "⏹️",
        "Keep Monitoring": "👀"
    }
    return icons.get(action, "📊")

# =========================
# 3) Data Loading & Processing
# =========================
@st.cache_data
def load_and_prepare():
    """Load CSVs and build campaign-level performance table."""
    
    # Load data
    campaign_leads = pd.read_csv(os.path.join(BASE_DIR, "campaign_leads.csv"))
    campaigns = pd.read_csv(os.path.join(BASE_DIR, "campaigns.csv"))
    insights = pd.read_csv(os.path.join(BASE_DIR, "insights.csv"))


    # Rename IDs
    campaign_leads = campaign_leads.rename(columns={"id": "lead_id"})
    campaigns = campaigns.rename(columns={"id": "campaign_id"})

    # Parse dates
    campaign_leads["added_date"] = pd.to_datetime(campaign_leads["added_date"])
    campaign_leads["date"] = campaign_leads["added_date"].dt.date

    insights["created_at"] = pd.to_datetime(insights["created_at"])
    insights["date"] = insights["created_at"].dt.date

    # Define conversion statuses
    conversion_statuses = [
        "DONE_DEAL", "ALREADY_BOUGHT", "RESALE_REQUEST",
        "MEETING_DONE", "HIGH_INTEREST", "QUALIFIED",
    ]
    
    campaign_leads["is_converted"] = campaign_leads["lead_status"].isin(conversion_statuses)

    # Enrich leads with campaign info
    leads_with_campaign = campaign_leads.merge(
        campaigns[["campaign_id", "user_id", "project_name", "daily_budget"]],
        on="campaign_id",
        how="left",
    )

    # Build campaign-level performance
    spend_agg = (
        insights.groupby("campaign_id", as_index=False)
        .agg(
            total_spend=("spend", "sum"),
            days_active_insights=("date", "nunique"),
        )
    )

    leads_agg = (
        leads_with_campaign.groupby("campaign_id", as_index=False)
        .agg(
            total_leads=("lead_id", "count"),
            converted_leads=("is_converted", "sum"),
            days_active_leads=("date", "nunique"),
        )
    )

    campaign_perf = spend_agg.merge(leads_agg, on="campaign_id", how="outer")

    # Add campaign meta
    campaign_info = campaigns[["campaign_id", "project_name", "user_id", "daily_budget"]]
    campaign_perf = campaign_perf.merge(campaign_info, on="campaign_id", how="left")

    # Calculate days active
    campaign_perf["days_active"] = campaign_perf["days_active_insights"].fillna(
        campaign_perf["days_active_leads"]
    )
    campaign_perf.drop(columns=["days_active_insights", "days_active_leads"], inplace=True)

    # Fill missing values
    for col in ["total_spend", "total_leads", "converted_leads", "days_active"]:
        campaign_perf[col] = campaign_perf[col].fillna(0)

    # Calculate KPIs
    campaign_perf["conversion_rate"] = np.where(
        campaign_perf["total_leads"] > 0,
        campaign_perf["converted_leads"] / campaign_perf["total_leads"],
        0.0,
    )

    campaign_perf["cpl"] = np.where(
        campaign_perf["total_leads"] > 0,
        campaign_perf["total_spend"] / campaign_perf["total_leads"],
        np.nan,
    )

    campaign_perf["leads_per_day"] = np.where(
        campaign_perf["days_active"] > 0,
        campaign_perf["total_leads"] / campaign_perf["days_active"],
        np.nan,
    )

    campaign_perf["spend_per_day"] = np.where(
        campaign_perf["days_active"] > 0,
        campaign_perf["total_spend"] / campaign_perf["days_active"],
        np.nan,
    )

    # Data period
    min_date = campaign_leads["added_date"].min().date()
    max_date = campaign_leads["added_date"].max().date()

    return leads_with_campaign, campaign_perf, (min_date, max_date), conversion_statuses

# =========================
# 4) Campaign Classification
# =========================
leads_with_campaign, campaign_perf, (min_date, max_date), conversion_statuses = load_and_prepare()

# Calculate percentiles
perf_non_empty = campaign_perf[
    (campaign_perf["total_leads"] >= 10) & (campaign_perf["total_spend"] > 0)
].copy()

conv_p25, conv_p50, conv_p75 = np.nanpercentile(
    perf_non_empty["conversion_rate"].dropna(),
    [25, 50, 75],
)

cpl_p25, cpl_p50, cpl_p75 = np.nanpercentile(
    perf_non_empty["cpl"].dropna(),
    [25, 50, 75],
)

def classify_campaign(row):
    """Rule-based health classification"""
    conv = row["conversion_rate"]
    cpl = row["cpl"]
    leads = row["total_leads"]
    spend = row["total_spend"]
    days = row["days_active"]

    # Not enough data
    if (leads < 10) or (spend <= 0) or (days < 3):
        return "NEEDS_MORE_DATA", "Keep Monitoring", "👀"

    # BAD – high CPL, zero conversions
    if (leads >= 20) and (conv == 0) and (cpl >= cpl_p75):
        return "BAD", "Stop / Reallocate", "⏹️"

    # HERO – high conversion, very efficient
    if (conv >= conv_p75) and (cpl <= cpl_p25):
        return "HERO", "Scale Up", "🚀"

    # GOOD – high conversion, acceptable cost
    if (conv >= conv_p75) and (cpl <= cpl_p50):
        return "GOOD", "Keep Running", "📈"

    # MIXED – some conversions but expensive
    if (conv > 0) and (cpl > cpl_p50):
        return "MIXED", "Optimize (Targeting / Creative / Audience)", "🔧"

    # Default
    return "NEEDS_MORE_DATA", "Keep Monitoring", "👀"

# Apply classification
campaign_scored = campaign_perf.copy()
classification_results = campaign_scored.apply(
    lambda r: pd.Series(classify_campaign(r)),
    axis=1
)
campaign_scored[["health_bucket", "recommended_action", "action_icon"]] = classification_results

# Summary table
summary_table = (
    campaign_scored.groupby(["health_bucket", "recommended_action"], as_index=False)
    .agg(
        n_campaigns=("campaign_id", "count"),
        total_spend=("total_spend", "sum"),
    )
    .sort_values("n_campaigns", ascending=False)
)

# =========================
# 5) Sidebar Configuration
# =========================
with st.sidebar:
    st.markdown("## 🔍 Filters")
    
    # Customer filter
    all_users = sorted(campaign_scored["user_id"].dropna().astype(int).unique().tolist())
    user_option = st.selectbox(
        "👥 Customer",
        options=["All Customers"] + [f"Customer {u}" for u in all_users],
        index=0,
    )
    
    # Project filter
    all_projects = sorted(campaign_scored["project_name"].dropna().unique().tolist())
    project_option = st.selectbox(
        "🏢 Project",
        options=["All Projects"] + all_projects,
        index=0,
    )
    
    # Health status filter
    all_health = sorted(campaign_scored["health_bucket"].dropna().unique().tolist())
    health_option = st.selectbox(
        "📊 Health Status",
        options=["All Statuses"] + all_health,
        index=0,
    )
    
    # Action filter
    all_actions = sorted(campaign_scored["recommended_action"].dropna().unique().tolist())
    action_option = st.selectbox(
        "🎯 Recommended Action",
        options=["All Actions"] + all_actions,
        index=0,
    )
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    
    # Calculate filtered stats
    filtered = campaign_scored.copy()
    
    if user_option != "All Customers":
        selected_user = int(user_option.replace("Customer ", ""))
        filtered = filtered[filtered["user_id"] == selected_user]
    
    if project_option != "All Projects":
        filtered = filtered[filtered["project_name"] == project_option]
    
    if health_option != "All Statuses":
        filtered = filtered[filtered["health_bucket"] == health_option]
    
    if action_option != "All Actions":
        filtered = filtered[filtered["recommended_action"] == action_option]
    
    # Display stats
    total_campaigns = filtered["campaign_id"].nunique()
    total_spend = filtered["total_spend"].sum()
    total_leads = filtered["total_leads"].sum()
    total_conversions = filtered["converted_leads"].sum()
    
    st.metric("Campaigns", f"{total_campaigns:,}")
    st.metric("Total Spend", format_money(total_spend))
    st.metric("Total Leads", f"{total_leads:,}")
    st.metric("Conversions", f"{total_conversions:,}")

# =========================
# 6) Main App Layout
# =========================
tab_overview, tab_explorer, tab_recommendation = st.tabs(
    ["📌 Dashboard", "🔍 Campaign Explorer", "🎯 Recommendation Engine"]
)

# =========================
# TAB 1: Dashboard
# =========================
with tab_overview:
    st.title("🚀 Campaign Strategic Decision System")
    
    # Hero Section
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1f35 0%, #0f1324 100%); 
                padding: 30px; border-radius: 20px; margin: 20px 0; border: 1px solid #2a2f45;">
        <h2 style="color: #ffffff; margin-bottom: 15px;">📊 AI-Powered Campaign Management</h2>
        <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6;">
        Transform your marketing strategy with data-driven decisions. Our system analyzes campaign performance 
        to recommend which campaigns to scale, optimize, or stop – maximizing your ROI.
        </p>
        <div style="color: #64748b; font-size: 0.9rem; margin-top: 15px;">
        📅 Data Period: {min_date} to {max_date} • 📊 {campaign_scored["campaign_id"].nunique():,} Campaigns Analyzed
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    st.markdown('<div class="section-title-gradient">📊 Performance Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        hero_count = (campaign_scored["health_bucket"] == "HERO").sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🏆 Hero Campaigns</div>
            <div class="kpi-gradient-value">{hero_count}</div>
            <div class="kpi-sub">High conversion & low CPL</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        good_count = (campaign_scored["health_bucket"] == "GOOD").sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 Good Campaigns</div>
            <div class="kpi-gradient-value">{good_count}</div>
            <div class="kpi-sub">Solid performance, keep running</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        mixed_count = (campaign_scored["health_bucket"] == "MIXED").sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🔧 Mixed Campaigns</div>
            <div class="kpi-gradient-value">{mixed_count}</div>
            <div class="kpi-sub">Needs optimization</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        bad_count = (campaign_scored["health_bucket"] == "BAD").sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">⏹️ Bad Campaigns</div>
            <div class="kpi-gradient-value">{bad_count}</div>
            <div class="kpi-sub">Consider stopping</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Health Distribution Chart
    st.markdown("---")
    st.markdown('<div class="section-title">📈 Campaign Health Distribution</div>', unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        # Create donut chart
        health_counts = campaign_scored["health_bucket"].value_counts()
        colors = [get_health_color(bucket) for bucket in health_counts.index]
        
        fig = go.Figure(data=[go.Pie(
            labels=health_counts.index,
            values=health_counts.values,
            hole=.6,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='inside',
            hoverinfo='label+value+percent'
        )])
        
        fig.update_layout(
            title="Campaign Health Distribution",
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
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("### 📋 Health Legend")
        
        health_info = {
            "HERO": "🚀 Scale Up",
            "GOOD": "📈 Keep Running",
            "MIXED": "🔧 Optimize",
            "BAD": "⏹️ Stop/Reallocate",
            "NEEDS_MORE_DATA": "👀 Monitor"
        }
        
        for health, action in health_info.items():
            color = get_health_color(health)
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 10px 16px; 
                        border-radius: 12px; margin-bottom: 8px; font-weight: 600;">
                {health}: {action}
            </div>
            """, unsafe_allow_html=True)
    
    # Performance Matrix
    st.markdown("---")
    st.markdown('<div class="section-title">🎯 Performance Matrix: CPL vs Conversion Rate</div>', unsafe_allow_html=True)
    
    # Create scatter plot
    scatter_df = filtered.copy()
    scatter_df["conv_pct"] = scatter_df["conversion_rate"] * 100
    
    # Calculate median lines
    median_conv = scatter_df["conv_pct"].median()
    median_cpl = scatter_df["cpl"].median()
    
    fig_scatter = px.scatter(
        scatter_df,
        x="cpl",
        y="conv_pct",
        color="health_bucket",
        size="total_spend",
        hover_data=[
            "campaign_id",
            "project_name",
            "user_id",
            "total_spend",
            "total_leads",
            "converted_leads",
        ],
        labels={
            "cpl": "Cost per Lead (CPL)",
            "conv_pct": "Conversion Rate (%)",
            "health_bucket": "Health Status"
        },
        color_discrete_map={
            "HERO": "#10b981",
            "GOOD": "#3b82f6",
            "MIXED": "#f59e0b",
            "BAD": "#ef4444",
            "NEEDS_MORE_DATA": "#6b7280"
        }
    )
    
    # Add quadrant lines
    fig_scatter.add_hline(
        y=median_conv,
        line_dash="dash",
        line_color="white",
        opacity=0.3,
        annotation_text=f"Median: {median_conv:.1f}%"
    )
    
    fig_scatter.add_vline(
        x=median_cpl,
        line_dash="dash",
        line_color="white",
        opacity=0.3,
        annotation_text=f"Median: ${median_cpl:,.0f}"
    )
    
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(gridcolor='#2a2f45', title="Cost per Lead ($)"),
        yaxis=dict(gridcolor='#2a2f45', title="Conversion Rate (%)"),
        hovermode='closest',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Quadrant Explanation
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    
    with col_q1:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 12px; border: 1px solid #10b981;">
            <div style="color: #10b981; font-weight: 700; margin-bottom: 8px;">🚀 High Conv, Low CPL</div>
            <div style="color: #94a3b8; font-size: 0.9rem;">Hero campaigns - Scale budget immediately</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_q2:
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 12px; border: 1px solid #3b82f6;">
            <div style="color: #3b82f6; font-weight: 700; margin-bottom: 8px;">📈 High Conv, High CPL</div>
            <div style="color: #94a3b8; font-size: 0.9rem;">Good campaigns - Keep running, monitor costs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_q3:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.1); padding: 15px; border-radius: 12px; border: 1px solid #f59e0b;">
            <div style="color: #f59e0b; font-weight: 700; margin-bottom: 8px;">🔧 Low Conv, High CPL</div>
            <div style="color: #94a3b8; font-size: 0.9rem;">Mixed campaigns - Needs optimization</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_q4:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.1); padding: 15px; border-radius: 12px; border: 1px solid #ef4444;">
            <div style="color: #ef4444; font-weight: 700; margin-bottom: 8px;">⏹️ Very High CPL</div>
            <div style="color: #94a3b8; font-size: 0.9rem;">Bad campaigns - Consider stopping</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# TAB 2: Campaign Explorer
# =========================
with tab_explorer:
    st.markdown('<div class="section-title-gradient">🔍 Campaign Performance Explorer</div>', unsafe_allow_html=True)
    
    if filtered.empty:
        st.warning("No campaigns match the current filters. Try adjusting your filter criteria.")
    else:
        # Summary Cards
        st.markdown(f"**Showing {len(filtered):,} campaigns**")
        
        # Interactive Data Table
        st.markdown("#### 📋 Campaign Performance Table")
        
        # Create display dataframe
        display_df = filtered.copy()
        display_df = display_df[[
            "campaign_id", "project_name", "user_id", 
            "total_spend", "total_leads", "converted_leads",
            "conversion_rate", "cpl", "health_bucket", "recommended_action"
        ]]
        
        # Format columns
        display_df["total_spend"] = display_df["total_spend"].apply(format_money)
        display_df["conversion_rate"] = display_df["conversion_rate"].apply(format_pct)
        display_df["cpl"] = display_df["cpl"].apply(lambda x: f"${x:,.0f}" if not pd.isna(x) else "-")
        
        # Display with conditional formatting
        st.dataframe(
            display_df.style.apply(
                lambda x: ['background: rgba(16, 185, 129, 0.1)' if v == "HERO" 
                          else 'background: rgba(59, 130, 246, 0.1)' if v == "GOOD"
                          else 'background: rgba(245, 158, 11, 0.1)' if v == "MIXED"
                          else 'background: rgba(239, 68, 68, 0.1)' if v == "BAD"
                          else 'background: rgba(107, 114, 128, 0.1)' for v in x],
                subset=["health_bucket"]
            ),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Campaign Data",
            data=csv,
            file_name="campaign_performance.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Detailed Analysis
        st.markdown("---")
        st.markdown("#### 📊 Detailed Analysis")
        
        col_analysis1, col_analysis2 = st.columns(2)
        
        with col_analysis1:
            # Top performing campaigns
            st.markdown("##### 🏆 Top 5 Performing Campaigns")
            top_campaigns = filtered.nlargest(5, "conversion_rate")
            
            for _, row in top_campaigns.iterrows():
                st.markdown(f"""
                <div class="campaign-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 700; color: #ffffff;">Campaign {row['campaign_id']}</div>
                            <div style="color: #94a3b8; font-size: 0.9rem;">{row['project_name']}</div>
                        </div>
                        <div class="health-hero">HERO</div>
                    </div>
                    <div style="margin-top: 12px;">
                        <div style="color: #94a3b8; font-size: 0.9rem;">
                            Conversion: <span style="color: #10b981; font-weight: 600;">{row['conversion_rate']*100:.1f}%</span>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.9rem;">
                            CPL: <span style="color: #10b981; font-weight: 600;">${row['cpl']:,.0f}</span>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.9rem;">
                            Spend: <span style="color: #10b981; font-weight: 600;">{format_money(row['total_spend'])}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_analysis2:
            # Campaigns needing attention
            st.markdown("##### ⚠️ Campaigns Needing Attention")
            attention_campaigns = filtered[filtered["health_bucket"].isin(["BAD", "MIXED"])].nlargest(5, "cpl")
            
            if attention_campaigns.empty:
                st.info("No campaigns need immediate attention! 🎉")
            else:
                for _, row in attention_campaigns.iterrows():
                    health_class = "health-bad" if row["health_bucket"] == "BAD" else "health-mixed"
                    health_text = "BAD" if row["health_bucket"] == "BAD" else "MIXED"
                    
                    st.markdown(f"""
                    <div class="campaign-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight: 700; color: #ffffff;">Campaign {row['campaign_id']}</div>
                                <div style="color: #94a3b8; font-size: 0.9rem;">{row['project_name']}</div>
                            </div>
                            <div class="{health_class}">{health_text}</div>
                        </div>
                        <div style="margin-top: 12px;">
                            <div style="color: #94a3b8; font-size: 0.9rem;">
                                Conversion: <span style="color: #ef4444; font-weight: 600;">{row['conversion_rate']*100:.1f}%</span>
                            </div>
                            <div style="color: #94a3b8; font-size: 0.9rem;">
                                CPL: <span style="color: #ef4444; font-weight: 600;">${row['cpl']:,.0f}</span>
                            </div>
                            <div style="color: #94a3b8; font-size: 0.9rem;">
                                Action: <span style="color: #f59e0b; font-weight: 600;">{row['recommended_action']}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# =========================
# =========================
# TAB 3: Recommendation Engine
# =========================
with tab_recommendation:
    st.markdown('<div class="section-title-gradient">🎯 Campaign Recommendation Engine</div>', unsafe_allow_html=True)
    
    if filtered.empty:
        st.warning("No campaigns available for the current filters.")
    else:
        # Campaign Selector
        st.markdown("### 🔍 Select a Campaign to Analyze")
        
        col_sel1, col_sel2 = st.columns(2)
        
        with col_sel1:
            # Method 1: Select by Campaign ID (Dropdown)
            available_campaigns = sorted(filtered["campaign_id"].unique().tolist())
            campaign_options = {f"Campaign {campaign_id}": campaign_id for campaign_id in available_campaigns}
            
            selected_campaign_option = st.selectbox(
                "**Select Campaign ID**",
                options=["-- Choose a Campaign --"] + list(campaign_options.keys()),
                key="campaign_id_dropdown"
            )
            
            if selected_campaign_option != "-- Choose a Campaign --":
                selected_campaign_id = campaign_options[selected_campaign_option]
            else:
                selected_campaign_id = None
        
        with col_sel2:
            # Method 2: Search by Project Name (Searchable dropdown)
            # Get unique project names
            project_list = filtered["project_name"].dropna().unique().tolist()
            project_list = sorted([str(p) for p in project_list if str(p).strip() != ""])
            
            # Create a searchable dropdown
            search_term = st.text_input(
                "**🔍 Or search by project name**",
                placeholder="Type project name to search...",
                key="project_search"
            )
            
            # Filter projects based on search
            if search_term:
                matching_projects = [p for p in project_list if search_term.lower() in p.lower()]
                if matching_projects:
                    selected_project = st.selectbox(
                        "**Matching Projects**",
                        options=["-- Select a Project --"] + matching_projects,
                        key="project_select"
                    )
                    
                    if selected_project != "-- Select a Project --":
                        # Find campaign ID for the selected project
                        matching_campaigns = filtered[
                            filtered["project_name"] == selected_project
                        ]
                        if not matching_campaigns.empty:
                            selected_campaign_id = matching_campaigns.iloc[0]["campaign_id"]
                else:
                    st.info("No projects found with that name.")
            else:
                # Show all projects in a dropdown when no search term
                selected_project = st.selectbox(
                    "**Browse Projects**",
                    options=["-- Select a Project --"] + project_list,
                    key="project_browse"
                )
                
                if selected_project != "-- Select a Project --":
                    # Find campaign ID for the selected project
                    matching_campaigns = filtered[
                        filtered["project_name"] == selected_project
                    ]
                    if not matching_campaigns.empty:
                        selected_campaign_id = matching_campaigns.iloc[0]["campaign_id"]
        
        # Check if a campaign is selected
        if selected_campaign_id is None:
            st.info("👈 Please select a campaign using one of the methods above to see detailed analysis.")
            
            # Show available campaigns for quick reference
            st.markdown("### 📋 Available Campaigns")
            
            # Display campaigns in a grid
            cols = st.columns(3)
            for idx, (campaign_id, project_name) in enumerate(zip(
                filtered["campaign_id"].head(9), 
                filtered["project_name"].head(9)
            )):
                with cols[idx % 3]:
                    health_color = get_health_color(
                        filtered[filtered["campaign_id"] == campaign_id]["health_bucket"].iloc[0]
                    )
                    st.markdown(f"""
                    <div style="background: #1a1f35; padding: 15px; border-radius: 12px; margin-bottom: 10px; border-left: 4px solid {health_color};">
                        <div style="font-weight: 700; color: #ffffff; margin-bottom: 5px;">Campaign {campaign_id}</div>
                        <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 5px;">{project_name[:30]}{'...' if len(project_name) > 30 else ''}</div>
                        <div style="color: {health_color}; font-weight: 600; font-size: 0.85rem;">
                            {filtered[filtered["campaign_id"] == campaign_id]["health_bucket"].iloc[0]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if len(filtered) > 9:
                st.caption(f"Showing 9 of {len(filtered)} available campaigns. Use filters in the sidebar to narrow down.")
            
        else:
            # Get campaign data
            try:
                row = filtered[filtered["campaign_id"] == selected_campaign_id].iloc[0]
            except IndexError:
                st.error("Selected campaign not found in the filtered data.")
                st.stop()
            
            # Display Campaign Details
            st.markdown("---")
            st.markdown(f"## 📊 Analysis for Campaign **{selected_campaign_id}**")
            
            # Project name display
            st.markdown(f"**Project:** {row['project_name']} | **Customer:** {int(row['user_id'])}")
            
            # Summary Cards
            col_sum1, col_sum2, col_sum3 = st.columns(3)
            
            with col_sum1:
                health_color = get_health_color(row["health_bucket"])
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Health Status</div>
                    <div class="kpi-value" style="color: {health_color};">{row['health_bucket']}</div>
                    <div class="kpi-sub">{row['action_icon']} {row['recommended_action']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_sum2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Performance Score</div>
                    <div class="kpi-gradient-value">{row['conversion_rate']*100:.1f}%</div>
                    <div class="kpi-sub">Conversion Rate</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_sum3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Cost Efficiency</div>
                    <div class="kpi-gradient-value">${row['cpl']:,.0f}</div>
                    <div class="kpi-sub">Cost per Lead</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed Analysis
            st.markdown("---")
            st.markdown("### 📈 Detailed Performance Analysis")
            
            col_det1, col_det2 = st.columns(2)
            
            with col_det1:
                st.markdown("#### 📋 Campaign Details")
                details = {
                    "Project Name": row["project_name"],
                    "Customer ID": int(row["user_id"]),
                    "Total Spend": format_money(row["total_spend"]),
                    "Active Days": int(row["days_active"]),
                    "Total Leads": f"{int(row['total_leads']):,}",
                    "Converted Leads": f"{int(row['converted_leads']):,}",
                    "Spend per Day": format_money(row["spend_per_day"]) if not pd.isna(row["spend_per_day"]) else "-",
                    "Leads per Day": f"{row['leads_per_day']:,.1f}" if not pd.isna(row["leads_per_day"]) else "-"
                }
                
                for key, value in details.items():
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #2a2f45;">
                        <div style="color: #94a3b8;">{key}</div>
                        <div style="color: #ffffff; font-weight: 600;">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_det2:
                st.markdown("#### 📊 Performance vs Peers")
                
                # Create comparison metrics
                metrics = [
                    ("Conversion Rate", row["conversion_rate"] * 100, conv_p50 * 100, "Higher is better"),
                    ("Cost per Lead", row["cpl"], cpl_p50, "Lower is better"),
                    ("Leads per Day", row["leads_per_day"] if not pd.isna(row["leads_per_day"]) else 0, 
                     filtered["leads_per_day"].median(), "Higher is better"),
                    ("Spend per Day", row["spend_per_day"] if not pd.isna(row["spend_per_day"]) else 0,
                     filtered["spend_per_day"].median(), "Depends on ROI")
                ]
                
                for metric_name, actual, median, note in metrics:
                    if pd.isna(actual):
                        continue
                        
                    diff_pct = ((actual - median) / median * 100) if median != 0 else 0
                    color = "#10b981" if diff_pct > 0 and "better" in note.lower() else "#ef4444"
                    icon = "📈" if diff_pct > 0 else "📉"
                    
                    st.markdown(f"""
                    <div style="background: #1a1f35; padding: 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #2a2f45;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="color: #94a3b8; font-weight: 600;">{metric_name}</div>
                            <div style="color: {color}; font-weight: 700;">{icon} {diff_pct:+.1f}%</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 8px;">
                            <div style="color: #ffffff; font-weight: 700;">
                                {actual:,.1f} {'%' if '%' in metric_name else '$' if 'Cost' in metric_name else ''}
                            </div>
                            <div style="color: #64748b; font-size: 0.9rem;">
                                vs {median:,.1f} median
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Recommendations
            st.markdown("---")
            st.markdown("### 🎯 Strategic Recommendations")
            
            if row["health_bucket"] == "HERO":
                st.markdown(f"""
                <div class="action-card action-scale">
                    <div style="font-size: 2rem; margin-bottom: 10px;">🚀</div>
                    <div class="insight-title">Scale Up Campaign</div>
                    <div class="insight-text">
                    **This campaign is performing exceptionally well!**
                    
                    - Conversion rate is in the **top 25%** of all campaigns
                    - Cost per lead is in the **bottom 25%** of all campaigns
                    - You're getting great ROI on every dollar spent
                    
                    **Recommended Actions:**
                    1. **Increase budget by 30-50%** immediately
                    2. **Expand audience targeting** to similar demographics
                    3. **Replicate successful creative strategy** to other campaigns
                    4. **Test higher bid strategies** while maintaining efficiency
                    
                    **Expected Impact:** 20-40% increase in conversions with maintained ROI
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            elif row["health_bucket"] == "GOOD":
                st.markdown(f"""
                <div class="action-card action-keep">
                    <div style="font-size: 2rem; margin-bottom: 10px;">📈</div>
                    <div class="insight-title">Keep Running Campaign</div>
                    <div class="insight-text">
                    **This campaign is performing well - maintain current strategy.**
                    
                    - Conversion rate is **above average**
                    - Cost per lead is **acceptable**
                    - Campaign is **profitable** and generating quality leads
                    
                    **Recommended Actions:**
                    1. **Maintain current budget** allocation
                    2. **Continue monitoring** performance weekly
                    3. **A/B test small variations** in creative
                    4. **Look for opportunities** to improve CPL by 10-15%
                    
                    **Expected Impact:** Stable growth with minor optimizations
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            elif row["health_bucket"] == "MIXED":
                st.markdown(f"""
                <div class="action-card action-optimize">
                    <div style="font-size: 2rem; margin-bottom: 10px;">🔧</div>
                    <div class="insight-title">Optimize Campaign</div>
                    <div class="insight-text">
                    **This campaign shows potential but needs optimization.**
                    
                    - **Generating conversions** (which is positive!)
                    - But **cost per lead is higher than ideal**
                    - With optimization, this could become a HERO campaign
                    
                    **Recommended Actions:**
                    1. **Review audience targeting** - are you reaching the right people?
                    2. **Test new ad creatives** - what messaging resonates best?
                    3. **Optimize bidding strategy** - consider cost cap or bid caps
                    4. **Improve landing page experience** - reduce bounce rates
                    5. **Pause low-performing ad sets** and focus on winners
                    
                    **Expected Impact:** 15-30% reduction in CPL with maintained conversions
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            elif row["health_bucket"] == "BAD":
                st.markdown(f"""
                <div class="action-card action-stop">
                    <div style="font-size: 2rem; margin-bottom: 10px;">⏹️</div>
                    <div class="insight-title">Stop / Reallocate Campaign</div>
                    <div class="insight-text">
                    **This campaign is underperforming and likely wasting budget.**
                    
                    - **Zero conversions** despite significant spend
                    - **Very high cost per lead** (worst quartile)
                    - **Enough data** to make a confident decision
                    
                    **Recommended Actions:**
                    1. **Stop campaign immediately** to prevent further budget waste
                    2. **Reallocate budget** to HERO or GOOD performing campaigns
                    3. **Analyze what went wrong** - targeting, creative, or offer?
                    4. **Consider testing** completely new strategy if restarting
                    
                    **Expected Impact:** Immediate savings of ${row['spend_per_day']:,.0f} per day
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            else:  # NEEDS_MORE_DATA
                st.markdown(f"""
                <div class="action-card action-monitor">
                    <div style="font-size: 2rem; margin-bottom: 10px;">👀</div>
                    <div class="insight-title">Monitor Campaign</div>
                    <div class="insight-text">
                    **This campaign needs more data before making decisions.**
                    
                    - Campaign is **too new** or has **insufficient data**
                    - Not enough leads or spend to make reliable conclusions
                    - Early indicators are inconclusive
                    
                    **Recommended Actions:**
                    1. **Continue running** with current settings
                    2. **Monitor daily performance** for trends
                    3. **Wait until you have at least 20 leads** before re-evaluating
                    4. **Set clear KPI targets** for next evaluation
                    
                    **Expected Impact:** Clearer picture in {max(0, 20 - int(row['total_leads']))} more leads
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Quick navigation to other similar campaigns
            st.markdown("---")
            st.markdown("### 🔄 Similar Campaigns")
            
            # Find campaigns with same project name or similar performance
            similar_campaigns = filtered[
                (filtered["project_name"] == row["project_name"]) & 
                (filtered["campaign_id"] != selected_campaign_id)
            ].head(3)
            
            if not similar_campaigns.empty:
                st.markdown(f"Other campaigns in **{row['project_name']}**:")
                for _, sim_row in similar_campaigns.iterrows():
                    sim_health_color = get_health_color(sim_row["health_bucket"])
                    st.markdown(f"""
                    <div style="background: #1a1f35; padding: 15px; border-radius: 12px; margin-bottom: 10px; border-left: 4px solid {sim_health_color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-weight: 700; color: #ffffff;">Campaign {sim_row['campaign_id']}</div>
                            <div style="color: {sim_health_color}; font-weight: 600;">{sim_row['health_bucket']}</div>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 8px;">
                            Conversion: {sim_row['conversion_rate']*100:.1f}% • CPL: ${sim_row['cpl']:,.0f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
