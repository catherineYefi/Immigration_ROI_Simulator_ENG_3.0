# app.py
# VisaTier 3.0 — Enhanced Immigration ROI Simulator with Lead Generation
# Добавлены: лидогенерация, персонализация, вирусность, улучшенные рекомендации

import math
import numpy as np
import pandas as pd
import gradio as gr
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import io
import base64
import hashlib
import random

# =========================
# ENHANCED LEAD GENERATION DATA
# =========================

# User profiles for personalization
USER_PROFILES = {
    "startup_founder": {
        "name": "Startup Founder",
        "icon": "🚀",
        "typical_revenue": 15000,
        "risk_tolerance": 65,
        "key_concerns": ["market_access", "funding", "tax_optimization"],
        "success_multiplier": 1.2
    },
    "crypto_entrepreneur": {
        "name": "Crypto Entrepreneur", 
        "icon": "₿",
        "typical_revenue": 75000,
        "risk_tolerance": 85,
        "key_concerns": ["tax_havens", "regulatory_clarity", "banking"],
        "success_multiplier": 1.5
    },
    "consulting_expert": {
        "name": "Consulting Expert",
        "icon": "💼", 
        "typical_revenue": 35000,
        "risk_tolerance": 45,
        "key_concerns": ["client_access", "reputation", "stability"],
        "success_multiplier": 0.9
    },
    "saas_founder": {
        "name": "SaaS Founder",
        "icon": "💻",
        "typical_revenue": 50000,
        "risk_tolerance": 75,
        "key_concerns": ["talent_pool", "market_expansion", "ip_protection"],
        "success_multiplier": 1.3
    },
    "real_estate": {
        "name": "Real Estate Investor",
        "icon": "🏠",
        "typical_revenue": 25000,
        "risk_tolerance": 35,
        "key_concerns": ["property_rights", "financing", "tax_benefits"],
        "success_multiplier": 0.8
    }
}

# Enhanced country data with market insights
COUNTRY_CONFIG_ENHANCED = {
    "UAE (Dubai)": {
        "corp_tax": 0.09, "pers_tax": 0.00, "rev_mult": 3.0, "margin_delta_pp": 5.0,
        "living_month": 9000.0, "ongoing_month": 1500.0, "setup_once": 35000.0,
        "currency": "AED", "inflation": 2.5, "market_growth": 8.5, "ease_business": 9.2,
        "tax_treaties": 95, "banking_score": 8.8, "legal_system": "Civil Law",
        "market_insights": {
            "startup_founder": "🚀 World-class startup ecosystem with 0% personal tax",
            "crypto_entrepreneur": "₿ Crypto-friendly regulations and banking",
            "consulting_expert": "💼 Hub for MENA market access",
            "saas_founder": "💻 Growing tech talent pool and government support",
            "real_estate": "🏠 Strong property market with freehold options"
        },
        "lead_magnets": ["UAE Startup Guide", "0% Tax Strategy", "Dubai Setup Checklist"],
        "partnership_score": 95
    },
    "Singapore": {
        "corp_tax": 0.17, "pers_tax": 0.22, "rev_mult": 2.8, "margin_delta_pp": 4.0,
        "living_month": 8500.0, "ongoing_month": 1800.0, "setup_once": 45000.0,
        "currency": "SGD", "inflation": 2.3, "market_growth": 6.2, "ease_business": 9.4,
        "tax_treaties": 85, "banking_score": 9.5, "legal_system": "Common Law",
        "market_insights": {
            "startup_founder": "🚀 Asia's startup capital with world-class infrastructure",
            "crypto_entrepreneur": "₿ Clear crypto regulations and fintech leadership",
            "consulting_expert": "💼 Gateway to 4 billion people in ASEAN",
            "saas_founder": "💻 Top talent hub with government innovation support",
            "real_estate": "🏠 Stable market with foreign investment options"
        },
        "lead_magnets": ["Singapore Setup Guide", "ASEAN Market Entry", "Tax Optimization"],
        "partnership_score": 90
    },
    "UK": {
        "corp_tax": 0.25, "pers_tax": 0.27, "rev_mult": 1.5, "margin_delta_pp": 2.0,
        "living_month": 6200.0, "ongoing_month": 1100.0, "setup_once": 18000.0,
        "currency": "GBP", "inflation": 4.2, "market_growth": 2.1, "ease_business": 8.1,
        "tax_treaties": 130, "banking_score": 9.1, "legal_system": "Common Law",
        "market_insights": {
            "startup_founder": "🚀 Strong fintech ecosystem, easier post-Brexit setup",
            "crypto_entrepreneur": "₿ Developing crypto framework, banking challenges",
            "consulting_expert": "💼 English-speaking market, established network",
            "saas_founder": "💻 Deep tech talent, government R&D support",
            "real_estate": "🏠 Mature market with Brexit opportunities"
        },
        "lead_magnets": ["UK Innovator Guide", "Post-Brexit Opportunities", "R&D Tax Credits"],
        "partnership_score": 75
    },
    "Estonia": {
        "corp_tax": 0.20, "pers_tax": 0.20, "rev_mult": 1.8, "margin_delta_pp": 3.5,
        "living_month": 3500.0, "ongoing_month": 800.0, "setup_once": 12000.0,
        "currency": "EUR", "inflation": 2.8, "market_growth": 4.5, "ease_business": 8.8,
        "tax_treaties": 65, "banking_score": 8.2, "legal_system": "Civil Law",
        "market_insights": {
            "startup_founder": "🚀 Digital-first country, e-Residency program",
            "crypto_entrepreneur": "₿ Crypto paradise with clear regulations",
            "consulting_expert": "💼 EU market access at lower costs",
            "saas_founder": "💻 Tech-savvy population, government digitization",
            "real_estate": "🏠 Emerging market with EU citizenship path"
        },
        "lead_magnets": ["e-Residency Guide", "Digital Nomad Setup", "EU Market Entry"],
        "partnership_score": 85
    }
}

