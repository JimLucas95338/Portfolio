#!/usr/bin/env python3
"""
AI Marketing Intelligence Platform - Interactive Demo
Demonstrates AI-powered lead scoring, chat automation, and analytics capabilities
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
from typing import Dict, List, Tuple
import time

# Configure Streamlit page
st.set_page_config(
    page_title="AI Marketing Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .user-message {
        background: #e3f2fd;
        margin-left: auto;
        text-align: right;
    }
    
    .ai-message {
        background: #f3e5f5;
        margin-right: auto;
    }
    
    .lead-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .high-score { border-left-color: #4caf50; }
    .medium-score { border-left-color: #ff9800; }
    .low-score { border-left-color: #f44336; }
</style>
""", unsafe_allow_html=True)

class AIMarketingPlatform:
    """Main class for the AI Marketing Intelligence Platform demo"""
    
    def __init__(self):
        self.initialize_data()
    
    def initialize_data(self):
        """Initialize sample data for the demo"""
        # Sample leads data
        self.leads_data = pd.DataFrame({
            'lead_id': range(1, 101),
            'company': [f"Company {i}" for i in range(1, 101)],
            'industry': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail'], 100),
            'company_size': np.random.choice(['Startup', 'SMB', 'Mid-market', 'Enterprise'], 100),
            'job_title': np.random.choice(['CEO', 'CTO', 'VP Marketing', 'Director Sales', 'Manager'], 100),
            'website_visits': np.random.randint(1, 50, 100),
            'page_views': np.random.randint(5, 200, 100),
            'time_on_site': np.random.randint(30, 1800, 100),
            'email_opens': np.random.randint(0, 10, 100),
            'form_submissions': np.random.randint(0, 3, 100),
            'ai_score': np.random.randint(20, 95, 100),
            'conversion_probability': np.random.uniform(0.1, 0.9, 100),
            'last_activity': pd.date_range('2024-01-01', periods=100, freq='D')
        })
        
        # Sample chat conversations
        self.chat_conversations = [
            {
                'visitor': "Hi, I'm interested in learning more about your AI marketing platform.",
                'ai_response': "Hello! I'd be happy to help you learn about our AI Marketing Intelligence Platform. What specific aspect interests you most - lead scoring, chat automation, or analytics?",
                'timestamp': datetime.now() - timedelta(minutes=5)
            },
            {
                'visitor': "We're looking to improve our lead qualification process.",
                'ai_response': "Excellent! Our AI lead scoring engine can help you identify high-quality prospects automatically. It analyzes over 50 data points including website behavior, firmographics, and intent signals. Would you like me to show you how it works?",
                'timestamp': datetime.now() - timedelta(minutes=3)
            },
            {
                'visitor': "What's the typical ROI for your platform?",
                'ai_response': "Our customers typically see a 40% improvement in conversion rates and 60% reduction in manual qualification time within the first 90 days. This usually translates to 300% ROI within 6 months. Would you like to schedule a personalized demo?",
                'timestamp': datetime.now() - timedelta(minutes=1)
            }
        ]
        
        # Sample analytics data
        self.analytics_data = {
            'conversion_rate': 0.23,
            'avg_lead_score': 67.5,
            'chat_responses': 156,
            'qualified_leads': 89,
            'revenue_impact': 125000
        }
    
    def calculate_ai_score(self, lead_data: Dict) -> int:
        """Simulate AI lead scoring algorithm"""
        base_score = 50
        
        # Website engagement factors
        if lead_data['website_visits'] > 10:
            base_score += 15
        if lead_data['time_on_site'] > 300:
            base_score += 10
        if lead_data['form_submissions'] > 0:
            base_score += 20
        
        # Company factors
        if lead_data['company_size'] in ['Mid-market', 'Enterprise']:
            base_score += 10
        if lead_data['job_title'] in ['CEO', 'CTO', 'VP Marketing']:
            base_score += 15
        
        # Industry factors
        if lead_data['industry'] in ['Technology', 'Healthcare']:
            base_score += 5
        
        return min(95, max(20, base_score + random.randint(-10, 10)))
    
    def generate_ai_response(self, user_input: str) -> str:
        """Generate sophisticated AI response with lead qualification logic"""
        
        # Initialize conversation context if not exists
        if "conversation_context" not in st.session_state:
            st.session_state.conversation_context = {
                "stage": "greeting",
                "company_info": {},
                "pain_points": [],
                "budget_range": None,
                "timeline": None,
                "decision_makers": [],
                "qualification_score": 0
            }
        
        context = st.session_state.conversation_context
        user_lower = user_input.lower()
        
        # Stage 1: Greeting and Initial Engagement
        if context["stage"] == "greeting":
            if any(word in user_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
                context["stage"] = "discovery"
                return "Hello! I'm Sarah, your AI SDR assistant. I help B2B companies automate their lead qualification and boost conversion rates. What brings you to our platform today?"
            
            elif any(word in user_lower for word in ['interested', 'learn', 'platform', 'solution']):
                context["stage"] = "discovery"
                return "Great! I'd love to learn more about your company and how we can help. What's your company name and what industry are you in?"
        
        # Stage 2: Discovery and Qualification
        elif context["stage"] == "discovery":
            # Company information gathering
            if any(word in user_lower for word in ['company', 'business', 'we are', 'we\'re']):
                context["qualification_score"] += 10
                return "Thanks for sharing! What's your biggest challenge with lead qualification right now? Are you spending too much time on manual processes?"
            
            # Pain point identification
            elif any(word in user_lower for word in ['challenge', 'problem', 'issue', 'struggle', 'difficult']):
                context["qualification_score"] += 15
                context["pain_points"].append(user_input)
                return "I understand that's frustrating. How many leads do you typically process per month, and what's your current conversion rate?"
            
            # Lead volume and conversion
            elif any(word in user_lower for word in ['leads', 'conversion', 'monthly', 'per month']):
                context["qualification_score"] += 20
                return "That's helpful context. What's your current process for qualifying leads? Do you have a dedicated SDR team?"
            
            # Team and process
            elif any(word in user_lower for word in ['team', 'sdr', 'sales', 'process', 'manual']):
                context["qualification_score"] += 15
                return "Got it. What's your timeline for implementing a solution? Are you looking to make changes in the next quarter?"
        
        # Stage 3: Budget and Timeline Qualification
        elif context["stage"] == "discovery":
            # Timeline qualification
            if any(word in user_lower for word in ['timeline', 'quarter', 'month', 'soon', 'urgent']):
                context["qualification_score"] += 25
                context["timeline"] = user_input
                return "Perfect timing! What's your budget range for a marketing automation solution? We have plans starting at $299/month."
            
            # Budget qualification
            elif any(word in user_lower for word in ['budget', 'price', 'cost', 'pricing', '$']):
                context["qualification_score"] += 30
                context["budget_range"] = user_input
                return "Excellent! Based on what you've shared, I think our Professional plan at $799/month would be perfect for your needs. Would you like me to schedule a personalized demo with our solutions team?"
        
        # Stage 4: Demo Scheduling and Next Steps
        elif context["qualification_score"] >= 50:
            if any(word in user_lower for word in ['demo', 'yes', 'sure', 'schedule', 'meeting']):
                context["stage"] = "demo_scheduled"
                return "Fantastic! I'll connect you with our solutions team. They'll show you exactly how our AI SDR agent can automate your lead qualification and boost your conversion rates by 40%. What's the best email to send the calendar invite?"
            
            elif any(word in user_lower for word in ['email', '@', 'contact']):
                context["stage"] = "demo_scheduled"
                return "Perfect! I've noted your email. Our team will send you a calendar invite within the next hour. Is there anything specific you'd like to see in the demo?"
        
        # Advanced responses for specific topics
        if 'pricing' in user_lower or 'cost' in user_lower:
            return "Our pricing is based on your team size and lead volume. The Professional plan at $799/month includes unlimited AI lead scoring, chat automation, and CRM integration. Would you like a personalized quote based on your needs?"
        
        elif 'roi' in user_lower or 'return' in user_lower:
            return "Our customers typically see 40% improvement in conversion rates and 300% ROI within 6 months. One client went from 15% to 23% conversion rates in just 3 months. Would you like to see their case study?"
        
        elif 'integration' in user_lower or 'crm' in user_lower:
            return "We integrate seamlessly with Salesforce, HubSpot, Pipedrive, and Microsoft Dynamics. The setup takes less than 2 hours and includes automated lead routing. What CRM are you currently using?"
        
        elif 'features' in user_lower or 'capabilities' in user_lower:
            return "Our AI SDR agent works 24/7 across your website and email channels. Key features include real-time lead scoring, intelligent chat automation, predictive analytics, and automated meeting booking. Which feature interests you most?"
        
        elif 'competitor' in user_lower or 'alternative' in user_lower:
            return "What sets us apart is our AI-first approach. While others bolt AI onto existing platforms, we built this from the ground up for AI automation. Our lead scoring is 87% accurate vs 72% for traditional systems. What other solutions are you evaluating?"
        
        elif 'security' in user_lower or 'compliance' in user_lower:
            return "We're SOC 2 Type II compliant with AES-256 encryption. All data is stored securely and we support SSO integration. Do you have specific compliance requirements I should know about?"
        
        elif 'support' in user_lower or 'help' in user_lower:
            return "We provide 24/7 support via chat, email, and phone. Enterprise customers get dedicated success managers. Our average response time is under 2 hours. How can I help you today?"
        
        # Default response with qualification attempt
        else:
            if context["qualification_score"] < 30:
                return "That's interesting! To better understand how we can help, could you tell me about your current lead qualification process? Are you doing this manually right now?"
            else:
                return "Great question! Based on what you've shared, I think our AI Marketing Intelligence Platform could really help your team. Would you like to see a quick demo of how it works?"

def main():
    """Main application function"""
    
    # Initialize the platform
    platform = AIMarketingPlatform()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Marketing Intelligence Platform</h1>
        <p>Demonstrating AI-Powered Lead Scoring, Chat Automation & Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a demo section:",
        ["Dashboard Overview", "AI Lead Scoring", "Chat Automation", "Analytics", "CRM Integration"]
    )
    
    if page == "Dashboard Overview":
        show_dashboard_overview(platform)
    elif page == "AI Lead Scoring":
        show_lead_scoring(platform)
    elif page == "Chat Automation":
        show_chat_automation(platform)
    elif page == "Analytics":
        show_analytics(platform)
    elif page == "CRM Integration":
        show_crm_integration(platform)

