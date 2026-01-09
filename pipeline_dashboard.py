import streamlit as st

st.set_page_config(
    page_title="OceanHub OH7 Pipeline Analytics",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit's default UI elements for a clean embed
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background: #0A1628;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OceanHub OH7 Pipeline Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --deep-ocean: #0A1628;
            --ocean-dark: #0F2847;
            --ocean-mid: #1A3A5C;
            --teal: #0891B2;
            --teal-light: #22D3EE;
            --seafoam: #5EEAD4;
            --coral: #F97316;
            --coral-light: #FB923C;
            --success: #10B981;
            --warning: #F59E0B;
            --danger: #EF4444;
            --text-primary: #FFFFFF;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --card-bg: rgba(255, 255, 255, 0.05);
            --card-border: rgba(255, 255, 255, 0.1);
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, var(--deep-ocean) 0%, var(--ocean-dark) 50%, var(--ocean-mid) 100%);
            min-height: 100vh;
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        .container { max-width: 1400px; margin: 0 auto; padding: 32px 24px; }
        
        header {
            text-align: center;
            margin-bottom: 48px;
            padding: 40px 0;
            border-bottom: 1px solid var(--card-border);
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--teal-light) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        
        .subtitle { color: var(--text-secondary); font-size: 1.1rem; }
        .date { color: var(--text-muted); font-size: 0.9rem; margin-top: 8px; }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin: 48px 0 24px 0;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--teal);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* Metric Cards */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .metric-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--teal), var(--teal-light));
        }
        
        .metric-card.coral::before { background: linear-gradient(90deg, var(--coral), var(--coral-light)); }
        .metric-card.success::before { background: linear-gradient(90deg, var(--success), #34D399); }
        .metric-card.warning::before { background: linear-gradient(90deg, var(--warning), #FCD34D); }
        .metric-card.danger::before { background: linear-gradient(90deg, var(--danger), #F87171); }
        
        .metric-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        
        .metric-sub { font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px; }
        
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-top: 8px;
        }
        
        .badge.coral { background: rgba(249, 115, 22, 0.2); color: var(--coral-light); }
        .badge.teal { background: rgba(34, 211, 238, 0.2); color: var(--teal-light); }
        .badge.success { background: rgba(16, 185, 129, 0.2); color: #34D399; }
        .badge.warning { background: rgba(245, 158, 11, 0.2); color: #FCD34D; }
        .badge.danger { background: rgba(239, 68, 68, 0.2); color: #F87171; }
        
        /* Charts */
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 24px;
            margin-bottom: 32px;
        }
        
        .chart-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 24px;
        }
        
        .chart-title {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text-primary);
        }
        
        /* Tables */
        .table-container {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 32px;
        }
        
        .table-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--card-border);
        }
        
        .table-header h3 { font-size: 1rem; font-weight: 600; }
        
        table { width: 100%; border-collapse: collapse; }
        
        th {
            text-align: left;
            padding: 12px 16px;
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.03);
            border-bottom: 1px solid var(--card-border);
        }
        
        td {
            padding: 12px 16px;
            font-size: 0.85rem;
            border-bottom: 1px solid var(--card-border);
        }
        
        tr:last-child td { border-bottom: none; }
        
        .status-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        .status-definitely { background: rgba(16, 185, 129, 0.2); color: #34D399; }
        .status-strong { background: rgba(8, 145, 178, 0.2); color: var(--teal-light); }
        .status-contacted { background: rgba(34, 211, 238, 0.2); color: var(--teal-light); }
        .status-notstarted { background: rgba(148, 163, 184, 0.2); color: #CBD5E1; }
        .status-ko { background: rgba(249, 115, 22, 0.2); color: var(--coral-light); }
        .status-notrelevant { background: rgba(100, 116, 139, 0.2); color: var(--text-muted); }
        .status-interested { background: rgba(94, 234, 212, 0.2); color: var(--seafoam); }
        
        /* Insight boxes */
        .insight-box {
            background: linear-gradient(135deg, rgba(8, 145, 178, 0.15) 0%, rgba(34, 211, 238, 0.05) 100%);
            border: 1px solid rgba(34, 211, 238, 0.3);
            border-radius: 12px;
            padding: 16px 20px;
            margin: 20px 0;
        }
        
        .insight-box.warning {
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(249, 115, 22, 0.05) 100%);
            border-color: rgba(249, 115, 22, 0.3);
        }
        
        .insight-box.danger {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
            border-color: rgba(239, 68, 68, 0.3);
        }
        
        .insight-label {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }
        
        .insight-label.teal { color: var(--teal-light); }
        .insight-label.coral { color: var(--coral-light); }
        .insight-label.danger { color: #F87171; }
        
        .insight-text { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5; }
        
        /* Funnel */
        .funnel-item {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 6px;
        }
        
        .funnel-label {
            width: 140px;
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-align: right;
        }
        
        .funnel-bar-container {
            flex: 1;
            height: 22px;
            background: rgba(255,255,255,0.05);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .funnel-bar {
            height: 100%;
            border-radius: 4px;
        }
        
        .funnel-value {
            width: 60px;
            text-align: right;
            font-weight: 600;
            font-size: 0.85rem;
        }
        
        /* Two column */
        .two-col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }
        
        @media (max-width: 900px) {
            .two-col, .charts-grid { grid-template-columns: 1fr; }
        }
        
        /* Action items */
        .action-item {
            display: flex;
            gap: 12px;
            padding: 14px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 10px;
            margin-bottom: 10px;
        }
        
        .action-number {
            width: 28px;
            height: 28px;
            background: linear-gradient(135deg, var(--teal), var(--teal-light));
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.85rem;
            flex-shrink: 0;
        }
        
        .action-content h4 { font-size: 0.9rem; margin-bottom: 2px; }
        .action-content p { font-size: 0.8rem; color: var(--text-secondary); }
        
        .highlight { color: #F87171; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌊 OH7 Pipeline Analytics</h1>
            <p class="subtitle">Complete Application Funnel Analysis</p>
            <p class="date">Data as of January 9, 2026</p>
        </header>

        <!-- SECTION 1: Overall Funnel -->
        <h2 class="section-title"><span>📊</span> Application Funnel Overview</h2>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Applicants</div>
                <div class="metric-value">357</div>
                <div class="metric-sub">Started applications</div>
            </div>
            <div class="metric-card success">
                <div class="metric-label">Completed</div>
                <div class="metric-value">82</div>
                <div class="metric-sub">Submitted</div>
                <span class="badge success">23% completion</span>
            </div>
            <div class="metric-card danger">
                <div class="metric-label">Incomplete</div>
                <div class="metric-value">275</div>
                <div class="metric-sub">Dropped off</div>
                <span class="badge danger">77% drop-off</span>
            </div>
            <div class="metric-card warning">
                <div class="metric-label">Scouting Pipeline</div>
                <div class="metric-value">135</div>
                <div class="metric-sub">Tracked startups</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">From Dashboard</div>
                <div class="metric-value">19</div>
                <div class="metric-sub">7 completed + 12 incomplete</div>
                <span class="badge teal">14% of pipeline</span>
            </div>
        </div>

        <!-- SECTION 2: The Drop-off Crisis -->
        <h2 class="section-title"><span>🚨</span> Incomplete Applications Analysis (275)</h2>
        
        <div class="insight-box danger">
            <div class="insight-label danger">Critical Finding</div>
            <div class="insight-text">
                <strong class="highlight">95 applicants (34.5%) stopped at exactly 45.9% progress</strong> — this is where the pitch video question appears.
                90.5% of incomplete applicants never uploaded a video. This single question is your biggest conversion killer.
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-title">Drop-off Funnel by Progress Stage</div>
                <div style="padding: 12px 0;">
                    <div class="funnel-item">
                        <div class="funnel-label">0-20% (Started)</div>
                        <div class="funnel-bar-container">
                            <div class="funnel-bar" style="width: 1.8%; background: linear-gradient(90deg, #64748B, #94A3B8);"></div>
                        </div>
                        <div class="funnel-value">5</div>
                    </div>
                    <div class="funnel-item">
                        <div class="funnel-label">21-35% (Registration)</div>
                        <div class="funnel-bar-container">
                            <div class="funnel-bar" style="width: 17.8%; background: linear-gradient(90deg, #F97316, #FB923C);"></div>
                        </div>
                        <div class="funnel-value">49</div>
                    </div>
                    <div class="funnel-item">
                        <div class="funnel-label">36-45% (Pre-Video)</div>
                        <div class="funnel-bar-container">
                            <div class="funnel-bar" style="width: 27.3%; background: linear-gradient(90deg, #F59E0B, #FCD34D);"></div>
                        </div>
                        <div class="funnel-value">75</div>
                    </div>
                    <div class="funnel-item">
                        <div class="funnel-label" style="color: #F87171; font-weight: 600;">45.9% PITCH VIDEO</div>
                        <div class="funnel-bar-container">
                            <div class="funnel-bar" style="width: 34.5%; background: linear-gradient(90deg, #EF4444, #F87171);"></div>
                        </div>
                        <div class="funnel-value" style="color: #F87171;">95</div>
                    </div>
                    <div class="funnel-item">
                        <div class="funnel-label">46-70% (Working)</div>
                        <div class="funnel-bar-container">
                            <div class="funnel-bar" style="width: 11.3%; background: linear-gradient(90deg, #0891B2, #22D3EE);"></div>
                        </div>
                        <div class="funnel-value">31</div>
                    </div>
                    <div class="funnel-item">
                        <div class="funnel-label" style="color: #34D399;">71-99% (Almost!)</div>
                        <div class="funnel-bar-container">
                            <div class="funnel-bar" style="width: 6.2%; background: linear-gradient(90deg, #10B981, #34D399);"></div>
                        </div>
                        <div class="funnel-value" style="color: #34D399;">17</div>
                    </div>
                    <div class="funnel-item">
                        <div class="funnel-label" style="color: #34D399; font-weight: 600;">100% (Just submit!)</div>
                        <div class="funnel-bar-container">
                            <div class="funnel-bar" style="width: 1.1%; background: linear-gradient(90deg, #10B981, #5EEAD4);"></div>
                        </div>
                        <div class="funnel-value" style="color: #5EEAD4;">3</div>
                    </div>
                </div>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">Field Completion Rates (275 incomplete)</div>
                <canvas id="fieldChart" height="220"></canvas>
            </div>
        </div>

        <!-- High Priority Re-engagement -->
        <div class="table-container">
            <div class="table-header">
                <h3>🚀 Immediate Re-engagement: 20 Almost-Complete Applications</h3>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Progress</th>
                        <th>Email</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Peanut Pride Limited</strong></td><td><span style="color: #5EEAD4; font-weight: 700;">100%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="a6ccc9d5ced3c7c7c2c9cbc2c7c8cfc3cae6c1cbc7cfca88c5c9cb">[email&#160;protected]</a></td><td><span class="badge success">JUST CLICK SUBMIT!</span></td></tr>
                    <tr><td><strong>ABU Abdulrahman Communication</strong></td><td><span style="color: #5EEAD4; font-weight: 700;">100%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="e2838097838086978e90838a8f838cd7d1d7d1a2858f838b8ecc818d8f">[email&#160;protected]</a></td><td><span class="badge success">JUST CLICK SUBMIT!</span></td></tr>
                    <tr><td><strong>IFBA</strong></td><td><span style="color: #5EEAD4; font-weight: 700;">100%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="4425263126252d2025272b202136042329252d286a272b29">[email&#160;protected]</a></td><td><span class="badge success">JUST CLICK SUBMIT!</span></td></tr>
                    <tr><td><strong>Aquapilote</strong></td><td><span style="color: #34D399;">97.3%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="a7ccc8caced4c2c9c6c696e7c0cac6cecb89c4c8ca">[email&#160;protected]</a></td><td><span class="badge teal">1 question left</span></td></tr>
                    <tr><td><strong>Furies Enterprise</strong> ⭐</td><td><span style="color: #34D399;">97.3%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="5d2b382f3c30343e353c38316f6d6d6d1d3a303c3431733e3230">[email&#160;protected]</a></td><td><span class="badge warning">From Dashboard</span></td></tr>
                    <tr><td><strong>Obote Mixed Farm</strong></td><td><span style="color: #34D399;">94.6%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="dbb4b9b4afbeafb4b6ebebe29bbcb6bab2b7f5b8b4b6">[email&#160;protected]</a></td><td><span class="badge teal">Almost there</span></td></tr>
                    <tr><td><strong>Constantnople Enterprise</strong></td><td><span style="color: #34D399;">94.6%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="d6b4bda1b7bfb8b7bfb8b7e4e496b1bbb7bfbaf8b5b9bb">[email&#160;protected]</a></td><td><span class="badge teal">Almost there</span></td></tr>
                    <tr><td><strong>HydroTech DZ Industrial</strong></td><td><span style="color: #34D399;">94.6%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="eb9f8a80828e8e8edad9d8ab8c868a8287c5888486">[email&#160;protected]</a></td><td><span class="badge teal">Almost there</span></td></tr>
                    <tr><td><strong>Mas Technologies Ltd</strong></td><td><span style="color: #34D399;">94.6%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="6b191e0c0a06090a0a07070a052b0c060a020745080406">[email&#160;protected]</a></td><td><span class="badge teal">Almost there</span></td></tr>
                    <tr><td><strong>Mtv</strong></td><td><span style="color: #34D399;">94.6%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="204b494e5955414d415254494e13151060474d41494c0e434f4d">[email&#160;protected]</a></td><td><span class="badge teal">Almost there</span></td></tr>
                    <tr><td><strong>PENAF</strong></td><td><span style="color: #22D3EE;">91.9%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="423126272e23273725272c27023b232a2d2d6c212d2f">[email&#160;protected]</a></td><td><span class="badge teal">Close</span></td></tr>
                    <tr><td><strong>The People & Planet Group</strong></td><td><span style="color: #22D3EE;">91.9%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="3e535f52575b565f5f7e4a565b4e5b514e525b5f505a4e525f505b4a10594c514b4e">[email&#160;protected]</a></td><td><span class="badge teal">Close</span></td></tr>
                    <tr><td><strong>SKOJI FOODS and HERBS</strong></td><td><span style="color: #22D3EE;">89.2%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="d6bbb7bba6beb9bcb7afeeee96b1bbb7bfbaf8b5b9bb">[email&#160;protected]</a></td><td><span class="badge teal">Close</span></td></tr>
                    <tr><td><strong>Rafiki Peps Limited</strong></td><td><span style="color: #22D3EE;">83.8%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="72111a131b13061a1f131c4032151f131b1e5c111d1f">[email&#160;protected]</a></td><td><span class="badge teal">Close</span></td></tr>
                    <tr><td><strong>Saliskhan Global LTD</strong></td><td><span style="color: #0891B2;">75.7%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="7e0d1f12170d15161f104c4a3e19131f1712501d1113">[email&#160;protected]</a></td><td><span class="badge teal">Follow up</span></td></tr>
                    <tr><td><strong>N.KV NITEZIMBERE LTD</strong></td><td><span style="color: #0891B2;">75.7%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="8ce2e7fae2e5f8e9f6e5e1eee9fee9a2e0f8e8ccebe1ede5e0a2efe3e1">[email&#160;protected]</a></td><td><span class="badge teal">Follow up</span></td></tr>
                    <tr><td><strong>Memento Holdings</strong></td><td><span style="color: #0891B2;">75.7%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="96f7e5f7f8f2f7d6fbf3fbf3f8e2f9fef9faf2fff8f1e5b8f5f9fb">[email&#160;protected]</a></td><td><span class="badge teal">Follow up</span></td></tr>
                    <tr><td><strong>KCG Aquatec</strong> ⭐</td><td><span style="color: #0891B2;">73.0%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="dba8afb0e9eeb7bebe9ba2bab3b4b4f5b8b4b6">[email&#160;protected]</a></td><td><span class="badge warning">Strong Pipeline Candidate!</span></td></tr>
                    <tr><td><strong>Mutombo The Grace Service</strong></td><td><span style="color: #0891B2;">73.0%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="e889848a8d9a9c859d9c87858a8783a88f85898184c68b8785">[email&#160;protected]</a></td><td><span class="badge teal">Follow up</span></td></tr>
                    <tr><td><strong>Sunshine Acres Enterprise</strong></td><td><span style="color: #0891B2;">70.3%</span></td><td><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="69080b1b080108040803080508585a5a50290e04080005470a0604">[email&#160;protected]</a></td><td><span class="badge teal">Follow up</span></td></tr>
                </tbody>
            </table>
        </div>

        <!-- Incomplete from Dashboard -->
        <div class="table-container">
            <div class="table-header">
                <h3>🎯 All 12 Incomplete Applications from Scouting Dashboard</h3>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Progress</th>
                        <th>Notion Record</th>
                        <th>Dashboard Status</th>
                        <th>Stopped At</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Furies Enterprise</strong></td>
                        <td><span style="color: #34D399; font-weight: 600;">97.3%</span></td>
                        <td>Furies Enterprise</td>
                        <td><span class="status-badge status-notstarted">Not Started</span></td>
                        <td>Final question!</td>
                    </tr>
                    <tr>
                        <td><strong>KCG Aquatec Fish Farming</strong></td>
                        <td><span style="color: #22D3EE; font-weight: 600;">73.0%</span></td>
                        <td>KCG Aquatec</td>
                        <td><span class="status-badge status-strong">Strong OH7 Candidate</span></td>
                        <td>Technical section</td>
                    </tr>
                    <tr>
                        <td><strong>Trident Analitics</strong></td>
                        <td>48.6%</td>
                        <td>Trident Analitics</td>
                        <td><span class="status-badge status-ko">Screened KO</span></td>
                        <td>Post-video</td>
                    </tr>
                    <tr>
                        <td><strong>MANMAN L'OCEAN SEASHELLES</strong></td>
                        <td>48.6%</td>
                        <td>MANMAN LOCEAN</td>
                        <td><span class="status-badge status-notrelevant">Not Relevant</span></td>
                        <td>Post-video</td>
                    </tr>
                    <tr>
                        <td><strong>OriGenes</strong></td>
                        <td>45.9%</td>
                        <td>Origenes</td>
                        <td><span class="status-badge status-ko">Screened KO</span></td>
                        <td>Pitch Video</td>
                    </tr>
                    <tr>
                        <td><strong>TerraVerge Solutions</strong></td>
                        <td>45.9%</td>
                        <td>BlueEco Trak</td>
                        <td><span class="status-badge status-notstarted">Not Started</span></td>
                        <td>Pitch Video</td>
                    </tr>
                    <tr>
                        <td><strong>Ecotech Naturewise</strong></td>
                        <td>45.9%</td>
                        <td>EcoTech Nature</td>
                        <td><span class="status-badge status-contacted">Contacted</span></td>
                        <td>Pitch Video</td>
                    </tr>
                    <tr>
                        <td><strong>Trident Analitics</strong> (dup)</td>
                        <td>43.2%</td>
                        <td>Trident Analitics</td>
                        <td><span class="status-badge status-ko">Screened KO</span></td>
                        <td>Ocean Focus</td>
                    </tr>
                    <tr>
                        <td><strong>MADA-FIA</strong></td>
                        <td>43.2%</td>
                        <td>Mada Fia</td>
                        <td><span class="status-badge status-ko">Screened KO</span></td>
                        <td>Ocean Focus</td>
                    </tr>
                    <tr>
                        <td><strong>Setetemela Industries</strong></td>
                        <td>35.1%</td>
                        <td>Setetemela Industries</td>
                        <td><span class="status-badge status-interested">They're Interested</span></td>
                        <td>Founder Structure</td>
                    </tr>
                    <tr>
                        <td><strong>Mofilet</strong> (Khadija Habyby)</td>
                        <td>29.7%</td>
                        <td>Mofilet</td>
                        <td><span class="status-badge status-notstarted">Not Started</span></td>
                        <td>Registration</td>
                    </tr>
                    <tr>
                        <td><strong>Kitronic Store</strong></td>
                        <td>18.9%</td>
                        <td>Kitronic Store</td>
                        <td><span class="status-badge status-notstarted">Not Started</span></td>
                        <td>Personal Info</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- SECTION 3: Completed Applications -->
        <h2 class="section-title"><span>✅</span> Completed Applications (82)</h2>

        <div class="metrics-grid">
            <div class="metric-card coral">
                <div class="metric-label">External / Organic</div>
                <div class="metric-value">75</div>
                <div class="metric-sub">Not from scouting</div>
                <span class="badge coral">91.5%</span>
            </div>
            <div class="metric-card success">
                <div class="metric-label">From Dashboard</div>
                <div class="metric-value">7</div>
                <div class="metric-sub">Converted from pipeline</div>
                <span class="badge teal">8.5%</span>
            </div>
            <div class="metric-card">
                <div class="metric-label">"Definitely OH7" Converted</div>
                <div class="metric-value">3</div>
                <div class="metric-sub">of 7 total</div>
                <span class="badge success">43% accuracy</span>
            </div>
        </div>

        <div class="table-container">
            <div class="table-header">
                <h3>✨ Dashboard → Completed Conversions (7)</h3>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>VC4A Applicant</th>
                        <th>Notion Record</th>
                        <th>Pipeline Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>BERTH Marine</strong></td><td>BERTH</td><td><span class="status-badge status-definitely">Definitely OH7</span></td></tr>
                    <tr><td><strong>Sea-Stematic Pty Ltd</strong></td><td>Sea-Stematic</td><td><span class="status-badge status-definitely">Definitely OH7</span></td></tr>
                    <tr><td><strong>VUA INC</strong></td><td>Vua Inc</td><td><span class="status-badge status-definitely">Definitely OH7</span></td></tr>
                    <tr><td><strong>Protein Hive Limited</strong></td><td>Protein Hive</td><td><span class="status-badge status-contacted">Contacted</span></td></tr>
                    <tr><td><strong>Green Tech Africa</strong></td><td>Green Tech Africa</td><td><span class="status-badge status-notstarted">Not Started</span></td></tr>
                    <tr><td><strong>Kingfisher AG</strong></td><td>Kingfisher AG</td><td><span class="status-badge status-ko">Screened KO</span></td></tr>
                    <tr><td><strong>MTBiofuels</strong></td><td>MTBiofuels</td><td><span class="status-badge status-notrelevant">Not Relevant</span></td></tr>
                </tbody>
            </table>
        </div>

        <!-- SECTION 4: Recommendations -->
        <h2 class="section-title"><span>🎯</span> Priority Actions</h2>
        
        <div class="two-col">
            <div>
                <h3 style="font-size: 0.95rem; margin-bottom: 12px; color: #F87171;">🔥 Immediate (This Week)</h3>
                
                <div class="action-item">
                    <div class="action-number">1</div>
                    <div class="action-content">
                        <h4>Email 3 "Just Submit" Applicants</h4>
                        <p>Peanut Pride, ABU Abdulrahman, IFBA — 100% complete, just need to click submit</p>
                    </div>
                </div>
                
                <div class="action-item">
                    <div class="action-number">2</div>
                    <div class="action-content">
                        <h4>Contact 17 Almost-Done (>70%)</h4>
                        <p>Personalized emails offering to help complete — these are warm leads</p>
                    </div>
                </div>
                
                <div class="action-item">
                    <div class="action-number">3</div>
                    <div class="action-content">
                        <h4>Priority: KCG Aquatec (73%)</h4>
                        <p>"Strong OH7 Pipeline Candidate" — personal outreach to help finish</p>
                    </div>
                </div>
                
                <div class="action-item">
                    <div class="action-number">4</div>
                    <div class="action-content">
                        <h4>Reach Setetemela Industries</h4>
                        <p>Tagged "They're Interested" but only 35% — find out what's blocking them</p>
                    </div>
                </div>
            </div>
            
            <div>
                <h3 style="font-size: 0.95rem; margin-bottom: 12px; color: var(--teal-light);">📋 Strategic (Next Cycle)</h3>
                
                <div class="action-item">
                    <div class="action-number">5</div>
                    <div class="action-content">
                        <h4>Fix the Pitch Video Blocker</h4>
                        <p>95 applicants (35%) stopped here. Make optional, provide templates, or offer recording help</p>
                    </div>
                </div>
                
                <div class="action-item">
                    <div class="action-number">6</div>
                    <div class="action-content">
                        <h4>Simplify 35-45% Section</h4>
                        <p>75 more stopped in founder/ownership questions — reduce friction</p>
                    </div>
                </div>
                
                <div class="action-item">
                    <div class="action-number">7</div>
                    <div class="action-content">
                        <h4>Chase 13 Pipeline Candidates</h4>
                        <p>16 tagged "Definitely OH7" or "Strong Candidate" — only 3 completed applications</p>
                    </div>
                </div>
                
                <div class="action-item">
                    <div class="action-number">8</div>
                    <div class="action-content">
                        <h4>Expand Nigeria Scouting</h4>
                        <p>Highest organic interest but 5th in pipeline — opportunity gap</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Summary Box -->
        <div style="margin-top: 40px; padding: 28px; background: linear-gradient(135deg, var(--card-bg), rgba(8, 145, 178, 0.1)); border-radius: 16px; border: 1px solid var(--card-border);">
            <h3 style="text-align: center; margin-bottom: 20px; color: var(--teal-light);">📈 Full Pipeline Summary</h3>
            <div class="metrics-grid" style="margin-bottom: 0;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary);">357</div>
                    <div style="font-size: 0.8rem; color: var(--text-muted);">Total Started</div>
                </div>
               
'''

# Embed the HTML
st.components.v1.html(HTML_CONTENT, height=4500, scrolling=True)