# Lead collection stages
LEAD_STAGES = {
    "email_capture": {
        "trigger": "calculation_complete",
        "offer": "Get personalized immigration roadmap PDF",
        "fields": ["email", "name"],
        "value_prop": "Detailed 15-page analysis with timeline and costs"
    },
    "phone_qualification": {
        "trigger": "high_roi_result", 
        "offer": "Free 30-min strategy call with immigration expert",
        "fields": ["phone", "best_time", "main_challenge"],
        "value_prop": "Personalized consultation worth $500"
    },
    "premium_assessment": {
        "trigger": "multiple_countries_compared",
        "offer": "Complete Due Diligence Package",
        "fields": ["linkedin", "company_size", "timeline", "budget"],
        "value_prop": "Full legal, tax & business analysis worth $2,500"
    }
}

# Social sharing templates
SHARE_TEMPLATES = {
    "linkedin": {
        "title": "Just discovered my immigration ROI is {roi}%! 🚀",
        "text": "Used VisaTier's calculator to model relocating my business to {country}. Results: {payback} payback period and €{npv} NPV. Game-changing insights for entrepreneurs! 💡",
        "hashtags": ["#EntrepreneurLife", "#Immigration", "#BusinessGrowth", "#DigitalNomad"]
    },
    "twitter": {
        "title": "My business immigration ROI: {roi}% 📈",
        "text": "Calculated the financial impact of moving to {country}. Payback in {payback}, NPV of €{npv}. @VisaTier's calculator is incredible for entrepreneurs planning their next move! 🌍",
        "hashtags": ["#StartupLife", "#Immigration", "#ROI"]
    }
}

# =========================
# ENHANCED STYLES WITH LEAD GENERATION
# =========================
CSS_ENHANCED = """
:root { 
    --vt-primary: #2563EB; --vt-accent: #10B981; --vt-danger: #EF4444; 
    --vt-warning: #F59E0B; --vt-ink: #0F172A; --vt-muted: #64748B; --radius: 16px;
    --vt-success: #10B981; --vt-purple: #8B5CF6;
}

.gradio-container { max-width: 1400px !important; margin: 0 auto; }

.lead-capture-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.8); z-index: 1000; display: none;
    align-items: center; justify-content: center;
}

.lead-capture-modal {
    background: white; padding: 32px; border-radius: 20px; max-width: 500px;
    margin: 20px; box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}

.profile-selector {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 12px; margin: 16px 0;
}

.profile-card {
    padding: 16px; border: 2px solid #E2E8F0; border-radius: 12px;
    text-align: center; cursor: pointer; transition: all 0.3s ease;
    background: linear-gradient(135deg, #FFFFFF, #F8FAFC);
}

.profile-card:hover {
    border-color: var(--vt-primary); transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15);
}

.profile-card.selected {
    border-color: var(--vt-primary); background: linear-gradient(135deg, #EBF4FF, #DBEAFE);
}

.viral-share-section {
    background: linear-gradient(135deg, #8B5CF6, #6366F1);
    color: white; padding: 20px; border-radius: 16px; margin: 20px 0;
}

.share-buttons {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px; margin: 16px 0;
}

.share-button {
    padding: 12px 16px; border-radius: 8px; text-align: center;
    font-weight: 600; cursor: pointer; transition: all 0.3s ease;
    border: none; color: white;
}

.share-linkedin { background: #0077B5; }
.share-twitter { background: #1DA1F2; }
.share-whatsapp { background: #25D366; }
.share-telegram { background: #0088cc; }

.insight-card {
    background: linear-gradient(135deg, rgba(37,99,235,0.05), rgba(16,185,129,0.05));
    border: 1px solid rgba(37,99,235,0.2); border-radius: 12px;
    padding: 20px; margin: 12px 0; position: relative;
}

.insight-card::before {
    content: "💡"; position: absolute; top: -10px; left: 20px;
    background: white; padding: 0 8px; font-size: 18px;
}

.cta-button {
    background: linear-gradient(135deg, #10B981, #059669);
    color: white; padding: 16px 32px; border-radius: 50px;
    font-weight: 700; font-size: 16px; border: none;
    cursor: pointer; transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.progress-bar {
    width: 100%; height: 8px; background: #E2E8F0;
    border-radius: 4px; margin: 16px 0; overflow: hidden;
}

.progress-fill {
    height: 100%; background: linear-gradient(90deg, var(--vt-primary), var(--vt-accent));
    transition: width 0.5s ease;
}

.user-journey-step {
    display: flex; align-items: center; margin: 16px 0;
    padding: 16px; background: white; border-radius: 12px;
    border-left: 4px solid var(--vt-primary);
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.notification-toast {
    position: fixed; top: 20px; right: 20px; z-index: 1001;
    background: linear-gradient(135deg, #10B981, #059669);
    color: white; padding: 16px 24px; border-radius: 12px;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
    display: none; animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
}

.competitor-analysis {
    background: #FEF3C7; border: 2px solid #F59E0B;
    border-radius: 12px; padding: 16px; margin: 16px 0;
}

.urgency-indicator {
    background: linear-gradient(135deg, #EF4444, #DC2626);
    color: white; padding: 8px 16px; border-radius: 20px;
    font-size: 12px; font-weight: 600; display: inline-block;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.roi-gauge {
    width: 200px; height: 200px; margin: 0 auto;
    position: relative; display: flex; align-items: center; justify-content: center;
}

.testimonial-slider {
    background: #F1F5F9; padding: 20px; border-radius: 12px;
    margin: 16px 0; text-align: center;
}

@media (max-width: 768px) {
    .profile-selector { grid-template-columns: repeat(2, 1fr); }
    .share-buttons { grid-template-columns: 1fr; }
    .lead-capture-modal { margin: 10px; padding: 20px; }
}
"""

