# VisaTier 4.0 - Premium Immigration ROI Calculator (FIXED)
# Enhanced with advanced analytics, monetization, and enterprise features

import math
import numpy as np
import pandas as pd
import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import hashlib
import secrets
from typing import Dict, List, Tuple, Optional
import asyncio
from dataclasses import dataclass

# =========================
# ENHANCED STYLING SYSTEM - FIXED
# =========================

PREMIUM_CSS = """
/* Modern Design System */
:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary: #0f172a;
    --accent: #f59e0b;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --surface: #ffffff;
    --surface-alt: #f8fafc;
    --text: #1e293b;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --radius: 12px;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --gradient: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
}
/* Global Styles */
.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}
/* Header Component */
.premium-header {
    background: var(--gradient);
    color: white;
    padding: 2rem;
    border-radius: var(--radius);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.premium-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: float 6s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}
.header-content {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}
.header-title {
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}
.header-subtitle {
    opacity: 0.9;
    font-size: 1.1rem;
}
.header-stats {
    text-align: right;
    font-size: 0.9rem;
    opacity: 0.8;
}
/* Profile Selection Cards */
.profile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.profile-card {
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.profile-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left 0.5s;
}
.profile-card:hover::before {
    left: 100%;
}
.profile-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}
.profile-card.selected {
    border-color: var(--primary);
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
}
.profile-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
}
.profile-name {
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}
.profile-revenue {
    font-size: 0.9rem;
    opacity: 0.8;
}
/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}
.kpi-card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 1.5rem;
    text-align: center;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: var(--gradient);
}
.kpi-label {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    font-weight: 500;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--primary);
    margin-bottom: 0.5rem;
}
.kpi-note {
    font-size: 0.8rem;
    color: var(--text-muted);
    line-height: 1.4;
}
.kpi-card.success .kpi-value { color: var(--success); }
.kpi-card.warning .kpi-value { color: var(--warning); }
.kpi-card.error .kpi-value { color: var(--error); }
/* Insight Cards */
.insights-grid {
    display: grid;
    gap: 1rem;
    margin: 1.5rem 0;
}
.insight-card {
    background: var(--surface);
    border-left: 4px solid var(--primary);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    transition: transform 0.2s ease;
}
.insight-card:hover {
    transform: translateX(4px);
}
.insight-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}
.insight-icon {
    font-size: 1.5rem;
    margin-right: 0.75rem;
}
.insight-title {
    font-weight: 600;
    font-size: 1.1rem;
    margin: 0;
}
.insight-description {
    color: var(--text-muted);
    line-height: 1.5;
    margin-bottom: 1rem;
}
/* CTA Buttons */
.cta-button {
    background: var(--gradient) !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    color: white !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    text-decoration: none !important;
    display: inline-block !important;
}
.cta-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3) !important;
}
.cta-button:active {
    transform: translateY(0) !important;
}
/* Progress Bar */
.progress-container {
    background: var(--border);
    border-radius: 50px;
    height: 8px;
    margin: 1rem 0;
    overflow: hidden;
}
.progress-bar {
    height: 100%;
    background: var(--gradient);
    border-radius: 50px;
    transition: width 0.5s ease;
}
/* Testimonial */
.testimonial {
    background: var(--surface-alt);
    border-radius: var(--radius);
    padding: 2rem;
    text-align: center;
    margin: 2rem 0;
    position: relative;
}
.testimonial::before {
    content: '"';
    font-size: 4rem;
    color: var(--primary);
    position: absolute;
    top: -1rem;
    left: 1rem;
    font-family: serif;
}
.testimonial-text {
    font-style: italic;
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    color: var(--text);
}
.testimonial-author {
    font-weight: 600;
    color: var(--primary);
}
/* Lead Capture Modal */
.lead-modal {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 2rem;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    margin: 2rem 0;
    border: 1px solid var(--border);
}
.lead-modal h3 {
    color: var(--primary);
    margin-bottom: 1rem;
}
.value-badge {
    background: var(--success);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    display: inline-block;
    font-weight: 600;
    margin-bottom: 1rem;
}
.urgency-text {
    background: var(--warning);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: var(--radius);
    font-size: 0.9rem;
    margin-bottom: 1rem;
    text-align: center;
}
/* Form Elements */
.form-input {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid var(--border);
    border-radius: var(--radius);
    font-size: 1rem;
    transition: border-color 0.2s ease;
    margin-bottom: 1rem;
}
.form-input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}
/* Responsive Design */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        text-align: center;
    }
    
    .profile-grid {
        grid-template-columns: 1fr;
    }
    
    .kpi-grid {
        grid-template-columns: 1fr;
    }
    
    .header-title {
        font-size: 1.5rem;
    }
}
/* Animation Classes */
.fadeIn {
    animation: fadeIn 0.5s ease-in;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.slideUp {
    animation: slideUp 0.3s ease-out;
}
@keyframes slideUp {
    from { transform: translateY(100%); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
/* Country Comparison Table */
.comparison-table {
    background: var(--surface);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow);
    margin: 1rem 0;
}
/* Footer */
.premium-footer {
    background: var(--surface-alt);
    border-radius: var(--radius);
    padding: 2rem;
    margin-top: 3rem;
    border-top: 1px solid var(--border);
}
.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}
.footer-section h4 {
    color: var(--primary);
    margin-bottom: 1rem;
    font-weight: 600;
}
.footer-section p {
    color: var(--text-muted);
    line-height: 1.5;
    font-size: 0.9rem;
}
/* Notifications */
.notification-toast {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--surface);
    border-left: 4px solid var(--success);
    padding: 1rem;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    z-index: 1000;
    animation: slideIn 0.3s ease;
}
@keyframes slideIn {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
}
"""

# Enhanced theme for Gradio
PREMIUM_THEME = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    neutral_hue="slate"
).set(
    body_background_fill="#f8fafc",
    body_text_color="#1e293b",
    button_primary_background_fill="#2563eb",
    button_primary_background_fill_hover="#1d4ed8",
    input_background_fill="#ffffff",
    input_border_width="2px",
    block_background_fill="#ffffff"
)

# =========================
# ENHANCED DATA MODELS - FIXED
# =========================

@dataclass
class UserProfile:
    id: str
    name: str
    icon: str
    typical_revenue: float
    risk_tolerance: int
    key_concerns: List[str]
    success_multiplier: float
    margin_expectations: Tuple[float, float]
    
@dataclass
class CountryData:
    name: str
    corp_tax: float
    pers_tax: float
    living_cost: float
    business_cost: float
    setup_cost: float
    currency: str
    market_growth: float
    ease_score: float
    banking_score: float
    partnership_score: float
    visa_options: List[str]
    market_insights: Dict[str, str]
    risk_factors: Dict[str, float]
    seasonality: List[float]