def show_dashboard_overview(platform: AIMarketingPlatform):
    """Display the main dashboard overview"""
    
    st.header("📊 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Conversion Rate",
            value=f"{platform.analytics_data['conversion_rate']:.1%}",
            delta="+5.2%"
        )
    
    with col2:
        st.metric(
            label="Avg Lead Score",
            value=f"{platform.analytics_data['avg_lead_score']:.1f}",
            delta="+3.1"
        )
    
    with col3:
        st.metric(
            label="AI Responses Today",
            value=platform.analytics_data['chat_responses'],
            delta="+12"
        )
    
    with col4:
        st.metric(
            label="Revenue Impact",
            value=f"${platform.analytics_data['revenue_impact']:,}",
            delta="+$15,000"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lead Score Distribution")
        fig = px.histogram(
            platform.leads_data,
            x='ai_score',
            nbins=20,
            title="Distribution of AI Lead Scores",
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Conversion by Industry")
        industry_conversion = platform.leads_data.groupby('industry')['conversion_probability'].mean().reset_index()
        fig = px.bar(
            industry_conversion,
            x='industry',
            y='conversion_probability',
            title="Average Conversion Probability by Industry",
            color='conversion_probability',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("Recent High-Score Leads")
    high_score_leads = platform.leads_data[platform.leads_data['ai_score'] > 80].head(5)
    
    for _, lead in high_score_leads.iterrows():
        score_color = "high-score" if lead['ai_score'] > 80 else "medium-score"
        st.markdown(f"""
        <div class="lead-card {score_color}">
            <strong>{lead['company']}</strong> - {lead['industry']}<br>
            <small>Score: {lead['ai_score']} | Size: {lead['company_size']} | Role: {lead['job_title']}</small>
        </div>
        """, unsafe_allow_html=True)

def show_lead_scoring(platform: AIMarketingPlatform):
    """Display AI lead scoring demo"""
    
    st.header("🎯 AI Lead Scoring Engine")
    
    st.markdown("""
    Our AI lead scoring engine analyzes multiple data points to automatically score leads from 0-100:
    - **Website Behavior**: Page views, time on site, content engagement
    - **Firmographics**: Company size, industry, job title
    - **Intent Signals**: Form submissions, email engagement, content downloads
    - **Predictive Factors**: Historical conversion patterns, market trends
    """)
    
    # Interactive lead scoring
    st.subheader("Try the Lead Scoring Engine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Company Information**")
        company_name = st.text_input("Company Name", "TechCorp Solutions")
        industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Manufacturing", "Retail"])
        company_size = st.selectbox("Company Size", ["Startup", "SMB", "Mid-market", "Enterprise"])
        job_title = st.selectbox("Job Title", ["CEO", "CTO", "VP Marketing", "Director Sales", "Manager"])
    
    with col2:
        st.write("**Engagement Metrics**")
        website_visits = st.slider("Website Visits", 1, 50, 15)
        time_on_site = st.slider("Time on Site (seconds)", 30, 1800, 450)
        form_submissions = st.slider("Form Submissions", 0, 5, 1)
        email_opens = st.slider("Email Opens", 0, 10, 3)
    
    if st.button("Calculate AI Score"):
        lead_data = {
            'company_name': company_name,
            'industry': industry,
            'company_size': company_size,
            'job_title': job_title,
            'website_visits': website_visits,
            'time_on_site': time_on_site,
            'form_submissions': form_submissions,
            'email_opens': email_opens
        }
        
        score = platform.calculate_ai_score(lead_data)
        
        # Display score with visual indicator
        if score >= 80:
            score_color = "#4caf50"
            score_label = "High Priority"
        elif score >= 60:
            score_color = "#ff9800"
            score_label = "Medium Priority"
        else:
            score_color = "#f44336"
            score_label = "Low Priority"
        
        st.markdown(f"""
        <div class="metric-card">
            <h2 style="color: {score_color}; text-align: center;">{score}</h2>
            <h3 style="text-align: center; color: {score_color};">{score_label}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Score breakdown
        st.subheader("Score Breakdown")
        breakdown_data = {
            'Factor': ['Website Engagement', 'Company Profile', 'Job Title', 'Industry', 'Form Activity'],
            'Points': [25, 20, 15, 10, 20],
            'Max Points': [30, 25, 20, 15, 25]
        }
        
        fig = px.bar(
            breakdown_data,
            x='Factor',
            y='Points',
            title="Score Contribution by Factor",
            color='Points',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_chat_automation(platform: AIMarketingPlatform):
    """Display enhanced chat automation demo"""
    
    st.header("💬 AI SDR Agent - Intelligent Chat Automation")
    
    st.markdown("""
    Our AI SDR Agent uses advanced LLMs to:
    - **Qualify leads** through intelligent conversation flow
    - **Engage visitors** with natural, contextual responses
    - **Score prospects** in real-time based on conversation
    - **Schedule meetings** automatically when ready
    - **Learn and improve** from every interaction
    """)
    
    # Qualification Score Display
    if "conversation_context" in st.session_state:
        context = st.session_state.conversation_context
        col1, col2, col3 = st.columns(3)
        
        with col1:
            score = context.get("qualification_score", 0)
            if score >= 50:
                st.success(f"🎯 **Qualification Score: {score}/100** - Ready for Demo!")
            elif score >= 30:
                st.warning(f"⚠️ **Qualification Score: {score}/100** - Qualifying")
            else:
                st.info(f"ℹ️ **Qualification Score: {score}/100** - Discovery Phase")
        
        with col2:
            stage = context.get("stage", "greeting")
            st.metric("Conversation Stage", stage.replace("_", " ").title())
        
        with col3:
            if context.get("budget_range"):
                st.metric("Budget Qualified", "✅ Yes")
            else:
                st.metric("Budget Qualified", "❌ No")
    
    # Chat interface
    st.subheader("🤖 Live AI SDR Agent Demo")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history with enhanced styling
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"""
                <div style="background: #e3f2fd; padding: 15px; border-radius: 10px; margin: 10px 0; margin-left: 20%; border-left: 4px solid #2196f3;">
                    <strong>👤 Visitor:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f3e5f5; padding: 15px; border-radius: 10px; margin: 10px 0; margin-right: 20%; border-left: 4px solid #9c27b0;">
                    <strong>🤖 AI SDR Agent:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Enhanced chat input with quick actions
    st.subheader("💬 Start a Conversation")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input("Type your message:", key="chat_input", placeholder="Try: 'Hello, I'm interested in your platform'")
    
    with col2:
        if st.button("Send", type="primary"):
            if user_input:
                # Add user message
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_input
                })
                
                # Generate AI response
                ai_response = platform.generate_ai_response(user_input)
                
                # Add AI response
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ai_response
                })
                
                # Rerun to update chat
                st.rerun()
    
    # Quick action buttons
    st.subheader("🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👋 Say Hello"):
            st.session_state.chat_history.append({"role": "user", "content": "Hello, I'm interested in your platform"})
            ai_response = platform.generate_ai_response("Hello, I'm interested in your platform")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    with col2:
        if st.button("💰 Ask About Pricing"):
            st.session_state.chat_history.append({"role": "user", "content": "What's your pricing?"})
            ai_response = platform.generate_ai_response("What's your pricing?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    with col3:
        if st.button("📅 Request Demo"):
            st.session_state.chat_history.append({"role": "user", "content": "I'd like to schedule a demo"})
            ai_response = platform.generate_ai_response("I'd like to schedule a demo")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    with col4:
        if st.button("🔄 Reset Chat"):
            st.session_state.chat_history = []
            st.session_state.conversation_context = {
                "stage": "greeting",
                "company_info": {},
                "pain_points": [],
                "budget_range": None,
                "timeline": None,
                "decision_makers": [],
                "qualification_score": 0
            }
            st.rerun()
    
    # Enhanced sample conversations
    st.subheader("📚 Sample AI SDR Conversations")
    
    sample_conversations = [
        {
            "title": "High-Quality Lead - Tech Startup",
            "conversation": [
                ("Visitor", "Hi, I'm looking for a marketing automation solution for our startup"),
                ("AI SDR", "Hello! I'm Sarah, your AI SDR assistant. I help B2B companies automate their lead qualification and boost conversion rates. What brings you to our platform today?"),
                ("Visitor", "We're a tech startup with 50 employees, struggling with manual lead qualification"),
                ("AI SDR", "Thanks for sharing! What's your biggest challenge with lead qualification right now? Are you spending too much time on manual processes?"),
                ("Visitor", "Yes, our SDR team spends 4+ hours daily on qualification. We process about 500 leads monthly with only 15% conversion"),
                ("AI SDR", "I understand that's frustrating. That's a lot of manual work! What's your timeline for implementing a solution? Are you looking to make changes in the next quarter?"),
                ("Visitor", "We need to improve this ASAP. What's your pricing?"),
                ("AI SDR", "Perfect timing! Based on your volume, our Professional plan at $799/month would be perfect. It includes unlimited AI lead scoring and chat automation. Would you like me to schedule a personalized demo?")
            ],
            "qualification_score": 85,
            "outcome": "Demo Scheduled"
        },
        {
            "title": "Enterprise Lead - Healthcare Company",
            "conversation": [
                ("Visitor", "We're evaluating marketing automation platforms for our healthcare company"),
                ("AI SDR", "Great! I'd love to learn more about your company and how we can help. What's your company name and what industry are you in?"),
                ("Visitor", "We're HealthTech Solutions, a 200-person healthcare technology company"),
                ("AI SDR", "Thanks for sharing! What's your biggest challenge with lead qualification right now? Are you spending too much time on manual processes?"),
                ("Visitor", "We have compliance requirements and need HIPAA-compliant solutions"),
                ("AI SDR", "Excellent point! We're SOC 2 Type II compliant with AES-256 encryption and support HIPAA requirements. What's your current lead volume and conversion rate?"),
                ("Visitor", "About 1000 leads monthly, 22% conversion rate"),
                ("AI SDR", "That's helpful context. Our Enterprise plan would be ideal for your compliance needs and volume. Would you like to see our security documentation and schedule a demo?")
            ],
            "qualification_score": 75,
            "outcome": "Security Review + Demo"
        }
    ]
    
    for i, conv in enumerate(sample_conversations):
        with st.expander(f"📋 {conv['title']} - Score: {conv['qualification_score']}/100 - {conv['outcome']}"):
            for role, message in conv['conversation']:
                if role == "Visitor":
                    st.markdown(f"""
                    <div style="background: #e3f2fd; padding: 10px; border-radius: 8px; margin: 5px 0; margin-left: 20%;">
                        <strong>👤 {role}:</strong> {message}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: #f3e5f5; padding: 10px; border-radius: 8px; margin: 5px 0; margin-right: 20%;">
                        <strong>🤖 {role}:</strong> {message}
                    </div>
                    """, unsafe_allow_html=True)

def show_analytics(platform: AIMarketingPlatform):
    """Display analytics dashboard"""
    
    st.header("📈 Predictive Analytics Dashboard")
    
    # Analytics overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Performance Metrics")
        
        metrics_data = {
            'Metric': ['Conversion Rate', 'Avg Lead Score', 'Response Time', 'Qualification Rate'],
            'Value': [23.5, 67.5, 1.2, 78.3],
            'Target': [25.0, 70.0, 2.0, 80.0],
            'Status': ['Below Target', 'Below Target', 'Above Target', 'Below Target']
        }
        
        for _, row in pd.DataFrame(metrics_data).iterrows():
            status_color = "#4caf50" if "Above" in row['Status'] else "#f44336"
            st.markdown(f"""
            <div class="metric-card">
                <strong>{row['Metric']}</strong><br>
                <span style="font-size: 1.5em; color: {status_color};">{row['Value']}</span> / {row['Target']}
                <small style="color: {status_color};">{row['Status']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Trend Analysis")
        
        # Generate trend data
        dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
        conversion_trend = [20 + i*0.5 + random.uniform(-2, 2) for i in range(len(dates))]
        
        fig = px.line(
            x=dates,
            y=conversion_trend,
            title="Conversion Rate Trend",
            labels={'x': 'Month', 'y': 'Conversion Rate (%)'}
        )
        fig.update_traces(line_color='#667eea', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    
    # Lead funnel analysis
    st.subheader("Lead Funnel Analysis")
    
    funnel_data = {
        'Stage': ['Website Visitors', 'Engaged Visitors', 'Form Submissions', 'Qualified Leads', 'Opportunities'],
        'Count': [10000, 2500, 500, 200, 50],
        'Conversion': [100, 25, 5, 2, 0.5]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.funnel(
            funnel_data,
            x='Count',
            y='Stage',
            title="Lead Funnel Volume"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            funnel_data,
            x='Stage',
            y='Conversion',
            title="Conversion Rate by Stage",
            color='Conversion',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ROI analysis
    st.subheader("ROI Analysis")
    
    roi_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Investment': [50000, 50000, 50000, 50000, 50000, 50000],
        'Revenue': [45000, 65000, 85000, 120000, 150000, 180000],
        'ROI': [-10, 30, 70, 140, 200, 260]
    }
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=roi_data['Month'],
        y=roi_data['ROI'],
        mode='lines+markers',
        name='ROI %',
        line=dict(color='#667eea', width=3)
    ))
    fig.update_layout(
        title="ROI Trend Over Time",
        xaxis_title="Month",
        yaxis_title="ROI (%)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

def show_crm_integration(platform: AIMarketingPlatform):
    """Display CRM integration demo"""
    
    st.header("🔗 CRM Integration Hub")
    
    st.markdown("""
    Seamlessly connect your AI Marketing Intelligence Platform with popular CRM systems:
    - **Real-time sync** of lead data and scores
    - **Automated lead routing** based on AI scores
    - **Unified data view** across marketing and sales
    - **Custom field mapping** for your specific needs
    """)
    
    # Integration status
    st.subheader("Integration Status")
    
    integrations = [
        {"name": "Salesforce", "status": "Connected", "leads_synced": 1250, "last_sync": "2 minutes ago"},
        {"name": "HubSpot", "status": "Connected", "leads_synced": 890, "last_sync": "1 minute ago"},
        {"name": "Pipedrive", "status": "Connected", "leads_synced": 456, "last_sync": "3 minutes ago"},
        {"name": "Microsoft Dynamics", "status": "Disconnected", "leads_synced": 0, "last_sync": "Never"}
    ]
    
    for integration in integrations:
        status_color = "#4caf50" if integration["status"] == "Connected" else "#f44336"
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{integration['name']}</strong><br>
                    <small>Status: <span style="color: {status_color};">{integration['status']}</span></small>
                </div>
                <div style="text-align: right;">
                    <strong>{integration['leads_synced']:,}</strong><br>
                    <small>Leads Synced</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Data mapping
    st.subheader("Data Field Mapping")
    
    mapping_data = {
        'AI Platform Field': ['Lead Score', 'Company Name', 'Industry', 'Job Title', 'Website Visits', 'Conversion Probability'],
        'Salesforce Field': ['Lead_Score__c', 'Company', 'Industry', 'Title', 'Website_Visits__c', 'Conversion_Prob__c'],
        'HubSpot Field': ['lead_score', 'company', 'industry', 'jobtitle', 'website_visits', 'conversion_probability'],
        'Pipedrive Field': ['Lead Score', 'Organization Name', 'Industry', 'Job Title', 'Website Visits', 'Conversion %']
    }
    
    st.dataframe(pd.DataFrame(mapping_data), use_container_width=True)
    
    # Sync activity
    st.subheader("Recent Sync Activity")
    
    sync_activity = pd.DataFrame({
        'Timestamp': pd.date_range(start='2024-12-01', periods=10, freq='H'),
        'CRM': ['Salesforce', 'HubSpot', 'Pipedrive', 'Salesforce', 'HubSpot', 'Pipedrive', 'Salesforce', 'HubSpot', 'Pipedrive', 'Salesforce'],
        'Records Synced': [45, 32, 18, 67, 23, 41, 55, 29, 37, 48],
        'Status': ['Success', 'Success', 'Success', 'Success', 'Success', 'Success', 'Success', 'Success', 'Success', 'Success']
    })
    
    fig = px.bar(
        sync_activity,
        x='Timestamp',
        y='Records Synced',
        color='CRM',
        title="Records Synced Over Time",
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Test integration
    st.subheader("Test Integration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        test_crm = st.selectbox("Select CRM to test:", ["Salesforce", "HubSpot", "Pipedrive"])
        test_records = st.slider("Number of test records:", 1, 100, 10)
    
    with col2:
        if st.button("Run Test Sync"):
            with st.spinner("Testing integration..."):
                time.sleep(2)
                st.success(f"✅ Successfully synced {test_records} records to {test_crm}")
                st.info("Integration test completed successfully!")

if __name__ == "__main__":
    main()
