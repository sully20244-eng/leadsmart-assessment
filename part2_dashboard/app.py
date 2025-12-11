import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Get absolute directory of this script (so Streamlit can find CSVs)
FILE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================
# 1) ENHANCED Page config + CSS
# =========================
st.set_page_config(
    page_title="LeadSmart Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fixed CSS - removed the problematic webkit prefix lines
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

/* Filter Badges */
.filter-badge {
    display: inline-block;
    padding: 4px 12px;
    background: rgba(99, 102, 241, 0.1);
    color: #c7d2fe;
    border-radius: 12px;
    font-size: 0.85rem;
    margin: 0 4px 8px 0;
}
</style>
"""

st.markdown(ENHANCED_CSS, unsafe_allow_html=True)

# =========================
# 2) Enhanced Helper Functions
# =========================
def format_large_number(x, is_currency=False):
    """Format large numbers with K, M suffixes"""
    if pd.isna(x) or x == 0:
        return "0" if not is_currency else "$0"
    x = float(x)
    
    if is_currency:
        if abs(x) >= 1_000_000:
            return f"${x/1_000_000:.1f}M"
        if abs(x) >= 10_000:
            return f"${x/1_000:.0f}K"
        if abs(x) >= 1_000:
            return f"${x/1_000:.1f}K"
        return f"${x:,.0f}"
    else:
        if abs(x) >= 1_000_000:
            return f"{x/1_000_000:.1f}M"
        if abs(x) >= 10_000:
            return f"{x/1_000:.0f}K"
        if abs(x) >= 1_000:
            return f"{x/1_000:.1f}K"
        return f"{x:,.0f}"

def create_gradient_color_scale(color_scheme="viridis"):
    """Create gradient colors for charts"""
    if color_scheme == "business":
        return ["#06b6d4", "#3b82f6", "#6366f1", "#8b5cf6", "#a855f7"]
    elif color_scheme == "success":
        return ["#10b981", "#22c55e", "#4ade80", "#86efac"]
    elif color_scheme == "warning":
        return ["#f59e0b", "#fbbf24", "#fcd34d", "#fde68a"]
    elif color_scheme == "danger":
        return ["#ef4444", "#f87171", "#fca5a5", "#fecaca"]
    else:
        return px.colors.sequential.Viridis

# =========================
# 3) Load & prepare data
# =========================
@st.cache_data
def load_data():
    """Load and prepare all data files"""
    try:
        campaign_leads = pd.read_csv(os.path.join(FILE_DIR, "campaign_leads.csv"))
        campaigns = pd.read_csv(os.path.join(FILE_DIR, "campaigns.csv"))
        insights = pd.read_csv(os.path.join(FILE_DIR, "insights.csv"))
        lead_status_changes = pd.read_csv(os.path.join(FILE_DIR, "lead_status_changes.csv"))
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        # Create dummy data for demonstration
        campaign_leads = pd.DataFrame({
            'id': range(100),
            'campaign_id': np.random.choice(range(1, 11), 100),
            'added_date': pd.date_range('2024-01-01', periods=100),
            'lead_status': np.random.choice(['NEW', 'CONTACTED', 'QUALIFIED', 'MEETING_DONE', 'DONE_DEAL'], 100)
        })
        campaigns = pd.DataFrame({
            'id': range(1, 11),
            'user_id': np.random.choice([1, 2, 3], 10),
            'project_name': [f'Project_{i}' for i in range(1, 11)]
        })
        insights = pd.DataFrame({
            'campaign_id': np.random.choice(range(1, 11), 50),
            'spend': np.random.uniform(100, 5000, 50),
            'created_at': pd.date_range('2024-01-01', periods=50)
        })
        lead_status_changes = pd.DataFrame(columns=['created_at'])

    # Rename IDs for consistency
    campaign_leads = campaign_leads.rename(columns={"id": "lead_id"})
    campaigns = campaigns.rename(columns={"id": "campaign_id"})

    # Parse dates
    date_columns = {
        'campaign_leads': ['added_date'],
        'insights': ['created_at'],
        'lead_status_changes': ['created_at']
    }
    
    for df_name, cols in date_columns.items():
        df = locals().get(df_name)
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

    # Derive date columns
    campaign_leads["date"] = campaign_leads["added_date"].dt.date
    insights["date"] = insights["created_at"].dt.date

    # Define conversion statuses
    conversion_statuses = [
        "DONE_DEAL",
        "ALREADY_BOUGHT",
        "RESALE_REQUEST",
        "MEETING_DONE",
        "HIGH_INTEREST",
        "QUALIFIED",
    ]
    campaign_leads["is_converted"] = campaign_leads["lead_status"].isin(conversion_statuses)

    # Join with campaigns
    leads_with_campaign = campaign_leads.merge(
        campaigns[["campaign_id", "user_id", "project_name"]],
        on="campaign_id",
        how="left"
    )

    insights_with_campaign = insights.merge(
        campaigns[["campaign_id", "user_id", "project_name"]],
        on="campaign_id",
        how="left"
    )

    return leads_with_campaign, insights_with_campaign, lead_status_changes

# Load the data
leads_with_campaign, insights_with_campaign, lead_status_changes = load_data()

# =========================
# 4) Enhanced Sidebar with Filter Badges
# =========================
st.sidebar.markdown("### 🔍 Filters")
st.sidebar.markdown('<div class="filter-badge">📅 Date Range</div>', unsafe_allow_html=True)

# Get date ranges
if not leads_with_campaign.empty and not insights_with_campaign.empty:
    min_date = min(
        leads_with_campaign["added_date"].min(),
        insights_with_campaign["created_at"].min()
    ).date()
    max_date = max(
        leads_with_campaign["added_date"].max(),
        insights_with_campaign["created_at"].max()
    ).date()
else:
    min_date = datetime(2024, 1, 1).date()
    max_date = datetime(2024, 12, 31).date()

date_range = st.sidebar.date_input(
    "",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# User filter
st.sidebar.markdown('<div class="filter-badge">👥 Customer</div>', unsafe_allow_html=True)
if not leads_with_campaign.empty:
    all_users = sorted(leads_with_campaign["user_id"].dropna().unique().tolist())
    user_display = ["All Customers"] + [f"Customer {int(u)}" for u in all_users]
else:
    all_users = []
    user_display = ["All Customers"]

selected_user_str = st.sidebar.selectbox(
    "",
    options=user_display,
    index=0
)

if selected_user_str != "All Customers":
    selected_user = int(selected_user_str.replace("Customer ", ""))
    if not leads_with_campaign.empty:
        available_projects = sorted(
            leads_with_campaign.query("user_id == @selected_user")["project_name"].dropna().unique().tolist()
        )
    else:
        available_projects = []
else:
    selected_user = None
    if not leads_with_campaign.empty:
        available_projects = sorted(
            leads_with_campaign["project_name"].dropna().unique().tolist()
        )
    else:
        available_projects = []

# Project filter
st.sidebar.markdown('<div class="filter-badge">🏢 Project</div>', unsafe_allow_html=True)
project_display = ["All Projects"] + available_projects
selected_project = st.sidebar.selectbox(
    "",
    options=project_display,
    index=0
)

# Sidebar quick stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")

if not leads_with_campaign.empty:
    total_campaigns = leads_with_campaign["campaign_id"].nunique()
    total_projects = leads_with_campaign["project_name"].nunique()
else:
    total_campaigns = 0
    total_projects = 0

st.sidebar.metric("Total Campaigns", total_campaigns)
st.sidebar.metric("Total Projects", total_projects)

# =========================
# 5) Apply filters to data
# =========================
def apply_filters(leads_df, insights_df):
    """Apply date and user/project filters to dataframes"""
    # Filter by date
    filtered_leads = leads_df[
        (leads_df["added_date"].dt.date >= start_date) &
        (leads_df["added_date"].dt.date <= end_date)
    ].copy()
    
    filtered_insights = insights_df[
        (insights_df["created_at"].dt.date >= start_date) &
        (insights_df["created_at"].dt.date <= end_date)
    ].copy()
    
    # Filter by user
    if selected_user is not None:
        filtered_leads = filtered_leads[filtered_leads["user_id"] == selected_user]
        filtered_insights = filtered_insights[filtered_insights["user_id"] == selected_user]
    
    # Filter by project
    if selected_project != "All Projects":
        filtered_leads = filtered_leads[filtered_leads["project_name"] == selected_project]
        filtered_insights = filtered_insights[filtered_insights["project_name"] == selected_project]
    
    return filtered_leads, filtered_insights

filtered_leads, filtered_insights = apply_filters(leads_with_campaign, insights_with_campaign)

# =========================
# 6) Aggregations helper function
# =========================
def build_aggregates(leads_df, insights_df):
    """Build aggregated metrics for campaigns and projects"""
    if leads_df.empty and insights_df.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    # Campaign-level metrics
    if not leads_df.empty:
        camp = (
            leads_df.groupby(["campaign_id", "project_name", "user_id"], as_index=False)
            .agg(
                total_leads=("lead_id", "count"),
                converted_leads=("is_converted", "sum")
            )
        )
    else:
        camp = pd.DataFrame(columns=["campaign_id", "project_name", "user_id", "total_leads", "converted_leads"])
    
    # Spend per campaign
    if not insights_df.empty:
        spend_by_campaign = (
            insights_df.groupby("campaign_id", as_index=False)
            .agg(spend=("spend", "sum"))
        )
    else:
        spend_by_campaign = pd.DataFrame(columns=["campaign_id", "spend"])
    
    # Merge spend data
    if not camp.empty:
        camp = camp.merge(spend_by_campaign, on="campaign_id", how="left")
        camp["spend"] = camp["spend"].fillna(0)
        
        # Calculate metrics
        camp["conversion_rate"] = np.where(
            camp["total_leads"] > 0,
            camp["converted_leads"] / camp["total_leads"],
            0.0
        )
        camp["CPL"] = np.where(
            camp["total_leads"] > 0,
            camp["spend"] / camp["total_leads"],
            np.nan
        )
        camp["cost_per_conversion"] = np.where(
            camp["converted_leads"] > 0,
            camp["spend"] / camp["converted_leads"],
            np.nan
        )
    else:
        camp["spend"] = 0
        camp["conversion_rate"] = 0
        camp["CPL"] = np.nan
        camp["cost_per_conversion"] = np.nan
    
    # Project-level metrics
    if not camp.empty:
        proj = (
            camp.groupby(["project_name", "user_id"], as_index=False)
            .agg(
                total_leads=("total_leads", "sum"),
                converted_leads=("converted_leads", "sum"),
                spend=("spend", "sum")
            )
        )
        
        proj["conversion_rate"] = np.where(
            proj["total_leads"] > 0,
            proj["converted_leads"] / proj["total_leads"],
            0.0
        )
        proj["CPL"] = np.where(
            proj["total_leads"] > 0,
            proj["spend"] / proj["total_leads"],
            np.nan
        )
    else:
        proj = pd.DataFrame(columns=["project_name", "user_id", "total_leads", "converted_leads", "spend", "conversion_rate", "CPL"])
    
    # Daily metrics
    if not insights_df.empty:
        daily_spend = (
            insights_df.groupby("date", as_index=False)
            .agg(daily_spend=("spend", "sum"))
            .sort_values("date")
        )
    else:
        daily_spend = pd.DataFrame(columns=["date", "daily_spend"])
    
    if not leads_df.empty:
        daily_leads = (
            leads_df.groupby("date", as_index=False)
            .agg(daily_leads=("lead_id", "count"))
            .sort_values("date")
        )
    else:
        daily_leads = pd.DataFrame(columns=["date", "daily_leads"])
    
    # Lead status distribution
    if not leads_df.empty:
        status_dist = (
            leads_df.groupby("lead_status", as_index=False)
            .agg(count=("lead_id", "count"))
            .sort_values("count", ascending=False)
        )
    else:
        status_dist = pd.DataFrame(columns=["lead_status", "count"])
    
    return camp, proj, daily_spend, daily_leads, status_dist

# Build aggregates
campaign_perf, project_perf, daily_spend, daily_leads, status_dist = build_aggregates(filtered_leads, filtered_insights)

# Create daily time series
if not daily_spend.empty or not daily_leads.empty:
    daily_ts = pd.merge(daily_spend, daily_leads, on="date", how="outer")
    daily_ts = daily_ts.sort_values("date")
    daily_ts["daily_spend"] = daily_ts["daily_spend"].fillna(0)
    daily_ts["daily_leads"] = daily_ts["daily_leads"].fillna(0)
    daily_ts["date"] = pd.to_datetime(daily_ts["date"])
else:
    daily_ts = pd.DataFrame(columns=["date", "daily_spend", "daily_leads"])

# =========================
# 7) Calculate Global KPIs
# =========================
total_spend = filtered_insights["spend"].sum() if not filtered_insights.empty else 0
total_leads = filtered_leads["lead_id"].nunique() if not filtered_leads.empty else 0
total_converted = filtered_leads["is_converted"].sum() if not filtered_leads.empty else 0
global_conv_rate = (total_converted / total_leads) if total_leads > 0 else 0
global_cpl = (total_spend / total_leads) if total_leads > 0 else np.nan

# Example trends (in a real app, these would be calculated from historical data)
spend_trend = 12.5 if total_spend > 0 else 0
leads_trend = 8.3 if total_leads > 0 else 0
conv_trend = 4.2 if global_conv_rate > 0 else 0

# =========================
# 8) ENHANCED Tabs with Creative Visuals
# =========================
tab_overview, tab_campaigns, tab_projects, tab_funnel, tab_insights = st.tabs(
    ["📊 Overview", "🎯 Campaigns", "🏢 Projects", "📈 Funnel", "💡 Insights"]
)

# ----------------------------------------
# TAB 1 – ENHANCED OVERVIEW
# ----------------------------------------
with tab_overview:
    # Header with current filters
    filter_info = f"📅 Period: {start_date} to {end_date}"
    if selected_user:
        filter_info += f" | 👥 Customer: {selected_user}"
    if selected_project != "All Projects":
        filter_info += f" | 🏢 Project: {selected_project}"
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1a1f35 0%, #0f1324 100%); padding: 20px; border-radius: 16px; margin-bottom: 24px; border: 1px solid #2a2f45;">
        <h3 style="margin: 0; color: #e2e8f0; font-size: 1.2rem; font-weight: 600;">
            {filter_info}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced KPI Cards
    st.markdown('<div class="section-title-gradient">Performance Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        trend_icon = "↗️" if spend_trend > 0 else "↘️" if spend_trend < 0 else "➡️"
        trend_class = "trend-up" if spend_trend > 0 else "trend-down" if spend_trend < 0 else ""
        trend_text = f"{abs(spend_trend):.1f}%" if spend_trend != 0 else ""
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Total Spend</div>
            <div class="kpi-gradient-value">{format_large_number(total_spend, True)}</div>
            <div class="kpi-sub">All campaigns in selected period</div>
            {f'<div class="kpi-trend {trend_class}">{trend_icon} {trend_text}</div>' if trend_text else ''}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        trend_icon = "↗️" if leads_trend > 0 else "↘️" if leads_trend < 0 else "➡️"
        trend_class = "trend-up" if leads_trend > 0 else "trend-down" if leads_trend < 0 else ""
        trend_text = f"{abs(leads_trend):.1f}%" if leads_trend != 0 else ""
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">👥 Total Leads</div>
            <div class="kpi-gradient-value">{format_large_number(total_leads)}</div>
            <div class="kpi-sub">Leads captured from all projects</div>
            {f'<div class="kpi-trend {trend_class}">{trend_icon} {trend_text}</div>' if trend_text else ''}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        conv_rate_pct = global_conv_rate * 100
        trend_icon = "↗️" if conv_trend > 0 else "↘️" if conv_trend < 0 else "➡️"
        trend_class = "trend-up" if conv_trend > 0 else "trend-down" if conv_trend < 0 else ""
        trend_text = f"{abs(conv_trend):.1f}%" if conv_trend != 0 else ""
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🎯 Conversion Rate</div>
            <div class="kpi-gradient-value">{conv_rate_pct:.1f}%</div>
            <div class="kpi-sub">Based on final sales statuses</div>
            {f'<div class="kpi-trend {trend_class}">{trend_icon} {trend_text}</div>' if trend_text else ''}
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        cpl_str = "—" if np.isnan(global_cpl) else f"${global_cpl:,.2f}"
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📊 Cost Per Lead</div>
            <div class="kpi-gradient-value">{cpl_str}</div>
            <div class="kpi-sub">Average cost per acquired lead</div>
            <div class="metric-badge">Industry Avg: $45.20</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Time Series Charts
    st.markdown('<div class="section-title">📈 Performance Trends</div>', unsafe_allow_html=True)
    
    if not daily_ts.empty:
        # Combined chart
        st.markdown("#### Daily Spend vs Leads")
        fig_combined = go.Figure()
        
        # Add spend line
        fig_combined.add_trace(go.Scatter(
            x=daily_ts["date"],
            y=daily_ts["daily_spend"],
            name="Spend",
            mode='lines',
            line=dict(color='#4f46e5', width=3),
            fill='tozeroy',
            fillcolor='rgba(79, 70, 229, 0.2)'
        ))
        
        # Add leads bar on secondary axis
        fig_combined.add_trace(go.Bar(
            x=daily_ts["date"],
            y=daily_ts["daily_leads"],
            name="Leads",
            marker_color='#06b6d4',
            opacity=0.7,
            yaxis='y2'
        ))
        
        fig_combined.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(
                title="Date",
                gridcolor='#2a2f45',
                showgrid=True
            ),
            yaxis=dict(
                title="Spend ($)",
                gridcolor='#2a2f45',
                showgrid=True
            ),
            yaxis2=dict(
                title="Leads",
                overlaying='y',
                side='right',
                gridcolor='#2a2f45',
                showgrid=False
            ),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig_combined, use_container_width=True)
        
        # Mini metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_daily_spend = daily_ts["daily_spend"].mean()
            st.metric("📈 Avg Daily Spend", f"${avg_daily_spend:,.0f}")
        
        with col2:
            avg_daily_leads = daily_ts["daily_leads"].mean()
            st.metric("👥 Avg Daily Leads", f"{avg_daily_leads:,.0f}")
        
        with col3:
            if not daily_ts.empty:
                peak_day = daily_ts.loc[daily_ts["daily_leads"].idxmax()]
                st.metric("🚀 Peak Day Leads", f"{peak_day['daily_leads']:,.0f}", 
                         f"on {peak_day['date'].strftime('%b %d')}")
            else:
                st.metric("🚀 Peak Day Leads", "0")
    else:
        st.info("No time series data available for the selected period.")

# ----------------------------------------
# TAB 2 – ENHANCED CAMPAIGNS
# ----------------------------------------
with tab_campaigns:
    st.markdown('<div class="section-title-gradient">🎯 Campaign Performance Analysis</div>', unsafe_allow_html=True)
    
    if campaign_perf.empty:
        st.warning("No campaign data available for the selected filters.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 Top 10 Campaigns by Conversion Rate")
            conv_camp = campaign_perf[campaign_perf["converted_leads"] > 0].copy()
            conv_camp["conv_pct"] = (conv_camp["conversion_rate"] * 100).round(1)
            conv_camp = conv_camp.sort_values("conversion_rate", ascending=False).head(10)
            
            if not conv_camp.empty:
                fig_top_conv = px.bar(
                    conv_camp,
                    x=conv_camp["campaign_id"].astype(str),
                    y="conv_pct",
                    text="conv_pct",
                    labels={"x": "Campaign ID", "conv_pct": "Conversion Rate (%)"},
                    color="conv_pct",
                    color_continuous_scale=create_gradient_color_scale("success")
                )
                fig_top_conv.update_traces(
                    texttemplate='%{text}%',
                    textposition='outside',
                    marker_line_width=0
                )
                fig_top_conv.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8'),
                    xaxis=dict(
                        gridcolor='#2a2f45',
                        title="Campaign ID"
                    ),
                    yaxis=dict(
                        gridcolor='#2a2f45',
                        title="Conversion Rate (%)"
                    ),
                    coloraxis_showscale=False,
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig_top_conv, use_container_width=True)
            else:
                st.info("No converting campaigns in this period.")
        
        with col2:
            st.markdown("#### 💰 Top 10 Campaigns by Highest CPL")
            cpl_camp = campaign_perf[campaign_perf["CPL"].notna()].copy()
            cpl_camp = cpl_camp.sort_values("CPL", ascending=False).head(10)
            
            if not cpl_camp.empty:
                fig_top_cpl = px.bar(
                    cpl_camp,
                    x=cpl_camp["campaign_id"].astype(str),
                    y="CPL",
                    text=cpl_camp["CPL"].round(0),
                    labels={"x": "Campaign ID", "CPL": "Cost per Lead ($)"},
                    color="CPL",
                    color_continuous_scale=create_gradient_color_scale("warning")
                )
                fig_top_cpl.update_traces(
                    texttemplate='$%{text:,.0f}',
                    textposition='outside',
                    marker_line_width=0
                )
                fig_top_cpl.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8'),
                    xaxis=dict(
                        gridcolor='#2a2f45',
                        title="Campaign ID"
                    ),
                    yaxis=dict(
                        gridcolor='#2a2f45',
                        title="Cost per Lead ($)"
                    ),
                    coloraxis_showscale=False,
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig_top_cpl, use_container_width=True)
            else:
                st.info("No CPL data available for campaigns.")

# ----------------------------------------
# TAB 3 – ENHANCED PROJECTS
# ----------------------------------------
with tab_projects:
    st.markdown('<div class="section-title-gradient">🏢 Project Performance Dashboard</div>', unsafe_allow_html=True)
    
    if project_perf.empty:
        st.warning("No project data available for the selected filters.")
    else:
        # Top project highlights
        col1, col2 = st.columns(2)
        
        with col1:
            if not project_perf.empty and project_perf["conversion_rate"].max() > 0:
                best_proj = project_perf.loc[project_perf["conversion_rate"].idxmax()]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1f35 0%, #0f172a 100%); padding: 20px; border-radius: 16px; border: 1px solid #2a2f45; margin-bottom: 20px;">
                    <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">🏆 Best Performing Project</div>
                    <div style="color: #ffffff; font-size: 1.2rem; font-weight: 700; margin-bottom: 4px;">{best_proj['project_name']}</div>
                    <div style="color: #22c55e; font-size: 0.9rem;">Conversion Rate: {(best_proj['conversion_rate']*100):.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if not project_perf.empty and project_perf["total_leads"].max() > 0:
                most_leads_project = project_perf.loc[project_perf["total_leads"].idxmax()]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1f35 0%, #0f172a 100%); padding: 20px; border-radius: 16px; border: 1px solid #2a2f45; margin-bottom: 20px;">
                    <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">📊 Highest Volume Project</div>
                    <div style="color: #ffffff; font-size: 1.2rem; font-weight: 700; margin-bottom: 4px;">{most_leads_project['project_name']}</div>
                    <div style="color: #06b6d4; font-size: 0.9rem;">Total Leads: {most_leads_project['total_leads']:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Efficiency Matrix
        st.markdown("#### ⚡ Efficiency Matrix: CPL vs Conversion Rate")
        proj_map = project_perf[
            project_perf["CPL"].notna() & 
            (project_perf["total_leads"] > 0) &
            (project_perf["conversion_rate"] > 0)
        ].copy()
        
        if not proj_map.empty:
            proj_map["conv_pct"] = (proj_map["conversion_rate"] * 100).round(1)
            
            # Calculate medians for quadrant lines
            median_cpl = proj_map["CPL"].median()
            median_conv = proj_map["conv_pct"].median()
            
            fig_eff = px.scatter(
                proj_map,
                x="CPL",
                y="conv_pct",
                size="total_leads",
                color="project_name",
                hover_data=["project_name", "total_leads", "converted_leads", "spend"],
                labels={
                    "CPL": "Cost per Lead ($)",
                    "conv_pct": "Conversion Rate (%)"
                },
                size_max=40
            )
            
            # Add quadrant lines
            fig_eff.add_hline(
                y=median_conv,
                line_dash="dash",
                line_color="white",
                opacity=0.3,
                annotation_text=f"Median Conv: {median_conv:.1f}%"
            )
            fig_eff.add_vline(
                x=median_cpl,
                line_dash="dash",
                line_color="white",
                opacity=0.3,
                annotation_text=f"Median CPL: ${median_cpl:.0f}"
            )
            
            fig_eff.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                xaxis=dict(
                    gridcolor='#2a2f45',
                    title="Cost per Lead (CPL)"
                ),
                yaxis=dict(
                    gridcolor='#2a2f45',
                    title="Conversion Rate (%)"
                ),
                showlegend=True,
                legend=dict(
                    title="Projects",
                    bgcolor='rgba(26, 31, 53, 0.8)',
                    bordercolor="#2a2f45",
                    borderwidth=1
                ),
                margin=dict(l=40, r=40, t=40, b=40)
            )
            
            st.plotly_chart(fig_eff, use_container_width=True)
            
            # Quadrant explanation
            st.markdown("""
            **📊 Quadrant Analysis:**
            
            - **🔵 Top-Left (High Conv, Low CPL):** Best performers - Scale these projects
            - **🟡 Top-Right (High Conv, High CPL):** Effective but expensive - Optimize costs
            - **🟠 Bottom-Left (Low Conv, Low CPL):** Inexpensive but ineffective - Test improvements
            - **🔴 Bottom-Right (Low Conv, High CPL):** Worst performers - Consider pausing
            """)
        else:
            st.info("Not enough data to create efficiency matrix.")

# ----------------------------------------
# TAB 4 – ENHANCED FUNNEL
# ----------------------------------------
with tab_funnel:
    st.markdown('<div class="section-title-gradient">📊 Lead Conversion Funnel</div>', unsafe_allow_html=True)
    
    if status_dist.empty:
        st.info("No lead status data available for the selected period.")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Funnel visualization - FIXED: Changed 'percent total' to 'percent'
            st.markdown("#### Lead Status Distribution")
            colors = px.colors.qualitative.Set3[:len(status_dist)]
            
            fig_funnel = go.Figure(go.Funnelarea(
                text=status_dist["lead_status"],
                values=status_dist["count"],
                marker=dict(colors=colors),
                textinfo="value+text",
                hoverinfo="value+percent",  # Fixed: 'percent' instead of 'percent total'
                opacity=0.9
            ))
            
            fig_funnel.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                margin=dict(l=40, r=40, t=40, b=40),
                title="Lead Status Funnel"
            )
            
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        with col2:
            # Funnel metrics
            total_leads_funnel = status_dist["count"].sum()
            
            # Calculate conversion metrics
            conversion_statuses = ["DONE_DEAL", "ALREADY_BOUGHT", "RESALE_REQUEST", 
                                 "MEETING_DONE", "HIGH_INTEREST", "QUALIFIED"]
            converted_df = status_dist[status_dist["lead_status"].isin(conversion_statuses)]
            converted_count = converted_df["count"].sum() if not converted_df.empty else 0
            
            conversion_rate_funnel = (converted_count / total_leads_funnel * 100) if total_leads_funnel > 0 else 0
            
            st.markdown("#### 📈 Funnel Metrics")
            
            # Metric cards
            st.markdown(f"""
            <div style="background: #1a1f35; border-radius: 12px; padding: 20px; margin-bottom: 16px; border: 1px solid #2a2f45;">
                <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">📊 Total Leads in Funnel</div>
                <div style="color: #ffffff; font-size: 1.8rem; font-weight: 700;">{total_leads_funnel:,}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: #1a1f35; border-radius: 12px; padding: 20px; margin-bottom: 16px; border: 1px solid #2a2f45;">
                <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">🎯 Converted Leads</div>
                <div style="color: #22c55e; font-size: 1.8rem; font-weight: 700;">{converted_count:,}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: #1a1f35; border-radius: 12px; padding: 20px; margin-bottom: 16px; border: 1px solid #2a2f45;">
                <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">📈 Overall Conversion Rate</div>
                <div style="color: #06b6d4; font-size: 1.8rem; font-weight: 700;">{conversion_rate_funnel:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick insights
            if not status_dist.empty:
                top_status = status_dist.iloc[0]
                percentage = (top_status['count'] / total_leads_funnel * 100) if total_leads_funnel > 0 else 0
                st.markdown(f"""
                <div style="background: #1a1f35; border-radius: 12px; padding: 16px; margin-top: 20px; border: 1px solid #2a2f45;">
                    <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">📋 Most Common Status</div>
                    <div style="color: #ffffff; font-size: 1.1rem; font-weight: 600;">{top_status['lead_status']}</div>
                    <div style="color: #06b6d4; font-size: 0.9rem;">{top_status['count']:,} leads ({percentage:.1f}%)</div>
                </div>
                """, unsafe_allow_html=True)

# ----------------------------------------
# TAB 5 – BUSINESS INSIGHTS
# ----------------------------------------
with tab_insights:
    st.markdown('<div class="section-title-gradient">💡 AI-Powered Business Insights</div>', unsafe_allow_html=True)
    
    if not campaign_perf.empty and not project_perf.empty and not daily_ts.empty:
        # Generate insights based on data
        insights = []
        
        # Insight 1: Best performing project
        if not project_perf.empty and project_perf["conversion_rate"].max() > 0:
            best_proj = project_perf.loc[project_perf["conversion_rate"].idxmax()]
            insights.append({
                "icon": "🏆",
                "title": "Top Performing Project",
                "content": f"**{best_proj['project_name']}** leads with a **{(best_proj['conversion_rate']*100):.1f}% conversion rate**. Consider replicating its strategy across other projects."
            })
        
        # Insight 2: Cost efficiency
        if not project_perf.empty and project_perf["CPL"].notna().any():
            median_cpl = project_perf["CPL"].median()
            efficient_projs = project_perf[project_perf["CPL"] < median_cpl * 0.7]  # 30% below median
            if len(efficient_projs) > 0:
                insights.append({
                    "icon": "💰",
                    "title": "Cost Efficient Projects",
                    "content": f"**{len(efficient_projs)} projects** are operating at CPL 30% below the median (${median_cpl:.0f}). These represent your most efficient lead sources."
                })
        
        # Insight 3: High volume opportunity
        if not campaign_perf.empty:
            top_5_campaigns = campaign_perf.nlargest(5, "converted_leads")
            if len(top_5_campaigns) > 0:
                total_conversions = top_5_campaigns["converted_leads"].sum()
                percentage = (total_conversions / total_converted * 100) if total_converted > 0 else 0
                insights.append({
                    "icon": "📈",
                    "title": "High Performers Concentration",
                    "content": f"Top 5 campaigns generate **{percentage:.0f}% of all conversions**. Focus resources on scaling these successful campaigns."
                })
        
        # Insight 4: Time-based insight
        if not daily_ts.empty:
            avg_leads = daily_ts["daily_leads"].mean()
            high_period = daily_ts[daily_ts["daily_leads"] > avg_leads * 1.5]  # 50% above average
            if len(high_period) > 0:
                insights.append({
                    "icon": "📅",
                    "title": "Peak Performance Periods",
                    "content": f"**{len(high_period)} days** showed lead volume 50% above average. Analyze what made these days successful."
                })
        
        # Insight 5: Warning for high CPL
        if not project_perf.empty and project_perf["CPL"].notna().any():
            high_cpl_projs = project_perf[project_perf["CPL"] > project_perf["CPL"].median() * 1.5]
            if len(high_cpl_projs) > 0:
                insights.append({
                    "icon": "⚠️",
                    "title": "High Cost Projects Alert",
                    "content": f"**{len(high_cpl_projs)} projects** have CPL 50% above median. Review targeting and creative strategies for these projects."
                })
        
        # Display insights
        for i, insight in enumerate(insights[:4]):  # Show up to 4 insights
            st.markdown(f"""
            <div class="insight-box">
                <div style="display: flex; align-items: start; margin-bottom: 12px;">
                    <span style="font-size: 1.5rem; margin-right: 10px;">{insight['icon']}</span>
                    <div>
                        <div class="insight-title">{insight['title']}</div>
                        <div class="insight-text">{insight['content']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations section
        st.markdown("---")
        st.markdown("#### 🎯 Recommended Actions")
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("""
            **✅ Scale & Expand:**
            
            • Increase budget for top-converting campaigns
            • Replicate successful creative strategies
            • Expand targeting in high-performing regions
            • Test new audiences with similar profiles
            """)
        
        with rec_col2:
            st.markdown("""
            **🔧 Optimize & Improve:**
            
            • Review targeting for high-CPL projects
            • A/B test new ad creatives
            • Optimize landing page experience
            • Adjust bids based on performance
            """)
    
    else:
        st.info("Adjust your filters or add more data to generate insights.")

# =========================
# 9) Footer
# =========================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 20px;">
        📊 <strong>LeadSmart Performance Dashboard</strong> | 
        📅 Last Updated: {date} | 
        ⚡ Real-time Analytics
    </div>
    """.format(date=datetime.now().strftime("%Y-%m-%d %H:%M")),
    unsafe_allow_html=True
)