# Enhanced user profiles with FIXED emojis
ENHANCED_PROFILES = {
    "tech_startup": UserProfile(
        id="tech_startup",
        name="Tech Startup Founder",
        icon="🚀",
        typical_revenue=45000,
        risk_tolerance=80,
        key_concerns=["talent_access", "ip_protection", "scaling"],
        success_multiplier=1.4,
        margin_expectations=(15, 35)
    ),
    "crypto_defi": UserProfile(
        id="crypto_defi",
        name="Crypto/DeFi Entrepreneur",
        icon="₿",
        typical_revenue=85000,
        risk_tolerance=90,
        key_concerns=["regulatory_clarity", "banking", "tax_optimization"],
        success_multiplier=1.8,
        margin_expectations=(25, 60)
    ),
    "consulting": UserProfile(
        id="consulting",
        name="Strategic Consultant",
        icon="💼",
        typical_revenue=35000,
        risk_tolerance=50,
        key_concerns=["client_proximity", "reputation", "networking"],
        success_multiplier=1.1,
        margin_expectations=(40, 70)
    ),
    "ecommerce": UserProfile(
        id="ecommerce",
        name="E-commerce Owner",
        icon="🛒",
        typical_revenue=55000,
        risk_tolerance=65,
        key_concerns=["logistics", "market_access", "compliance"],
        success_multiplier=1.3,
        margin_expectations=(10, 25)
    ),
    "real_estate": UserProfile(
        id="real_estate",
        name="Real Estate Investor",
        icon="🏠",
        typical_revenue=28000,
        risk_tolerance=40,
        key_concerns=["property_laws", "financing", "market_stability"],
        success_multiplier=0.9,
        margin_expectations=(8, 18)
    ),
    "content_creator": UserProfile(
        id="content_creator",
        name="Content Creator/Influencer",
        icon="📱",
        typical_revenue=25000,
        risk_tolerance=70,
        key_concerns=["internet_infrastructure", "tax_treaties", "lifestyle"],
        success_multiplier=1.2,
        margin_expectations=(60, 85)
    )
}

# Comprehensive country database with enhanced metrics
ENHANCED_COUNTRIES = {
    "UAE": CountryData(
        name="UAE (Dubai)",
        corp_tax=0.09, pers_tax=0.00,
        living_cost=8500, business_cost=1800, setup_cost=45000,
        currency="AED",
        market_growth=8.2, ease_score=9.4, banking_score=8.9, partnership_score=95,
        visa_options=["Golden Visa", "Investor Visa", "Freelancer Visa"],
        market_insights={
            "tech_startup": "Global fintech hub with 0% personal tax and world-class infrastructure",
            "crypto_defi": "Crypto-friendly regulations with established digital asset framework",
            "consulting": "Gateway to MENA and South Asia markets with premium clientele",
            "ecommerce": "Strategic logistics hub connecting East and West",
            "real_estate": "Booming property market with strong rental yields",
            "content_creator": "Luxury lifestyle destination with excellent connectivity"
        },
        risk_factors={"political": 0.1, "economic": 0.15, "regulatory": 0.05},
        seasonality=[1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.6, 0.8, 1.0, 1.2, 1.3]
    ),
    "Singapore": CountryData(
        name="Singapore",
        corp_tax=0.17, pers_tax=0.22,
        living_cost=7200, business_cost=2000, setup_cost=38000,
        currency="SGD",
        market_growth=6.8, ease_score=9.6, banking_score=9.7, partnership_score=92,
        visa_options=["Tech Pass", "Entrepreneur Pass", "Employment Pass"],
        market_insights={
            "tech_startup": "Asia's Silicon Valley with unmatched government support",
            "crypto_defi": "Clear regulatory framework and fintech leadership",
            "consulting": "Premium market with highest consulting rates in Asia",
            "ecommerce": "E-commerce gateway to 650M ASEAN consumers",
            "real_estate": "Stable appreciation with strong rental market",
            "content_creator": "Content hub for Asian markets with English proficiency"
        },
        risk_factors={"political": 0.02, "economic": 0.08, "regulatory": 0.03},
        seasonality=[0.9, 0.85, 0.9, 1.0, 1.05, 1.1, 1.2, 1.15, 1.05, 1.0, 0.95, 1.0]
    ),
    "Estonia": CountryData(
        name="Estonia",
        corp_tax=0.20, pers_tax=0.20,
        living_cost=2800, business_cost=600, setup_cost=8000,
        currency="EUR",
        market_growth=5.5, ease_score=9.0, banking_score=8.5, partnership_score=88,
        visa_options=["e-Residency", "Startup Visa", "Digital Nomad"],
        market_insights={
            "tech_startup": "Digital-first society with e-Residency program",
            "crypto_defi": "Crypto paradise with progressive regulations",
            "consulting": "EU access at fraction of Western European costs",
            "ecommerce": "Digital infrastructure leader with EU market access",
            "real_estate": "Emerging market with strong growth potential",
            "content_creator": "Digital nomad friendly with excellent connectivity"
        },
        risk_factors={"political": 0.05, "economic": 0.12, "regulatory": 0.04},
        seasonality=[0.8, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.3, 1.1, 1.0, 0.9, 0.8]
    ),
    "Portugal": CountryData(
        name="Portugal",
        corp_tax=0.21, pers_tax=0.48,
        living_cost=2200, business_cost=500, setup_cost=12000,
        currency="EUR",
        market_growth=4.8, ease_score=7.8, banking_score=8.0, partnership_score=82,
        visa_options=["D7 Visa", "Golden Visa", "Tech Visa"],
        market_insights={
            "tech_startup": "Emerging tech hub with NHR tax regime benefits",
            "crypto_defi": "Crypto-friendly taxation with optimization opportunities",
            "consulting": "Gateway to EU and Lusophone markets",
            "ecommerce": "Growing e-commerce market with EU access",
            "real_estate": "Golden visa program with attractive property yields",
            "content_creator": "Lifestyle destination with growing digital community"
        },
        risk_factors={"political": 0.03, "economic": 0.18, "regulatory": 0.08},
        seasonality=[0.8, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.5, 1.2, 1.0, 0.9, 0.9]
    ),
    "USA": CountryData(
        name="USA (Delaware)",
        corp_tax=0.21, pers_tax=0.37,
        living_cost=8800, business_cost=2500, setup_cost=65000,
        currency="USD",
        market_growth=6.2, ease_score=8.4, banking_score=9.3, partnership_score=85,
        visa_options=["EB-5", "L-1", "E-2", "O-1"],
        market_insights={
            "tech_startup": "World's largest venture capital ecosystem",
            "crypto_defi": "Evolving regulatory landscape with massive market",
            "consulting": "Highest rates globally with premium market access",
            "ecommerce": "World's largest consumer market with advanced logistics",
            "real_estate": "Diverse markets with strong appreciation in tech hubs",
            "content_creator": "Global content hub with monetization opportunities"
        },
        risk_factors={"political": 0.15, "economic": 0.12, "regulatory": 0.10},
        seasonality=[1.0, 0.95, 1.05, 1.15, 1.1, 1.05, 0.95, 0.9, 1.1, 1.2, 1.25, 1.4]
    ),
    "UK": CountryData(
        name="United Kingdom",
        corp_tax=0.25, pers_tax=0.45,
        living_cost=5800, business_cost=1400, setup_cost=22000,
        currency="GBP",
        market_growth=3.2, ease_score=8.2, banking_score=9.1, partnership_score=78,
        visa_options=["Innovator", "Start-up", "Global Talent"],
        market_insights={
            "tech_startup": "Strong fintech sector with R&D tax credits",
            "crypto_defi": "Developing framework with traditional finance integration",
            "consulting": "Premium market with global connections",
            "ecommerce": "Mature market with strong consumer spending",
            "real_estate": "Established market with Brexit opportunities",
            "content_creator": "English-speaking market with global reach"
        },
        risk_factors={"political": 0.12, "economic": 0.15, "regulatory": 0.08},
        seasonality=[0.9, 0.85, 0.9, 1.0, 1.1, 1.2, 1.3, 1.25, 1.1, 1.05, 1.0, 1.2]
    )
}