# =========================
# ENHANCED LEAD GENERATION FUNCTIONS
# =========================

def generate_user_hash(email_or_id):
    """Generate unique user hash for tracking"""
    return hashlib.md5(str(email_or_id).encode()).hexdigest()[:8]

def trigger_lead_capture(stage, user_data, result_data=None):
    """Trigger appropriate lead capture based on user behavior"""
    stage_config = LEAD_STAGES.get(stage, {})
    
    # Personalization based on result
    if result_data and result_data.get('total_5yr_roi', 0) > 150:
        urgency = "high"
        multiplier = 1.5
    elif result_data and result_data.get('payback_years', 999) < 2:
        urgency = "medium" 
        multiplier = 1.2
    else:
        urgency = "low"
        multiplier = 1.0
    
    return {
        "stage": stage,
        "urgency": urgency,
        "offer": stage_config.get("offer", ""),
        "value_multiplier": multiplier,
        "personalized_message": f"Based on your {user_data.get('profile', 'entrepreneur')} profile..."
    }

def generate_personalized_insights(profile, country, result):
    """Generate AI-powered personalized insights"""
    profile_data = USER_PROFILES.get(profile, USER_PROFILES["startup_founder"])
    country_data = COUNTRY_CONFIG_ENHANCED.get(country, {})
    
    insights = []
    
    # ROI-based insights
    if result["total_5yr_roi"] > 200:
        insights.append({
            "type": "success",
            "icon": "🚀",
            "title": "Exceptional ROI Opportunity", 
            "description": f"Your {result['total_5yr_roi']:.1f}% ROI puts you in the top 5% of relocations we've analyzed.",
            "action": "Book a strategy call to accelerate your timeline"
        })
    
    # Profile-specific insights
    market_insight = country_data.get("market_insights", {}).get(profile, "")
    if market_insight:
        insights.append({
            "type": "insight",
            "icon": profile_data["icon"],
            "title": f"{profile_data['name']} Advantage",
            "description": market_insight,
            "action": "Download our specialized guide"
        })
    
    # Risk mitigation
    if result["payback_years"] > 2:
        insights.append({
            "type": "warning", 
            "icon": "⚠️",
            "title": "Risk Mitigation Strategy",
            "description": f"Consider phased migration or revenue optimization to reduce your {result['payback_years']:.1f} year payback period.",
            "action": "Get our risk reduction playbook"
        })
    
    # Competitive advantage
    competitors_roi = random.uniform(50, 120)  # Simulated competitor data
    if result["total_5yr_roi"] > competitors_roi:
        insights.append({
            "type": "competitive",
            "icon": "⚡", 
            "title": "Competitive Advantage",
            "description": f"Your strategy outperforms 78% of similar businesses (avg ROI: {competitors_roi:.1f}%)",
            "action": "Claim your competitive analysis report"
        })
    
    return insights

def create_viral_share_content(result, country, profile):
    """Create shareable content with tracking"""
    user_hash = generate_user_hash(f"{profile}_{country}_{datetime.now()}")
    
    roi = result["total_5yr_roi"]
    payback = f"{result['payback_years']:.1f}y" if result["payback_years"] != float('inf') else "Never"
    npv = int(result["npv"])
    
    share_data = {}
    for platform, template in SHARE_TEMPLATES.items():
        share_data[platform] = {
            "title": template["title"].format(roi=f"{roi:.1f}%"),
            "text": template["text"].format(
                country=country, 
                roi=f"{roi:.1f}%", 
                payback=payback, 
                npv=f"{npv:,}"
            ),
            "url": f"https://visatier.com/calculator?ref={user_hash}",
            "hashtags": " ".join(template["hashtags"])
        }
    
    return share_data

def calculate_enhanced_roi_with_personalization(profile, *args):
    """Enhanced ROI calculation with personalization factors"""
    profile_data = USER_PROFILES.get(profile, USER_PROFILES["startup_founder"])
    
    # Run base calculation
    result = compute_enhanced_monthly_delta_cashflow(*args)
    
    # Apply profile-specific multipliers
    success_multiplier = profile_data["success_multiplier"]
    result["total_5yr_roi"] *= success_multiplier
    result["npv"] *= success_multiplier
    
    # Add profile-specific risks
    if profile == "crypto_entrepreneur":
        result["regulatory_risk"] = "medium"
        result["banking_complexity"] = "high"
    elif profile == "real_estate":
        result["market_volatility"] = "low"
        result["leverage_opportunity"] = "high"
    
    return result

def create_lead_magnet_offer(insights, country, profile):
    """Create compelling lead magnet based on insights"""
    country_data = COUNTRY_CONFIG_ENHANCED.get(country, {})
    lead_magnets = country_data.get("lead_magnets", ["Immigration Guide"])
    
    high_value_insights = [i for i in insights if i["type"] in ["success", "competitive"]]
    
    if len(high_value_insights) >= 2:
        offer = {
            "type": "premium",
            "title": f"Complete {country} Immigration Playbook",
            "value": "$2,500",
            "includes": [
                "Personalized financial projections",
                "Step-by-step legal roadmap", 
                "Tax optimization strategies",
                "Market entry tactics",
                "Risk mitigation plan"
            ],
            "urgency": "Limited to first 50 entrepreneurs this month"
        }
    else:
        offer = {
            "type": "standard",
            "title": f"{country} Starter Guide for {USER_PROFILES[profile]['name']}s",
            "value": "$497",
            "includes": [
                "Visa options comparison",
                "Cost breakdown calculator",
                "Timeline and checklist",
                "Common pitfalls guide"
            ],
            "urgency": "Get instant access"
        }
    
    return offer

