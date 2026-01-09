import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="OceanHub OH7 Pipeline Analytics",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ocean theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0A1628 0%, #0F2847 50%, #1A3A5C 100%);
    }
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .insight-box {
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.15) 0%, rgba(34, 211, 238, 0.05) 100%);
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
    }
    .insight-box.danger {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
        border-color: rgba(239, 68, 68, 0.3);
    }
    .insight-box.warning {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(249, 115, 22, 0.05) 100%);
        border-color: rgba(249, 115, 22, 0.3);
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 16px;
    }
    div[data-testid="stMetric"] label {
        color: #64748B !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🌊 OH7 Pipeline Analytics Dashboard")
st.markdown("**Complete Application Funnel Analysis**")
st.caption("Data as of January 9, 2026")

st.divider()

# ============ SECTION 1: Overall Funnel ============
st.header("📊 Application Funnel Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Applicants", "357", help="Started applications")
    
with col2:
    st.metric("Completed", "82", "23%", help="Submitted applications")
    
with col3:
    st.metric("Incomplete", "275", "-77%", delta_color="inverse", help="Dropped off")
    
with col4:
    st.metric("Scouting Pipeline", "135", help="Tracked startups")
    
with col5:
    st.metric("From Dashboard", "19", help="7 completed + 12 incomplete")

st.divider()

# ============ SECTION 2: Incomplete Applications Crisis ============
st.header("🚨 Incomplete Applications Analysis (275)")

# Critical insight
st.markdown("""
<div class="insight-box danger">
    <strong style="color: #F87171;">🔴 Critical Finding:</strong> 
    <span style="color: #CBD5E1;"><strong>95 applicants (34.5%) stopped at exactly 45.9% progress</strong> — this is where the pitch video question appears.
    90.5% of incomplete applicants never uploaded a video. This single question is your biggest conversion killer.</span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Drop-off funnel
    funnel_data = pd.DataFrame({
        'Stage': ['0-20% (Started)', '21-35% (Registration)', '36-45% (Pre-Video)', 
                  '45.9% PITCH VIDEO 🔴', '46-70% (Working)', '71-99% (Almost!)', '100% (Just Submit!)'],
        'Count': [5, 49, 75, 95, 31, 17, 3],
        'Percentage': [1.8, 17.8, 27.3, 34.5, 11.3, 6.2, 1.1]
    })
    
    colors = ['#64748B', '#F97316', '#F59E0B', '#EF4444', '#0891B2', '#10B981', '#5EEAD4']
    
    fig_funnel = go.Figure(go.Bar(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        orientation='h',
        marker_color=colors,
        text=funnel_data['Count'],
        textposition='inside',
        textfont=dict(color='white', size=14)
    ))
    
    fig_funnel.update_layout(
        title="Drop-off Funnel by Progress Stage",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_title="Number of Applicants",
        yaxis=dict(categoryorder='array', categoryarray=funnel_data['Stage'].tolist()[::-1]),
        height=400
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

with col2:
    # Field completion rates
    field_data = pd.DataFrame({
        'Field': ['Company Name', 'Ocean Focus', 'Pitch Video', 'Pitch Deck', 'Tech Stage', 'Innovation Desc'],
        'Completion': [100, 67.3, 9.5, 9.5, 8.4, 5.1]
    })
    
    colors2 = ['#10B981', '#22D3EE', '#EF4444', '#EF4444', '#EF4444', '#EF4444']
    
    fig_fields = go.Figure(go.Bar(
        y=field_data['Field'],
        x=field_data['Completion'],
        orientation='h',
        marker_color=colors2,
        text=[f"{v}%" for v in field_data['Completion']],
        textposition='inside',
        textfont=dict(color='white', size=12)
    ))
    
    fig_fields.update_layout(
        title="Field Completion Rates (275 incomplete)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_title="Completion %",
        xaxis=dict(range=[0, 100]),
        yaxis=dict(categoryorder='array', categoryarray=field_data['Field'].tolist()[::-1]),
        height=400
    )
    st.plotly_chart(fig_fields, use_container_width=True)

st.divider()

# ============ SECTION 3: Re-engagement Candidates ============
st.header("🚀 High-Priority Re-engagement: Almost-Complete Applications")

reengage_data = pd.DataFrame({
    'Company': ['Peanut Pride Limited', 'ABU Abdulrahman Communication', 'IFBA', 
                'Aquapilote', 'Furies Enterprise ⭐', 'Obote Mixed Farm',
                'Constantnople Enterprise', 'HydroTech DZ Industrial', 'Mas Technologies Ltd',
                'Mtv', 'PENAF', 'The People & Planet Group', 'SKOJI FOODS and HERBS',
                'Rafiki Peps Limited', 'Saliskhan Global LTD', 'N.KV NITEZIMBERE LTD',
                'Memento Holdings', 'KCG Aquatec ⭐', 'Mutombo The Grace Service', 'Sunshine Acres'],
    'Progress': [100.0, 100.0, 100.0, 97.3, 97.3, 94.6, 94.6, 94.6, 94.6, 94.6,
                 91.9, 91.9, 89.2, 83.8, 75.7, 75.7, 75.7, 73.0, 73.0, 70.3],
    'Email': ['joshuaadomdaniel@gmail.com', 'abuabdulrahman5353@gmail.com', 'abubaidacoder@gmail.com',
              'komisenaa1@gmail.com', 'veramichael2000@gmail.com', 'obotetom009@gmail.com',
              'bkwainaina22@gmail.com', 'takieee123@gmail.com', 'rugambaallan@gmail.com',
              'kinyuamartin350@gmail.com', 'sdelaeugene@yahoo.com', 'maliehaa@thepeopleandplanet.group',
              'mamphojay88@gmail.com', 'chaiathman2@gmail.com', 'saliskhan24@gmail.com',
              'nkvnitezimbere.ltd@gmail.com', 'asanda@mementoholdings.com', 'stk25lee@yahoo.com',
              'albertmutombok@gmail.com', 'abrahamajala1339@gmail.com'],
    'Action': ['JUST CLICK SUBMIT!', 'JUST CLICK SUBMIT!', 'JUST CLICK SUBMIT!',
               '1 question left', 'From Dashboard!', 'Almost there', 'Almost there', 
               'Almost there', 'Almost there', 'Almost there', 'Close', 'Close', 'Close',
               'Close', 'Follow up', 'Follow up', 'Follow up', 'Strong Pipeline Candidate!',
               'Follow up', 'Follow up']
})

def color_progress(val):
    if val >= 100:
        return 'background-color: rgba(94, 234, 212, 0.3); color: #5EEAD4; font-weight: bold'
    elif val >= 90:
        return 'background-color: rgba(16, 185, 129, 0.3); color: #34D399; font-weight: bold'
    elif val >= 70:
        return 'background-color: rgba(34, 211, 238, 0.3); color: #22D3EE'
    else:
        return ''

def color_action(val):
    if 'SUBMIT' in val:
        return 'background-color: rgba(16, 185, 129, 0.4); color: #34D399; font-weight: bold'
    elif 'Pipeline' in val or 'Dashboard' in val:
        return 'background-color: rgba(245, 158, 11, 0.4); color: #FCD34D; font-weight: bold'
    else:
        return 'background-color: rgba(34, 211, 238, 0.2); color: #22D3EE'

styled_reengage = reengage_data.style.applymap(color_progress, subset=['Progress']).applymap(color_action, subset=['Action'])
st.dataframe(styled_reengage, use_container_width=True, hide_index=True, height=500)

st.divider()

# ============ SECTION 4: Dashboard Incomplete ============
st.header("🎯 Incomplete Applications from Scouting Dashboard (12)")

dashboard_incomplete = pd.DataFrame({
    'Company': ['Furies Enterprise', 'KCG Aquatec Fish Farming', 'Trident Analitics',
                "MANMAN L'OCEAN SEASHELLES", 'OriGenes', 'TerraVerge Solutions',
                'Ecotech Naturewise', 'Trident Analitics (dup)', 'MADA-FIA',
                'Setetemela Industries', 'Mofilet', 'Kitronic Store'],
    'Progress': [97.3, 73.0, 48.6, 48.6, 45.9, 45.9, 45.9, 43.2, 43.2, 35.1, 29.7, 18.9],
    'Notion Record': ['Furies Enterprise', 'KCG Aquatec', 'Trident Analitics',
                      'MANMAN LOCEAN', 'Origenes', 'BlueEco Trak', 'EcoTech Nature',
                      'Trident Analitics', 'Mada Fia', 'Setetemela Industries', 'Mofilet', 'Kitronic Store'],
    'Dashboard Status': ['Not Started', 'Strong OH7 Candidate', 'Screened KO', 'Not Relevant',
                         'Screened KO', 'Not Started', 'Contacted', 'Screened KO', 'Screened KO',
                         "They're Interested", 'Not Started', 'Not Started'],
    'Stopped At': ['Final question!', 'Technical section', 'Post-video', 'Post-video',
                   'Pitch Video', 'Pitch Video', 'Pitch Video', 'Ocean Focus', 'Ocean Focus',
                   'Founder Structure', 'Registration', 'Personal Info']
})

def color_status(val):
    if val == 'Strong OH7 Candidate':
        return 'background-color: rgba(8, 145, 178, 0.4); color: #22D3EE; font-weight: bold'
    elif val == "They're Interested":
        return 'background-color: rgba(94, 234, 212, 0.3); color: #5EEAD4'
    elif val == 'Contacted':
        return 'background-color: rgba(34, 211, 238, 0.3); color: #22D3EE'
    elif val == 'Screened KO':
        return 'background-color: rgba(249, 115, 22, 0.3); color: #FB923C'
    elif val == 'Not Relevant':
        return 'background-color: rgba(100, 116, 139, 0.3); color: #64748B'
    else:
        return 'background-color: rgba(148, 163, 184, 0.2); color: #CBD5E1'

styled_dashboard = dashboard_incomplete.style.applymap(color_progress, subset=['Progress']).applymap(color_status, subset=['Dashboard Status'])
st.dataframe(styled_dashboard, use_container_width=True, hide_index=True)

st.markdown("""
<div class="insight-box warning">
    <strong style="color: #FB923C;">Priority Actions:</strong> 
    <span style="color: #CBD5E1;">
    <br>• <strong>Furies Enterprise</strong> (97.3%) - Just 1 question away from completion!
    <br>• <strong>KCG Aquatec</strong> (73.0%) - "Strong OH7 Pipeline Candidate" - high priority outreach
    <br>• <strong>Setetemela Industries</strong> (35.1%) - "They're Interested" - find out what's blocking them
    </span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============ SECTION 5: Completed Applications ============
st.header("✅ Completed Applications (82)")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("External / Organic", "75", "91.5%")
    
with col2:
    st.metric("From Dashboard", "7", "8.5%")
    
with col3:
    st.metric('"Definitely OH7" Converted', "3", "43% accuracy")

# Conversion table
completed_conversions = pd.DataFrame({
    'VC4A Applicant': ['BERTH Marine', 'Sea-Stematic Pty Ltd', 'VUA INC', 'Protein Hive Limited',
                       'Green Tech Africa', 'Kingfisher AG', 'MTBiofuels'],
    'Notion Record': ['BERTH', 'Sea-Stematic', 'Vua Inc', 'Protein Hive',
                      'Green Tech Africa', 'Kingfisher AG', 'MTBiofuels'],
    'Pipeline Status': ['Definitely OH7', 'Definitely OH7', 'Definitely OH7', 'Contacted',
                        'Not Started', 'Screened KO', 'Not Relevant']
})

styled_completed = completed_conversions.style.applymap(color_status, subset=['Pipeline Status'])
st.dataframe(styled_completed, use_container_width=True, hide_index=True)

st.divider()

# ============ SECTION 6: Priority Actions ============
st.header("🎯 Priority Actions")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Immediate (This Week)")
    st.error("**1. Email 3 'Just Submit' Applicants**\nPeanut Pride, ABU Abdulrahman, IFBA — 100% complete")
    st.warning("**2. Contact 17 Almost-Done (>70%)**\nPersonalized emails offering help to complete")
    st.warning("**3. Priority: KCG Aquatec (73%)**\n'Strong OH7 Pipeline Candidate' — personal outreach")
    st.info("**4. Reach Setetemela Industries**\nTagged 'They're Interested' but only 35% — find blockers")

with col2:
    st.subheader("📋 Strategic (Next Cycle)")
    st.error("**5. Fix Pitch Video Blocker**\n95 applicants (35%) stopped here. Make optional or provide templates")
    st.warning("**6. Simplify 35-45% Section**\n75 more stopped in founder/ownership questions")
    st.info("**7. Chase 13 Pipeline Candidates**\n16 tagged 'Definitely OH7'/'Strong Candidate' — only 3 completed")
    st.info("**8. Expand Nigeria Scouting**\nHighest organic interest but 5th in pipeline")

st.divider()

# ============ SUMMARY ============
st.header("📈 Full Pipeline Summary")

summary_cols = st.columns(6)

metrics = [
    ("Total Started", "357", None),
    ("Completed", "82", "23%"),
    ("Incomplete", "275", "77%"),
    ("Stopped at Video", "95", "35%"),
    ("From Dashboard", "19", None),
    ("Re-engage (>70%)", "20", None)
]

colors_summary = ['#FFFFFF', '#10B981', '#EF4444', '#F87171', '#22D3EE', '#5EEAD4']

for i, (label, value, delta) in enumerate(metrics):
    with summary_cols[i]:
        if delta:
            st.metric(label, value, delta)
        else:
            st.metric(label, value)

# Footer
st.divider()
st.caption("OceanHub Africa | OH7 Pipeline Analytics | Full Funnel Analysis")