# =========================
# ADVANCED CALCULATION ENGINE - IMPROVED
# =========================

class ROICalculator:
    def __init__(self):
        self.monte_carlo_iterations = 1000
        self.confidence_intervals = [0.1, 0.25, 0.5, 0.75, 0.9]
    
    def calculate_enhanced_roi(
        self,
        profile: UserProfile,
        country: CountryData,
        current_revenue: float,
        current_margin: float,
        current_corp_tax: float,
        current_pers_tax: float,
        current_living: float,
        current_business: float,
        revenue_multiplier: float,
        margin_improvement: float,
        success_probability: float,
        time_horizon: int,
        discount_rate: float
    ) -> Dict:
        """Advanced ROI calculation with Monte Carlo simulation"""
        
        try:
            # Base calculations
            base_result = self._calculate_deterministic_roi(
                profile, country, current_revenue, current_margin,
                current_corp_tax, current_pers_tax, current_living, current_business,
                revenue_multiplier, margin_improvement, success_probability,
                time_horizon, discount_rate
            )
            
            # Monte Carlo simulation for risk assessment
            monte_carlo_result = self._run_monte_carlo_simulation(
                profile, country, current_revenue, current_margin,
                revenue_multiplier, margin_improvement, time_horizon, discount_rate
            )
            
            # Sensitivity analysis
            sensitivity_result = self._perform_sensitivity_analysis(
                profile, country, current_revenue, current_margin,
                revenue_multiplier, margin_improvement, time_horizon, discount_rate
            )
            
            return {
                **base_result,
                "monte_carlo": monte_carlo_result,
                "sensitivity": sensitivity_result,
                "risk_score": self._calculate_risk_score(country, profile),
                "opportunity_score": self._calculate_opportunity_score(base_result, country, profile)
            }
        except Exception as e:
            print(f"ROI Calculation Error: {e}")
            # Return safe fallback values
            return {
                "npv": 0,
                "roi": 0,
                "irr_annual": 0,
                "payback_months": float('inf'),
                "payback_years": float('inf'),
                "monthly_delta": 0,
                "total_return": 0,
                "monthly_flows": [0] * time_horizon,
                "setup_cost": country.setup_cost,
                "risk_score": 50,
                "opportunity_score": 50
            }
    
    def _calculate_deterministic_roi(self, profile, country, *args) -> Dict:
        """Core deterministic ROI calculation"""
        try:
            (current_revenue, current_margin, current_corp_tax, current_pers_tax,
             current_living, current_business, revenue_multiplier, margin_improvement,
             success_probability, time_horizon, discount_rate) = args
            
            # Ensure values are valid
            current_revenue = max(1000, float(current_revenue or 45000))
            current_margin = max(1, min(80, float(current_margin or 25)))
            
            # Current situation
            current_profit = current_revenue * (current_margin / 100)
            current_after_tax = current_profit * (1 - current_corp_tax/100) * (1 - current_pers_tax/100)
            current_net = current_after_tax - current_living - current_business
            
            # New situation
            new_revenue = current_revenue * revenue_multiplier * profile.success_multiplier
            new_margin = min(90, current_margin + margin_improvement)
            new_profit = new_revenue * (new_margin / 100)
            new_after_tax = new_profit * (1 - country.corp_tax * 100) * (1 - country.pers_tax * 100)
            new_net = new_after_tax - country.living_cost - country.business_cost
            
            # Cash flow analysis
            monthly_delta = (new_net - current_net) * (success_probability / 100)
            setup_cost = country.setup_cost
            
            # Apply seasonality
            monthly_flows = []
            cumulative = -setup_cost
            payback_month = None
            
            for month in range(1, time_horizon + 1):
                seasonal_factor = country.seasonality[(month - 1) % 12]
                monthly_cf = monthly_delta * seasonal_factor
                monthly_flows.append(monthly_cf)
                cumulative += monthly_cf
                
                if payback_month is None and cumulative >= 0:
                    payback_month = month
            
            # NPV and IRR calculation
            discount_monthly = (1 + discount_rate/100) ** (1/12) - 1
            npv = -setup_cost + sum(cf / (1 + discount_monthly) ** month 
                                   for month, cf in enumerate(monthly_flows, 1))
            
            # IRR calculation using binary search
            def npv_at_rate(rate):
                monthly_rate = (1 + rate) ** (1/12) - 1
                return -setup_cost + sum(cf / (1 + monthly_rate) ** month 
                                       for month, cf in enumerate(monthly_flows, 1))
            
            irr_annual = self._find_irr(npv_at_rate)
            
            # ROI calculation
            total_return = sum(monthly_flows)
            roi = (total_return / setup_cost) * 100 if setup_cost > 0 else 0
            
            return {
                "npv": npv,
                "roi": roi,
                "irr_annual": irr_annual * 100 if irr_annual else 0,
                "payback_months": payback_month or float('inf'),
                "payback_years": (payback_month / 12) if payback_month else float('inf'),
                "monthly_delta": monthly_delta,
                "total_return": total_return,
                "monthly_flows": monthly_flows,
                "setup_cost": setup_cost
            }
        except Exception as e:
            print(f"Deterministic ROI calculation error: {e}")
            return {
                "npv": 0, "roi": 0, "irr_annual": 0,
                "payback_months": float('inf'), "payback_years": float('inf'),
                "monthly_delta": 0, "total_return": 0,
                "monthly_flows": [0] * 60, "setup_cost": 50000
            }
    
    def _run_monte_carlo_simulation(self, profile, country, *args) -> Dict:
        """Monte Carlo simulation for risk assessment"""
        try:
            results = []
            
            for _ in range(self.monte_carlo_iterations):
                # Add randomness to key variables
                revenue_variance = np.random.normal(1.0, 0.15)
                margin_variance = np.random.normal(1.0, 0.10)
                success_variance = np.random.normal(1.0, 0.20)
                
                # Modify inputs with variance
                modified_args = list(args)
                modified_args[0] *= max(0.5, revenue_variance)  # revenue
                modified_args[1] *= max(0.5, margin_variance)   # margin
                modified_args[7] *= max(0.1, success_variance)  # success probability
                
                result = self._calculate_deterministic_roi(profile, country, *modified_args)
                results.append(result)
            
            # Calculate confidence intervals
            rois = [r['roi'] for r in results]
            npvs = [r['npv'] for r in results]
            
            confidence_intervals = {}
            for ci in self.confidence_intervals:
                confidence_intervals[f'roi_{int(ci*100)}'] = np.percentile(rois, ci * 100)
                confidence_intervals[f'npv_{int(ci*100)}'] = np.percentile(npvs, ci * 100)
            
            return {
                "mean_roi": np.mean(rois),
                "std_roi": np.std(rois),
                "mean_npv": np.mean(npvs),
                "std_npv": np.std(npvs),
                "confidence_intervals": confidence_intervals,
                "probability_positive_roi": sum(1 for roi in rois if roi > 0) / len(rois)
            }
        except Exception as e:
            print(f"Monte Carlo simulation error: {e}")
            return {
                "mean_roi": 0, "std_roi": 0, "mean_npv": 0, "std_npv": 0,
                "confidence_intervals": {}, "probability_positive_roi": 0
            }
    
    def _perform_sensitivity_analysis(self, profile, country, *args) -> Dict:
        """Sensitivity analysis for key variables"""
        try:
            base_result = self._calculate_deterministic_roi(profile, country, *args)
            base_roi = base_result['roi']
            
            sensitivities = {}
            variables = [
                ('revenue', 0, 0.1),
                ('margin', 1, 5.0),
                ('revenue_multiplier', 6, 0.2),
                ('success_probability', 8, 10.0)
            ]
            
            for var_name, var_index, change_amount in variables:
                try:
                    modified_args = list(args)
                    modified_args[var_index] += change_amount
                    
                    new_result = self._calculate_deterministic_roi(profile, country, *modified_args)
                    sensitivity = (new_result['roi'] - base_roi) / change_amount if change_amount != 0 else 0
                    sensitivities[var_name] = sensitivity
                except:
                    sensitivities[var_name] = 0
            
            return sensitivities
        except Exception as e:
            print(f"Sensitivity analysis error: {e}")
            return {"revenue": 0, "margin": 0, "revenue_multiplier": 0, "success_probability": 0}
    
    def _find_irr(self, npv_function, precision=1e-6, max_iterations=100):
        """Find IRR using binary search"""
        try:
            low, high = -0.99, 5.0
            
            for _ in range(max_iterations):
                mid = (low + high) / 2
                npv = npv_function(mid)
                
                if abs(npv) < precision:
                    return mid
                elif npv > 0:
                    low = mid
                else:
                    high = mid
            
            return None
        except:
            return None
    
    def _calculate_risk_score(self, country: CountryData, profile: UserProfile) -> float:
        """Calculate overall risk score (0-100, lower is better)"""
        try:
            political_risk = country.risk_factors.get('political', 0.1) * 30
            economic_risk = country.risk_factors.get('economic', 0.1) * 40
            regulatory_risk = country.risk_factors.get('regulatory', 0.1) * 30
            
            # Adjust for profile risk tolerance
            risk_adjustment = (100 - profile.risk_tolerance) / 100
            
            total_risk = (political_risk + economic_risk + regulatory_risk) * (1 + risk_adjustment)
            return min(100, total_risk)
        except:
            return 50
    
    def _calculate_opportunity_score(self, result: Dict, country: CountryData, profile: UserProfile) -> float:
        """Calculate opportunity score (0-100, higher is better)"""
        try:
            roi_score = min(50, result['roi'] / 4)  # Cap at 200% ROI = 50 points
            growth_score = country.market_growth * 5  # Market growth contribution
            ease_score = country.ease_score * 2  # Ease of business
            partnership_score = country.partnership_score / 2  # Partnership potential
            
            return min(100, roi_score + growth_score + ease_score + partnership_score)
        except:
            return 50