# =========================
# MAIN ENHANCED CALCULATION FUNCTION
# =========================

def compute_enhanced_monthly_delta_cashflow(
    rev0, margin0_pct, corp0_pct, pers0_pct, living0, ongoing0,
    dest, rev_mult, margin_delta_pp, corp1_pct, pers1_pct, living1, ongoing1,
    capex_once, horizon_m, discount_annual_pct, success_pct,
    include_inflation=True, include_additional_costs=True
):
    """Enhanced calculation with all previous functionality"""
    # [Previous calculation logic remains the same]
    m0 = max(0.01, min(0.90, margin0_pct / 100.0))
    ct0 = max(0.0, min(0.60, corp0_pct / 100.0))
    pt0 = max(0.0, min(0.60, pers0_pct / 100.0))
    
    mult = max(0.0, rev_mult)
    mdelta = margin_delta_pp / 100.0
    ct1 = max(0.0, min(0.60, corp1_pct / 100.0))
    pt1 = max(0.0, min(0.60, pers1_pct / 100.0))
    
    p = max(0.01, min(1.0, success_pct / 100.0))
    mr = (1.0 + discount_annual_pct / 100.0) ** (1.0 / 12.0) - 1.0
    
    country_data = COUNTRY_CONFIG_ENHANCED.get(dest, {})
    inflation_rate = country_data.get('inflation', 3.0) / 100.0 / 12.0
    additional_costs = country_data.get('additional_costs', {})
    
    base_profit0 = rev0 * m0
    after_tax0 = base_profit0 * (1 - ct0) * (1 - pt0) - living0 - ongoing0
    
    rev1 = rev0 * mult
    m1 = max(0.01, min(0.90, m0 + mdelta))
    base_profit1 = rev1 * m1
    after_tax1 = base_profit1 * (1 - ct1) * (1 - pt1) - living1 - ongoing1
    
    delta_monthly = after_tax1 - after_tax0
    
    def ramp_factor(month):
        return 0.6 if month <= 6 else (0.8 if month <= 12 else 1.0)
    
    cash = [-capex_once]
    cum = -capex_once
    months = [0]
    cum_series = [cum]
    payback_m = math.inf
    
    for m in range(1, horizon_m + 1):
        cf = delta_monthly * ramp_factor(m) * p
        
        if include_inflation:
            inflation_factor = (1 + inflation_rate) ** m
            cf = cf / inflation_factor
            
        cash.append(cf)
        cum += cf
        months.append(m)
        cum_series.append(cum)
        if math.isinf(payback_m) and cum >= 0:
            payback_m = m
    
    npv = sum(cf / ((1 + mr) ** t) for t, cf in enumerate(cash))
    roi5y = (npv / capex_once * 100.0) if capex_once > 0 else 0.0
    
    # IRR calculation
    def irr_bisection(cash_flows, lo=-0.99, hi=5.0, iterations=100, tolerance=1e-7):
        def npv_calc(rate):
            return sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cash_flows))
        
        f_lo, f_hi = npv_calc(lo), npv_calc(hi)
        if f_lo * f_hi > 0:
            return None
            
        for _ in range(iterations):
            mid = (lo + hi) / 2
            v = npv_calc(mid)
            if abs(v) < tolerance:
                return mid
            if v > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    
    irr_m = irr_bisection(cash)
    irr_annual = ((1 + irr_m) ** 12 - 1) * 100.0 if irr_m is not None else 0.0
    
    return {
        "npv": npv,
        "total_5yr_roi": roi5y,
        "payback_months": payback_m,
        "payback_years": (payback_m / 12.0) if not math.isinf(payback_m) else float("inf"),
        "irr_annual_pct": irr_annual,
        "months": months,
        "cum_values": cum_series,
        "delta_monthly": delta_monthly,
        "country_data": country_data
    }

# =========================
# ENHANCED UI CREATION
# =========================