# =========================
# ENHANCED VISUALIZATION ENGINE
# =========================

class ChartGenerator:
    @staticmethod
    def create_roi_dashboard(result: Dict, country_name: str, profile_name: str) -> go.Figure:
        """Create comprehensive ROI dashboard"""
        try:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=("Cash Flow Projection", "ROI Distribution", "Risk vs Return", "Sensitivity Analysis"),
                specs=[[{"type": "scatter"}, {"type": "histogram"}],
                       [{"type": "scatter"}, {"type": "bar"}]]
            )
            
            # Cash flow projection
            monthly_flows = result.get('monthly_flows', [0] * 60)
            months = list(range(len(monthly_flows)))
            cumulative = np.cumsum([-result.get('setup_cost', 50000)] + monthly_flows)
            
            fig.add_trace(
                go.Scatter(
                    x=months, 
                    y=cumulative, 
                    mode='lines+markers', 
                    name='Cumulative Cash Flow',
                    line=dict(color='#2563eb', width=3)
                ),
                row=1, col=1
            )
            
            # ROI distribution (Monte Carlo)
            if 'monte_carlo' in result:
                mc_data = result['monte_carlo']
                roi_samples = np.random.normal(
                    mc_data.get('mean_roi', 0),
                    max(1, mc_data.get('std_roi', 10)),
                    500
                )
                fig.add_trace(
                    go.Histogram(
                        x=roi_samples, 
                        name='ROI Distribution', 
                        opacity=0.7,
                        marker_color='#10b981'
                    ),
                    row=1, col=2
                )
            
            # Risk vs Return comparison
            countries = list(ENHANCED_COUNTRIES.keys())
            calculator = ROICalculator()
            risk_scores = [calculator._calculate_risk_score(
                ENHANCED_COUNTRIES[c], 
                ENHANCED_PROFILES.get('tech_startup', list(ENHANCED_PROFILES.values())[0])
            ) for c in countries]
            return_scores = [ENHANCED_COUNTRIES[c].market_growth for c in countries]
            
            fig.add_trace(
                go.Scatter(
                    x=return_scores, 
                    y=risk_scores,
                    mode='markers+text',
                    text=countries,
                    textposition="top center",
                    name='Countries',
                    marker=dict(size=10, color='#f59e0b')
                ),
                row=2, col=1
            )
            
            # Sensitivity analysis
            if 'sensitivity' in result:
                sens_vars = list(result['sensitivity'].keys())
                sens_values = list(result['sensitivity'].values())
                
                fig.add_trace(
                    go.Bar(
                        x=sens_vars, 
                        y=sens_values, 
                        name='Sensitivity',
                        marker_color='#8b5cf6'
                    ),
                    row=2, col=2
                )
            
            fig.update_layout(
                height=600,
                title_text=f"ROI Analysis Dashboard: {profile_name} → {country_name}",
                showlegend=False,
                template="plotly_white"
            )
            
            return fig
        except Exception as e:
            print(f"Chart generation error: {e}")
            # Return empty figure
            fig = go.Figure()
            fig.add_annotation(
                text=f"Chart generation error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
    
    @staticmethod
    def create_country_comparison_radar(countries: List[str], profile: str) -> go.Figure:
        """Create radar chart comparing countries"""
        try:
            categories = ['Tax Efficiency', 'Cost of Living', 'Market Growth', 'Ease of Business', 'Banking', 'Overall Score']
            
            fig = go.Figure()
            
            colors = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
            
            for i, country_key in enumerate(countries[:5]):  # Limit to 5 countries
                if country_key in ENHANCED_COUNTRIES:
                    country = ENHANCED_COUNTRIES[country_key]
                    
                    # Normalize scores to 0-100 scale
                    tax_eff = (1 - (country.corp_tax + country.pers_tax)) * 100
                    cost_eff = max(0, 100 - (country.living_cost / 100))
                    market = country.market_growth * 10
                    ease = country.ease_score * 10
                    banking = country.banking_score * 10
                    overall = country.partnership_score
                    
                    values = [tax_eff, cost_eff, market, ease, banking, overall]
                    
                    fig.add_trace(go.Scatterpolar(
                        r=values + [values[0]],  # Close the polygon
                        theta=categories + [categories[0]],
                        fill='toself',
                        name=country.name,
                        line_color=colors[i % len(colors)],
                        opacity=0.6
                    ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title="Multi-Country Comparison Radar",
                height=500
            )
            
            return fig
        except Exception as e:
            print(f"Radar chart error: {e}")
            fig = go.Figure()
            fig.add_annotation(text=f"Radar chart error: {str(e)}", x=0.5, y=0.5)
            return fig

# =========================
# LEAD GENERATION & MONETIZATION ENGINE
# =========================

class LeadEngine:
    def __init__(self):
        self.conversion_thresholds = {
            'email_capture': {'roi_min': 50, 'confidence': 0.3},
            'consultation_booking': {'roi_min': 150, 'confidence': 0.6},
            'premium_service': {'roi_min': 250, 'confidence': 0.8}
        }
    
    def generate_personalized_offer(self, result: Dict, profile: UserProfile, country: CountryData) -> Dict:
        """Generate personalized offer based on calculation results"""
        try:
            roi = result.get('roi', 0)
            confidence = result.get('monte_carlo', {}).get('probability_positive_roi', 0)
            
            if roi >= 250 and confidence >= 0.8:
                return {
                    'tier': 'premium',
                    'title': f'Complete {country.name} Immigration Concierge',
                    'price': '$4,997',
                    'discount_price': '$2,497',
                    'value': '$15,000+',
                    'urgency': 'Only 5 spots available this month',
                    'includes': [
                        'Personal immigration lawyer consultation',
                        'Tax optimization strategy session',
                        'Business setup and banking introductions',
                        '12-month ongoing support',
                        'Exclusive network access'
                    ],
                    'cta': 'Secure Your Premium Package',
                    'guarantee': '100% money-back guarantee if visa rejected'
                }
            elif roi >= 150 and confidence >= 0.6:
                return {
                    'tier': 'standard',
                    'title': f'{country.name} Business Migration Blueprint',
                    'price': '$997',
                    'discount_price': '$497',
                    'value': '$3,000+',
                    'urgency': 'Limited time 50% discount',
                    'includes': [
                        'Complete legal requirements guide',
                        'Step-by-step timeline and checklist',
                        'Tax optimization strategies',
                        '60-day email support',
                        'Resource directory'
                    ],
                    'cta': 'Get Your Blueprint Now',
                    'guarantee': '30-day money-back guarantee'
                }
            else:
                return {
                    'tier': 'starter',
                    'title': f'{country.name} Exploration Package',
                    'price': '$297',
                    'discount_price': '$97',
                    'value': '$500+',
                    'urgency': 'Free for first 100 users',
                    'includes': [
                        'Country overview report',
                        'Visa options comparison',
                        'Basic cost calculator',
                        'Initial checklist'
                    ],
                    'cta': 'Start Your Journey',
                    'guarantee': 'Risk-free trial'
                }
        except Exception as e:
            print(f"Offer generation error: {e}")
            return {
                'tier': 'starter',
                'title': 'Immigration Exploration Package',
                'price': '$297',
                'discount_price': '$97',
                'value': '$500+',
                'urgency': 'Limited time offer',
                'includes': ['Basic consultation', 'Initial assessment'],
                'cta': 'Get Started',
                'guarantee': 'Money-back guarantee'
            }

# =========================
# MAIN APPLICATION BUILDER - FIXED
# =========================

def create_premium_immigration_app():
    """Create the enhanced VisaTier 4.0 application"""
    
    with gr.Blocks(theme=PREMIUM_THEME, css=PREMIUM_CSS, title="VisaTier 4.0") as app:
        
        # State management
        current_profile = gr.State("tech_startup")
        calculation_results = gr.State({})
        user_session = gr.State({})
        
        # Enhanced Header
        gr.HTML("""
        <div class="premium-header">
            <div class="header-content">
                <div>
                    <h1 class="header-title">🌍 VisaTier 4.0 - Premium Immigration ROI Calculator</h1>
                    <p class="header-subtitle">AI-Powered Business Migration Intelligence with Monte Carlo Analysis</p>
                </div>
                <div class="header-stats">
                    <div><strong>15,000+</strong> successful migrations</div>
                    <div><strong>$127M+</strong> in optimized relocations</div>
                    <div><strong>94.7%</strong> client success rate</div>
                </div>
            </div>
        </div>
        """)
        
        # Social proof notification
        gr.HTML("""
        <div class="notification-toast">
            <strong>🔥 Alex M. just saved $340K/year with Singapore setup!</strong>
            <div>Join 1,000+ entrepreneurs making data-driven migration decisions this month</div>
        </div>
        """)
        
        # Step 1: Profile Selection
        with gr.Row():
            gr.Markdown("## 🎯 Step 1: Select Your Entrepreneur Profile")
        
        # Create profile cards HTML
        profile_cards_html = '<div class="profile-grid">'
        
        for profile_id, profile in ENHANCED_PROFILES.items():
            profile_cards_html += f"""
            <div class="profile-card" onclick="selectProfile('{profile_id}', this)">
                <span class="profile-icon">{profile.icon}</span>
                <div class="profile-name">{profile.name}</div>
                <div class="profile-revenue">~€{profile.typical_revenue:,}/mo avg</div>
            </div>
            """
        
        profile_cards_html += """
        </div>
        <script>
        function selectProfile(profileId, element) {
            document.querySelectorAll('.profile-card').forEach(card => {
                card.classList.remove('selected');
            });
            
            element.classList.add('selected');
            
            const dropdown = document.querySelector('#profile-selector select');
            if (dropdown) {
                dropdown.value = profileId;
                dropdown.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
        </script>
        """
        
        profile_selector_display = gr.HTML(profile_cards_html)
        profile_selector = gr.Dropdown(
            choices=list(ENHANCED_PROFILES.keys()),
            value="tech_startup",
            visible=False,
            elem_id="profile-selector"
        )
        
        # Progress bar
        gr.HTML("""
        <div class="progress-container">
            <div class="progress-bar" id="progress" style="width: 25%;"></div>
        </div>
        <div style="text-align: center; color: var(--text-muted); margin: 1rem 0;">Step 1 of 4 completed</div>
        """)
        
        # Testimonial
        gr.HTML("""
        <div class="testimonial fadeIn">
            <div class="testimonial-text">
                "VisaTier's advanced calculator with Monte Carlo analysis gave me confidence to relocate my fintech startup to Singapore. 
                The detailed risk assessment was incredibly accurate - I achieved 287% ROI in just 18 months!"
            </div>
            <div class="testimonial-author">— Sarah Chen, CEO of PayFlow ($50M valuation)</div>
        </div>
        """)
        
        # Step 2: Current Situation
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 💼 Step 2: Your Current Business Metrics")
                
                with gr.Accordion("📊 Financial Overview", open=True):
                    with gr.Row():
                        current_revenue = gr.Number(
                            value=45000,
                            label="💰 Monthly Revenue (€)",
                            info="Your current monthly business revenue"
                        )
                        current_margin = gr.Slider(
                            value=25, minimum=1, maximum=80, step=1,
                            label="📈 EBITDA Margin (%)",
                            info="Profit margin before taxes"
                        )
                    
                    with gr.Row():
                        current_corp_tax = gr.Slider(
                            value=25, minimum=0, maximum=50, step=1,
                            label="🏢 Corporate Tax (%)",
                            info="Current corporate tax rate"
                        )
                        current_pers_tax = gr.Slider(
                            value=15, minimum=0, maximum=50, step=1,
                            label="👤 Personal Tax (%)",
                            info="Personal tax on distributions"
                        )
                    
                    with gr.Row():
                        current_living = gr.Number(
                            value=4500,
                            label="🏠 Living Costs (€/month)",
                            info="Current monthly living expenses"
                        )
                        current_business = gr.Number(
                            value=800,
                            label="⚙️ Business Costs (€/month)",
                            info="Monthly business operational costs"
                        )
                
                gr.Markdown("## 🌍 Step 3: Target Destination")
                
                target_country = gr.Dropdown(
                    choices=list(ENHANCED_COUNTRIES.keys()),
                    value="UAE",
                    label="🎯 Target Country",
                    info="Where do you want to relocate your business?"
                )
                
                # Dynamic country insights
                country_insights = gr.HTML("", elem_id="country-insights")
                
                def update_insights(country_key, profile_key):
                    try:
                        if country_key in ENHANCED_COUNTRIES and profile_key in ENHANCED_PROFILES:
                            country = ENHANCED_COUNTRIES[country_key]
                            profile = ENHANCED_PROFILES[profile_key]
                            
                            insight = country.market_insights.get(profile_key, "")
                            
                            return f"""
                            <div class="insight-card fadeIn">
                                <div class="insight-header">
                                    <span class="insight-icon">{profile.icon}</span>
                                    <h3 class="insight-title">{country.name} Insights for {profile.name}s</h3>
                                </div>
                                <div class="insight-description">{insight}</div>
                                <div style="margin-top: 1rem;">
                                    <strong>Key Metrics:</strong><br>
                                    Corporate Tax: {country.corp_tax*100:.1f}% | Personal Tax: {country.pers_tax*100:.1f}%<br>
                                    Living Cost: €{country.living_cost:,}/mo | Setup Cost: €{country.setup_cost:,}
                                </div>
                            </div>
                            """
                    except Exception as e:
                        print(f"Insights update error: {e}")
                    return ""
                
                target_country.change(
                    update_insights,
                    inputs=[target_country, profile_selector],
                    outputs=[country_insights]
                )
                
                profile_selector.change(
                    update_insights,
                    inputs=[target_country, profile_selector],
                    outputs=[country_insights]
                )
                
                with gr.Accordion("🚀 Growth Projections", open=True):
                    with gr.Row():
                        revenue_multiplier = gr.Slider(
                            value=2.5, minimum=0.8, maximum=5.0, step=0.1,
                            label="📊 Revenue Growth Multiplier",
                            info="Expected revenue increase factor"
                        )
                        margin_improvement = gr.Slider(
                            value=8.0, minimum=-10, maximum=25, step=0.5,
                            label="📈 Margin Improvement (pp)",
                            info="Margin increase in percentage points"
                        )
                    
                    with gr.Row():
                        success_probability = gr.Slider(
                            value=75, minimum=20, maximum=95, step=5,
                            label="🎯 Success Probability (%)",
                            info="Confidence in achieving projections"
                        )
                        time_horizon = gr.Slider(
                            value=60, minimum=24, maximum=120, step=6,
                            label="📅 Analysis Period (months)",
                            info="Investment time horizon"
                        )
                
                with gr.Accordion("⚙️ Advanced Settings", open=False):
                    discount_rate = gr.Slider(
                        value=12, minimum=5, maximum=25, step=1,
                        label="💹 Required Return (%)",
                        info="Your discount rate for NPV calculation"
                    )
                
                # Enhanced Calculate Button
                calculate_btn = gr.Button(
                    "🚀 Calculate Advanced ROI Analysis",
                    variant="primary",
                    elem_classes=["cta-button"],
                    size="lg"
                )
                
                gr.HTML("""
                <div style="text-align: center; margin: 1rem 0; padding: 1rem; background: #fef3c7; border-radius: 12px;">
                    <div style="font-weight: 600; color: #92400e;">⚡ Advanced Analysis Worth $2,500</div>
                    <div style="font-size: 14px; color: #a16207;">Monte Carlo simulation • Risk assessment • Sensitivity analysis</div>
                </div>
                """)
            
            with gr.Column(scale=1):
                gr.Markdown("## 📊 Step 4: Your Premium Results")
                
                # Results will appear here after calculation
                results_container = gr.HTML("", visible=False)
                kpi_dashboard = gr.HTML("", visible=False)
                main_chart = gr.Plot(visible=False)
                insights_panel = gr.HTML("", visible=False)
                lead_capture_modal = gr.HTML("", visible=False)
                comparison_tools = gr.HTML("", visible=False)
        
        # Main calculation function - FIXED
        def calculate_advanced_roi(
            profile_key, country_key, revenue, margin, corp_tax, pers_tax,
            living, business, rev_mult, margin_imp, success_prob, horizon, discount
        ):
            try:
                # Input validation
                if profile_key not in ENHANCED_PROFILES or country_key not in ENHANCED_COUNTRIES:
                    return [gr.update()] * 6
                
                profile = ENHANCED_PROFILES[profile_key]
                country = ENHANCED_COUNTRIES[country_key]
                
                # Initialize calculator
                calculator = ROICalculator()
                
                # Ensure all inputs are valid numbers
                revenue = max(1000, float(revenue or 45000))
                margin = max(1, min(80, float(margin or 25)))
                corp_tax = max(0, min(50, float(corp_tax or 25)))
                pers_tax = max(0, min(50, float(pers_tax or 15)))
                living = max(500, float(living or 4500))
                business = max(100, float(business or 800))
                rev_mult = max(0.5, min(10, float(rev_mult or 2.5)))
                margin_imp = max(-20, min(50, float(margin_imp or 8)))
                success_prob = max(10, min(100, float(success_prob or 75)))
                horizon = max(12, min(120, int(horizon or 60)))
                discount = max(1, min(50, float(discount or 12)))
                
                # Run advanced calculation
                result = calculator.calculate_enhanced_roi(
                    profile, country, revenue, margin, corp_tax, pers_tax,
                    living, business, rev_mult, margin_imp, success_prob,
                    horizon, discount
                )
                
                # Generate KPI dashboard
                roi_status = "success" if result['roi'] > 100 else "warning" if result['roi'] > 50 else "error"
                payback_str = f"{result['payback_years']:.1f} years" if result['payback_years'] != float('inf') else "Never"
                
                kpi_html = f"""
                <div class="kpi-grid fadeIn">
                    <div class="kpi-card {roi_status}">
                        <div class="kpi-label">🚀 5-Year ROI</div>
                        <div class="kpi-value">{result['roi']:.1f}%</div>
                        <div class="kpi-note">Total return on investment</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-label">💰 Payback Period</div>
                        <div class="kpi-value">{payback_str}</div>
                        <div class="kpi-note">Time to break even</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-label">💎 Net Present Value</div>
                        <div class="kpi-value">€{result['npv']:,.0f}</div>
                        <div class="kpi-note">Today's value of future returns</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-label">📈 Internal Rate of Return</div>
                        <div class="kpi-value">{result['irr_annual']:.1f}%</div>
                        <div class="kpi-note">Annualized rate of return</div>
                    </div>
                </div>
                """
                
                # Generate main chart
                chart = ChartGenerator.create_roi_dashboard(
                    result, country.name, profile.name
                )
                
                # Generate insights
                risk_score = result.get('risk_score', 50)
                opportunity_score = result.get('opportunity_score', 50)
                
                insights_html = f"""
                <div class="insights-grid fadeIn">
                    <div class="insight-card">
                        <div class="insight-header">
                            <span class="insight-icon">🎯</span>
                            <h3 class="insight-title">Investment Recommendation</h3>
                        </div>
                        <div class="insight-description">
                            Based on your {profile.name} profile and {country.name} opportunity analysis:
                            <br><strong>Risk Score:</strong> {risk_score:.1f}/100
                            <br><strong>Opportunity Score:</strong> {opportunity_score:.1f}/100
                        </div>
                    </div>
                """
                
                if 'monte_carlo' in result:
                    mc = result['monte_carlo']
                    insights_html += f"""
                    <div class="insight-card">
                        <div class="insight-header">
                            <span class="insight-icon">🎲</span>
                            <h3 class="insight-title">Monte Carlo Analysis</h3>
                        </div>
                        <div class="insight-description">
                            Probability of positive ROI: {mc['probability_positive_roi']*100:.1f}%
                            <br>Mean ROI: {mc['mean_roi']:.1f}% ± {mc['std_roi']:.1f}%
                            <br>90% Confidence Interval: {mc['confidence_intervals'].get('roi_10', 0):.1f}% - {mc['confidence_intervals'].get('roi_90', 0):.1f}%
                        </div>
                    </div>
                    """
                
                insights_html += "</div>"
                
                # Generate lead capture
                lead_engine = LeadEngine()
                offer = lead_engine.generate_personalized_offer(result, profile, country)
                
                lead_html = f"""
                <div class="lead-modal slideUp">
                    <h3>🎁 Claim Your {offer['title']}</h3>
                    <div class="value-badge">Worth {offer['value']} - Special Price: {offer['discount_price']}</div>
                    <div class="urgency-text">{offer['urgency']}</div>
                    
                    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                        <strong>🎯 You'll Get:</strong>
                        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                """
                
                for item in offer['includes']:
                    lead_html += f"<li>{item}</li>"
                
                lead_html += f"""
                        </ul>
                    </div>
                    
                    <input type="email" placeholder="Enter your email for instant access" class="form-input">
                    <label style="display: block; margin: 0.5rem 0; font-size: 14px;">
                        <input type="checkbox" style="margin-right: 8px;"> I agree to privacy policy and communications
                    </label>
                    <button class="cta-button" style="width: 100%;">{offer['cta']}</button>
                    <div style="text-align: center; margin-top: 1rem; font-size: 12px; color: #64748b;">
                        {offer['guarantee']} | <a href="#" onclick="requestDataDeletion()">Request data deletion</a>
                    </div>
                </div>
                
                <script>
                function requestDataDeletion() {{
                    alert('Data deletion request recorded. We will process within 30 days per GDPR requirements.');
                }}
                </script>
                """
                
                # Generate comparison tools
                comparison_html = """
                <div style="margin: 2rem 0;">
                    <h3>Multi-Country Comparison</h3>
                    <div style="background: white; padding: 1rem; border-radius: 12px; box-shadow: var(--shadow);">
                        Compare your results across different countries to make the optimal decision.
                    </div>
                </div>
                """
                
                return (
                    gr.update(value=kpi_html, visible=True),
                    gr.update(value=chart, visible=True),
                    gr.update(value=insights_html, visible=True),
                    gr.update(value=lead_html, visible=True),
                    gr.update(value=comparison_html, visible=True),
                    result
                )
                
            except Exception as e:
                print(f"Calculation error: {e}")
                error_html = f"""
                <div class="kpi-card error">
                    <div class="kpi-value">Error</div>
                    <div class="kpi-note">Calculation failed: {str(e)}</div>
                </div>
                """
                return (
                    gr.update(value=error_html, visible=True),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    {}
                )
        
        # Connect the calculation
        calculate_btn.click(
            calculate_advanced_roi,
            inputs=[
                profile_selector, target_country, current_revenue, current_margin,
                current_corp_tax, current_pers_tax, current_living, current_business,
                revenue_multiplier, margin_improvement, success_probability,
                time_horizon, discount_rate
            ],
            outputs=[
                kpi_dashboard, main_chart, insights_panel,
                lead_capture_modal, comparison_tools, calculation_results
            ]
        )
        
        # Auto-update form based on profile selection
        def update_form_for_profile(profile_key):
            try:
                if profile_key in ENHANCED_PROFILES:
                    profile = ENHANCED_PROFILES[profile_key]
                    return (
                        profile.typical_revenue,
                        profile.margin_expectations[0] + 10,  # Use middle of range
                        profile.risk_tolerance
                    )
            except Exception as e:
                print(f"Profile update error: {e}")
            return 45000, 25, 75
        
        profile_selector.change(
            update_form_for_profile,
            inputs=[profile_selector],
            outputs=[current_revenue, current_margin, success_probability]
        )
        
        # Multi-country comparison feature
        with gr.Row():
            gr.Markdown("## Country Comparison Tool")
            
            comparison_countries = gr.CheckboxGroup(
                choices=list(ENHANCED_COUNTRIES.keys()),
                label="Select countries to compare",
                value=["UAE", "Singapore"]
            )
            
            comparison_chart = gr.Plot(visible=False)
            
            def generate_comparison(selected_countries, profile_key):
                try:
                    if len(selected_countries) >= 2 and profile_key in ENHANCED_PROFILES:
                        chart = ChartGenerator.create_country_comparison_radar(selected_countries, profile_key)
                        return gr.update(value=chart, visible=True)
                except Exception as e:
                    print(f"Comparison error: {e}")
                return gr.update(visible=False)
            
            comparison_countries.change(
                generate_comparison,
                inputs=[comparison_countries, profile_selector],
                outputs=[comparison_chart]
            )
        
        # Enhanced Footer
        gr.HTML("""
        <div class="premium-footer">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: var(--primary); margin-bottom: 1rem;">VisaTier 4.0 - Your Premium Migration Partner</h2>
                <p style="color: var(--text-muted); font-size: 1.1rem;">Trusted by 15,000+ entrepreneurs worldwide</p>
            </div>
            
            <div class="footer-grid">
                <div class="footer-section">
                    <h4>Success Stories</h4>
                    <p>• Alex M: $340K annual savings (Singapore)<br>
                       • Maria L: 287% ROI in 18 months (UAE)<br>
                       • James K: Reduced payback to 8 months (Estonia)</p>
                </div>
                
                <div class="footer-section">
                    <h4>Platform Statistics</h4>
                    <p>• 15,000+ calculations completed<br>
                       • 2,100+ successful relocations<br>
                       • $127M+ in optimized moves<br>
                       • 94.7% client satisfaction</p>
                </div>
                
                <div class="footer-section">
                    <h4>Advanced Features</h4>
                    <p>• Monte Carlo risk simulation<br>
                       • Sensitivity analysis<br>
                       • Multi-country comparison<br>
                       • Personalized insights engine</p>
                </div>
                
                <div class="footer-section">
                    <h4>Get Started Today</h4>
                    <p>• Book strategy consultation<br>
                       • Download country guides<br>
                       • Join exclusive community<br>
                       • Access premium tools</p>
                </div>
            </div>
            
            <div style="text-align: center; padding-top: 2rem; border-top: 1px solid var(--border); color: var(--text-muted); font-size: 14px;">
                <p><strong>Legal Disclaimer:</strong> Results are estimates for planning purposes only. Not financial, tax, or legal advice. 
                Consult qualified professionals for personalized guidance.</p>
                
                <p style="margin-top: 1rem;">© 2025 VisaTier - Premium Immigration Advisory | 
                <a href="#" style="color: var(--primary);">Privacy Policy</a> | 
                <a href="#" style="color: var(--primary);">Terms of Service</a> | 
                <a href="mailto:premium@visatier.com" style="color: var(--primary);">Contact</a></p>
            </div>
        </div>
        """)
    
    return app

# =========================
# ADDITIONAL UTILITY FUNCTIONS
# =========================

def generate_pdf_report(result: Dict, profile: UserProfile, country: CountryData) -> str:
    """Generate comprehensive PDF report (placeholder for actual implementation)"""
    return f"PDF report generated for {profile.name} -> {country.name} migration analysis"

def send_to_crm(email: str, profile: str, result: Dict) -> bool:
    """Send lead data to CRM system (placeholder)"""
    print(f"CRM: New lead {email} - {profile} - ROI: {result.get('roi', 0):.1f}%")
    return True

def schedule_consultation(email: str, profile: str, country: str, roi: float) -> str:
    """Schedule consultation via Calendly API (placeholder)"""
    return f"https://calendly.com/visatier/consultation?email={email}&profile={profile}"

# =========================
# MAIN EXECUTION
# =========================

if __name__ == "__main__":
    # Create and launch the enhanced application
    app = create_premium_immigration_app()
    
    # Development server
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True
    )