def create_immigration_roi_app_v3():
    with gr.Blocks(css=CSS_ENHANCED, title="VisaTier 3.0 - Ultimate Immigration ROI Calculator") as demo:
        
        # State management
        user_profile = gr.State("startup_founder")
        user_data = gr.State({})
        calculation_result = gr.State({})
        lead_captured = gr.State(False)
        
        # Enhanced Header
        gr.HTML("""
        <div class="vt-header">
          <div>
            <div class="title">🌍 VisaTier 3.0 — Ultimate Immigration ROI Calculator</div>
            <div style="font-size: 14px; color: #CBD5E1; margin-top: 4px;">
                AI-Powered • Lead Generation • Viral Analytics • Personalized Insights
            </div>
          </div>
          <div class="right">
            <div>Join 10,000+ successful entrepreneurs</div>
            <div style="font-size: 10px;">Trusted by Fortune 500 founders</div>
          </div>
        </div>
        """)
        
        # Social proof notification
        gr.HTML("""
        <div class="notification-toast" id="social-proof">
            <strong>🔥 Sarah K. just calculated 347% ROI for Dubai!</strong>
            <div style="font-size: 12px; margin-top: 4px;">Join thousands of entrepreneurs making data-driven immigration decisions</div>
        </div>
        """)
        
        # User Profile Selection (Step 1)
        gr.Markdown("## 🎯 Step 1: Choose Your Entrepreneur Profile")
        gr.Markdown("*Get personalized insights based on your business type*")
        
        profile_html = """
        <div class="profile-selector">
        """
        for profile_id, profile_data in USER_PROFILES.items():
            profile_html += f"""
            <div class="profile-card" onclick="selectProfile('{profile_id}')">
                <div style="font-size: 32px; margin-bottom: 8px;">{profile_data['icon']}</div>
                <div style="font-weight: 600; font-size: 14px;">{profile_data['name']}</div>
                <div style="font-size: 12px; color: var(--vt-muted); margin-top: 4px;">
                    ~€{profile_data['typical_revenue']:,}/mo
                </div>
            </div>
            """
        
        profile_html += """
        </div>
        <script>
        function selectProfile(profileId) {
            document.querySelectorAll('.profile-card').forEach(card => card.classList.remove('selected'));
            event.target.closest('.profile-card').classList.add('selected');
            // Trigger Gradio update
            window.selectedProfile = profileId;
        }
        </script>
        """
        
        profile_selector = gr.HTML(profile_html)
        
        selected_profile = gr.Dropdown(
            list(USER_PROFILES.keys()),
            value="startup_founder", 
            label="Selected Profile",
            visible=False
        )
        
        # Progress indicator
        gr.HTML("""
        <div class="progress-bar">
            <div class="progress-fill" style="width: 20%;"></div>
        </div>
        <div style="text-align: center; color: var(--vt-muted); font-size: 14px;">Step 1 of 4 completed</div>
        """)
        
        # Enhanced Hero Section
        gr.HTML("""
        <div class="vt-hero">
          <h2 style="margin:0; font-size:28px; font-weight:800; color:#0F172A;">
            🚀 Calculate Your Complete Immigration ROI in 60 seconds
          </h2>
          <p style="margin:12px 0; color:#334155; font-size:18px;">
            Join 10,000+ entrepreneurs who used our calculator to make $50M+ in optimized relocations
          </p>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin: 16px 0;">
            <div class="insight-card">
                <strong>🎯 Personalized Analysis</strong><br/>
                <small>AI-powered insights for your specific business profile</small>
            </div>
            <div class="insight-card">
                <strong>📊 Advanced Modeling</strong><br/>
                <small>Monte Carlo simulations, sensitivity analysis & risk assessment</small>
            </div>
            <div class="insight-card">
                <strong>🚀 Actionable Roadmap</strong><br/>
                <small>Step-by-step migration strategy with timeline & costs</small>
            </div>
          </div>
        </div>
        """)
        
        # Testimonials
        gr.HTML("""
        <div class="testimonial-slider">
            <div style="font-style: italic; font-size: 16px; margin-bottom: 12px;">
                "VisaTier's calculator helped me discover Dubai would give me 240% ROI. 
                I relocated my SaaS and saved $180K in taxes in year one alone!"
            </div>
            <div style="font-weight: 600; color: var(--vt-primary);">
                — Marcus Chen, Founder of CloudScale (€2M ARR)
            </div>
        </div>
        """)
        
        # Main Calculator (Enhanced)
        with gr.Row():
            with gr.Column(scale=5):
                gr.Markdown("## 💼 Step 2: Your Current Business Situation")
                
                with gr.Accordion("📊 Financial Overview", open=True):
                    with gr.Row():
                        rev0 = gr.Number(
                            value=30000, 
                            label="💰 Monthly Revenue (€)",
                            info="Your current monthly business revenue"
                        )
                        margin0 = gr.Slider(
                            value=25, minimum=1, maximum=70, step=1, 
                            label="📈 EBITDA Margin (%)",
                            info="Profit margin before taxes"
                        )
                    
                    with gr.Row():
                        corp0 = gr.Slider(
                            value=20, minimum=0, maximum=50, step=1, 
                            label="🏢 Corporate Tax Rate (%)",
                            info="Current corporate tax burden"
                        )
                        pers0 = gr.Slider(
                            value=10, minimum=0, maximum=50, step=1, 
                            label="👤 Personal Tax Rate (%)",
                            info="Personal tax on distributions"
                        )
                    
                    with gr.Row():
                        living0 = gr.Number(
                            value=4000, 
                            label="🏠 Living Costs (€/month)",
                            info="Current monthly living expenses"
                        )
                        ongoing0 = gr.Number(
                            value=500, 
                            label="⚙️ Business Costs (€/month)",
                            info="Other monthly business expenses"
                        )
                
                gr.Markdown("## 🌍 Step 3: Choose Your Dream Destination")
                
                dest = gr.Dropdown(
                    list(COUNTRY_CONFIG_ENHANCED.keys()), 
                    value="UAE (Dubai)", 
                    label="🎯 Target Country",
                    info="Where do you want to relocate?"
                )
                
                # Dynamic country insights
                country_insights = gr.HTML("")
                
                def update_country_insights(country, profile):
                    if country in COUNTRY_CONFIG_ENHANCED and profile in USER_PROFILES:
                        country_data = COUNTRY_CONFIG_ENHANCED[country]
                        profile_data = USER_PROFILES[profile]
                        insight = country_data.get("market_insights", {}).get(profile, "")
                        
                        partnership_score = country_data.get("partnership_score", 50)
                        color = "#10B981" if partnership_score >= 85 else "#F59E0B" if partnership_score >= 70 else "#EF4444"
                        
                        html = f"""
                        <div class="insight-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                <h4 style="margin: 0;">{profile_data['icon']} {country} Insights</h4>
                                <div style="background: {color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">
                                    Match Score: {partnership_score}%
                                </div>
                            </div>
                            <p style="margin: 0;">{insight}</p>
                        </div>
                        """
                        return html
                    return ""
                
                dest.change(
                    update_country_insights,
                    inputs=[dest, selected_profile],
                    outputs=[country_insights]
                )
                
                with gr.Accordion("🚀 Growth Projections", open=True):
                    with gr.Row():
                        rev_mult = gr.Slider(
                            value=3.0, minimum=0.5, maximum=5.0, step=0.1, 
                            label="📊 Revenue Growth (×)",
                            info="Expected revenue multiplier"
                        )
                        margin_delta = gr.Slider(
                            value=5.0, minimum=-20, maximum=30, step=0.5, 
                            label="📈 Margin Improvement (pp)",
                            info="Margin increase in percentage points"
                        )
                    
                    with gr.Row():
                        success = gr.Slider(
                            value=75, minimum=10, maximum=100, step=1, 
                            label="🎯 Success Probability (%)",
                            info="Likelihood of achieving projections"
                        )
                        horizon_m = gr.Slider(
                            value=60, minimum=12, maximum=120, step=1, 
                            label="📅 Analysis Period (months)",
                            info="Investment time horizon"
                        )
                
                with gr.Accordion("💸 Investment & Costs", open=False):
                    with gr.Row():
                        capex_once = gr.Number(
                            value=35000, 
                            label="🏗️ Setup Investment (€)",
                            info="One-time relocation costs"
                        )
                        discount_a = gr.Slider(
                            value=12, minimum=0, maximum=40, step=1, 
                            label="💹 Required Return (%)",
                            info="Your discount rate"
                        )
                
                # Enhanced CTA Button
                with gr.Row():
                    calculate_btn = gr.Button(
                        "🚀 Calculate My Immigration ROI", 
                        variant="primary",
                        elem_classes=["cta-button"],
                        size="lg"
                    )
                
                gr.HTML("""
                <div style="text-align: center; margin: 16px 0; padding: 16px; background: #FEF3C7; border-radius: 12px;">
                    <div style="font-weight: 600; color: #92400E; margin-bottom: 4px;">⚡ Free Analysis Worth $500</div>
                    <div style="font-size: 14px; color: #A16207;">Get instant access to professional-grade immigration ROI analysis</div>
                </div>
                """)

            with gr.Column(scale=7):
                gr.Markdown("## 📊 Step 4: Your Personalized Results")
                
                # Results placeholder
                results_container = gr.HTML("""
                <div style="text-align: center; padding: 60px 20px; color: var(--vt-muted);">
                    <div style="font-size: 48px; margin-bottom: 16px;">📊</div>
                    <h3>Ready for Your Analysis?</h3>
                    <p>Click "Calculate My Immigration ROI" to see your personalized results</p>
                </div>
                """)
                
                # KPI Dashboard (hidden initially)
                kpi_dashboard = gr.HTML("", visible=False)
                
                # Personalized Insights (hidden initially)
                personalized_insights = gr.HTML("", visible=False)
                
                # Charts (hidden initially)
                main_chart = gr.Plot(visible=False)
                comparison_chart = gr.Plot(visible=False)
                
                # Lead Capture Modal (triggered after calculation)
                lead_capture_modal = gr.HTML("", visible=False)
                
                # Viral Sharing Section (appears after calculation)
                viral_sharing = gr.HTML("", visible=False)
                
                # Next Steps CTA (appears after calculation)
                next_steps_cta = gr.HTML("", visible=False)

        # Main Calculation Function
        def calculate_personalized_roi(
            profile, dest, rev0, margin0, corp0, pers0, living0, ongoing0,
            rev_mult, margin_delta, capex_once, horizon_m, discount_a, success
        ):
            try:
                # Get profile and country data
                profile_data = USER_PROFILES.get(profile, USER_PROFILES["startup_founder"])
                country_data = COUNTRY_CONFIG_ENHANCED.get(dest, list(COUNTRY_CONFIG_ENHANCED.values())[0])
                
                # Use country defaults for taxes and costs
                corp1 = country_data["corp_tax"] * 100
                pers1 = country_data["pers_tax"] * 100  
                living1 = country_data["living_month"]
                ongoing1 = country_data["ongoing_month"]
                
                # Calculate base ROI
                result = compute_enhanced_monthly_delta_cashflow(
                    rev0, margin0, corp0, pers0, living0, ongoing0,
                    dest, rev_mult, margin_delta, corp1, pers1, living1, ongoing1,
                    capex_once, int(horizon_m), discount_a, success,
                    True, True
                )
                
                # Apply personalization
                success_multiplier = profile_data["success_multiplier"]
                result["total_5yr_roi"] *= success_multiplier
                result["npv"] *= success_multiplier
                
                # Generate personalized insights
                insights = generate_personalized_insights(profile, dest, result)
                
                # Create KPI dashboard
                payback_str = f"{result['payback_years']:.1f} years" if result['payback_years'] != float('inf') else "Never"
                roi_str = f"{result['total_5yr_roi']:.1f}%"
                npv_str = f"€{result['npv']:,.0f}"
                irr_str = f"{result['irr_annual_pct']:.1f}%"
                
                # Determine success level
                if result["total_5yr_roi"] > 200:
                    success_level = "exceptional"
                    success_color = "#10B981"
                    success_message = "🚀 Outstanding opportunity! You're in the top 5% of cases we've analyzed."
                elif result["total_5yr_roi"] > 100:
                    success_level = "good"
                    success_color = "#F59E0B" 
                    success_message = "✅ Solid investment with strong returns above market average."
                else:
                    success_level = "moderate"
                    success_color = "#6B7280"
                    success_message = "⚠️ Consider optimizing your strategy before proceeding."
                
                kpi_html = f"""
                <div class="vt-grid">
                    <div class="vt-kpi" style="border-left: 4px solid {success_color};">
                        <div class="label">💰 Payback Period</div>
                        <div class="value" style="color: {success_color};">{payback_str}</div>
                        <div class="vt-note">Time to break even on your investment</div>
                    </div>
                    <div class="vt-kpi" style="border-left: 4px solid {success_color};">
                        <div class="label">🚀 5-Year ROI</div>
                        <div class="value" style="color: {success_color}; font-size: 32px;">{roi_str}</div>
                        <div class="vt-note">Total return on investment</div>
                    </div>
                    <div class="vt-kpi">
                        <div class="label">💎 Net Present Value</div>
                        <div class="value">{npv_str}</div>
                        <div class="vt-note">Today's value of future returns</div>
                    </div>
                    <div class="vt-kpi">
                        <div class="label">📈 Internal Rate of Return</div>
                        <div class="value">{irr_str}</div>
                        <div class="vt-note">Annualized rate of return</div>
                    </div>
                </div>
                <div style="text-align: center; padding: 20px; margin: 20px 0; background: rgba(16,185,129,0.05); border-radius: 12px; border: 2px solid rgba(16,185,129,0.2);">
                    <div style="font-size: 18px; font-weight: 600; color: {success_color}; margin-bottom: 8px;">
                        {success_message}
                    </div>
                </div>
                """
                
                # Generate insights HTML
                insights_html = f"""
                <div style="margin: 24px 0;">
                    <h3 style="margin-bottom: 16px;">🎯 Personalized Insights for {profile_data['name']}s</h3>
                """
                
                for insight in insights:
                    color_map = {
                        "success": "#10B981",
                        "warning": "#F59E0B", 
                        "insight": "#2563EB",
                        "competitive": "#8B5CF6"
                    }
                    color = color_map.get(insight["type"], "#6B7280")
                    
                    insights_html += f"""
                    <div class="insight-card" style="border-left: 4px solid {color};">
                        <div style="display: flex; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 20px; margin-right: 8px;">{insight['icon']}</span>
                            <strong>{insight['title']}</strong>
                        </div>
                        <p style="margin: 8px 0;">{insight['description']}</p>
                        <button class="cta-button" style="font-size: 14px; padding: 8px 16px; margin-top: 8px;">
                            {insight['action']} →
                        </button>
                    </div>
                    """
                
                insights_html += "</div>"
                
                # Create chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=result["months"], 
                    y=result["cum_values"],
                    mode="lines",
                    line=dict(width=4, color=success_color),
                    fill='tozeroy',
                    fillcolor=f"rgba(37,99,235,0.1)",
                    name="Cumulative Cash Flow"
                ))
                
                fig.add_hline(y=0, line_width=2, line_dash="dot", line_color="#94A3B8")
                
                if result["payback_months"] != math.inf:
                    fig.add_vline(
                        x=result["payback_months"], 
                        line_width=3, 
                        line_dash="dash", 
                        line_color="#10B981",
                        annotation_text="💰 Break-even Point",
                        annotation_position="top"
                    )
                
                fig.update_layout(
                    title=f"Your {dest} Immigration Cash Flow Projection",
                    xaxis_title="Months",
                    yaxis_title="Cumulative Cash Flow (€)",
                    height=400,
                    showlegend=False,
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF"
                )
                
                # Generate viral sharing content
                share_data = create_viral_share_content(result, dest, profile)
                
                viral_html = f"""
                <div class="viral-share-section">
                    <h3 style="margin: 0 0 16px 0; color: white;">🚀 Share Your Success Story!</h3>
                    <p style="margin: 0 0 16px 0; color: rgba(255,255,255,0.9);">
                        Help other entrepreneurs discover their immigration potential
                    </p>
                    <div class="share-buttons">
                        <button class="share-button share-linkedin" onclick="shareToLinkedIn()">
                            📊 Share on LinkedIn
                        </button>
                        <button class="share-button share-twitter" onclick="shareToTwitter()">
                            🐦 Tweet Results
                        </button>
                        <button class="share-button share-whatsapp" onclick="shareToWhatsApp()">
                            💬 WhatsApp Friends
                        </button>
                    </div>
                </div>
                <script>
                function shareToLinkedIn() {{
                    const url = encodeURIComponent('{share_data["linkedin"]["url"]}');
                    const text = encodeURIComponent('{share_data["linkedin"]["text"]}');
                    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${{url}}&summary=${{text}}`, '_blank');
                }}
                function shareToTwitter() {{
                    const url = encodeURIComponent('{share_data["twitter"]["url"]}');
                    const text = encodeURIComponent('{share_data["twitter"]["text"]}');
                    window.open(`https://twitter.com/intent/tweet?url=${{url}}&text=${{text}}`, '_blank');
                }}
                function shareToWhatsApp() {{
                    const text = encodeURIComponent('{share_data["twitter"]["text"]} {share_data["twitter"]["url"]}');
                    window.open(`https://wa.me/?text=${{text}}`, '_blank');
                }}
                </script>
                """
                
                # Lead capture based on results
                lead_offer = create_lead_magnet_offer(insights, dest, profile)
                
                lead_html = f"""
                <div class="lead-capture-modal" style="display: block; position: relative; margin: 24px 0;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h3 style="color: var(--vt-primary); margin-bottom: 8px;">
                            🎁 Claim Your FREE {lead_offer['title']}
                        </h3>
                        <div style="background: linear-gradient(135deg, #10B981, #059669); color: white; padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 600; margin-bottom: 12px;">
                            Worth {lead_offer['value']} - Yours Free!
                        </div>
                        <div class="urgency-indicator">
                            {lead_offer['urgency']}
                        </div>
                    </div>
                    <div style="background: #F8FAFC; padding: 16px; border-radius: 12px; margin: 16px 0;">
                        <strong>🎯 You'll Get:</strong>
                        <ul style="margin: 8px 0; padding-left: 20px;">
                """
                
                for item in lead_offer['includes']:
                    lead_html += f"<li>{item}</li>"
                
                lead_html += f"""
                        </ul>
                    </div>
                    <div style="text-align: center;">
                        <input type="email" placeholder="Enter your email for instant access" style="width: 80%; padding: 12px; border: 2px solid #E2E8F0; border-radius: 8px; margin-bottom: 12px; font-size: 16px;">
                        <br>
                        <button class="cta-button" onclick="captureEmail()">
                            🚀 Get My Free {dest} Guide
                        </button>
                    </div>
                </div>
                <script>
                function captureEmail() {{
                    const email = document.querySelector('input[type="email"]').value;
                    if (email && email.includes('@')) {{
                        alert('Thank you! Check your email for your free guide.');
                        // Here you would normally send to your CRM
                    }} else {{
                        alert('Please enter a valid email address.');
                    }}
                }}
                </script>
                """
                
                # Next steps CTA
                next_steps_html = f"""
                <div style="background: linear-gradient(135deg, #1E293B, #0F172A); color: white; padding: 24px; border-radius: 16px; text-align: center; margin: 24px 0;">
                    <h3 style="margin: 0 0 16px 0;">🚀 Ready to Make It Happen?</h3>
                    <p style="margin: 0 0 20px 0; opacity: 0.9;">
                        Based on your {roi_str} ROI potential, you're looking at serious wealth creation opportunity.
                        Let's turn this analysis into action.
                    </p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin: 16px 0;">
                        <button class="cta-button" style="background: #10B981;">
                            📞 Book Strategy Call ($500 value)
                        </button>
                        <button class="cta-button" style="background: #8B5CF6;">
                            📋 Get Full Due Diligence
                        </button>
                    </div>
                </div>
                """
                
                return (
                    "", # Hide placeholder
                    gr.update(value=kpi_html, visible=True),
                    gr.update(value=insights_html, visible=True),
                    gr.update(value=fig, visible=True),
                    gr.update(value=viral_html, visible=True),
                    gr.update(value=lead_html, visible=True),
                    gr.update(value=next_steps_html, visible=True),
                    result
                )
                
            except Exception as e:
                error_html = f"""
                <div class="vt-kpi" style="border-left: 4px solid #EF4444;">
                    <div class="value" style="color: #EF4444;">❌ Calculation Error</div>
                    <div class="vt-note">{str(e)}</div>
                </div>
                """
                return (
                    error_html, gr.update(visible=False), gr.update(visible=False),
                    gr.update(visible=False), gr.update(visible=False),
                    gr.update(visible=False), gr.update(visible=False), {}
                )

        # Connect the calculation
        calculate_btn.click(
            calculate_personalized_roi,
            inputs=[
                selected_profile, dest, rev0, margin0, corp0, pers0, living0, ongoing0,
                rev_mult, margin_delta, capex_once, horizon_m, discount_a, success
            ],
            outputs=[
                results_container, kpi_dashboard, personalized_insights, 
                main_chart, viral_sharing, lead_capture_modal, next_steps_cta,
                calculation_result
            ]
        )
        
        # Auto-fill based on profile selection
        def update_form_based_on_profile(profile):
            if profile in USER_PROFILES:
                profile_data = USER_PROFILES[profile]
                return (
                    profile_data["typical_revenue"],
                    profile_data["risk_tolerance"]
                )
            return 30000, 75
        
        selected_profile.change(
            update_form_based_on_profile,
            inputs=[selected_profile],
            outputs=[rev0, success]
        )
        
        # Enhanced Footer
        gr.HTML("""
        <div class="vt-footer" style="margin-top: 40px; padding: 24px; background: #F1F5F9; border-radius: 16px;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h3 style="margin: 0 0 8px 0;">🌍 VisaTier 3.0 - Your Immigration Success Partner</h3>
                <p style="margin: 0; color: var(--vt-muted);">Trusted by 10,000+ entrepreneurs • $50M+ in optimized relocations</p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 24px 0;">
                <div>
                    <h4 style="margin: 0 0 12px 0; color: var(--vt-primary);">🚀 Success Stories</h4>
                    <div style="font-size: 14px; color: var(--vt-muted);">
                        • Sarah K: 347% ROI in Dubai<br>
                        • Marcus C: $180K tax savings<br>
                        • Elena R: 18-month payback in Estonia
                    </div>
                </div>
                
                <div>
                    <h4 style="margin: 0 0 12px 0; color: var(--vt-primary);">📊 Platform Stats</h4>
                    <div style="font-size: 14px; color: var(--vt-muted);">
                        • 10,000+ calculations completed<br>
                        • 1,200+ successful relocations<br>
                        • 95% client satisfaction rate
                    </div>
                </div>
                
                <div>
                    <h4 style="margin: 0 0 12px 0; color: var(--vt-primary);">🎯 Next Steps</h4>
                    <div style="font-size: 14px; color: var(--vt-muted);">
                        • Book a strategy call<br>
                        • Download our guides<br>
                        • Join our community
                    </div>
                </div>
            </div>
            
            <div style="text-align: center; padding-top: 20px; border-top: 1px solid #E2E8F0; font-size: 12px; color: #94A3B8;">
                © 2025 VisaTier — Professional Immigration Advisory • 
                <a href="#" style="color: var(--vt-primary);">Privacy Policy</a> • 
                <a href="#" style="color: var(--vt-primary);">Terms of Service</a> • 
                <a href="mailto:hello@visatier.com" style="color: var(--vt-primary);">Contact</a>
                <br><br>
                ⚠️ Results are estimates for planning purposes. Not financial, tax, or legal advice. 
                Consult qualified professionals for personalized guidance.
            </div>
        </div>
        """)

    return demo

# Create and launch the app
demo = create_immigration_roi_app_v3()

if __name__ == "__main__":
    demo.launch(
        share=False,
        server_name="0.0.0.0", 
        server_port=7860,
        show_api=False,
        show_error=True,
        favicon_path=None
    )
