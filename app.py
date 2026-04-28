import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.stats.api as sms
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
import plotly.graph_objects as go
import plotly.express as px
import math

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="A/B Testing Engine",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED CUSTOM CSS (SLICK DARK THEME) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #e0e6ed;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .winner-text {
        color: #10b981; /* emerald green */
        font-weight: 700;
        font-size: 1.5rem;
    }
    .loser-text {
        color: #ef4444; /* red */
        font-weight: 700;
        font-size: 1.5rem;
    }
    .neutral-text {
        color: #f59e0b; /* amber */
        font-weight: 700;
        font-size: 1.5rem;
    }
    header {visibility: hidden;}
    .css-1544g2n.e1fqcg0o4 {padding-top: 1rem;}
    hr { border-color: rgba(255,255,255,0.1); margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

def calculate_sample_size(bcr, mde, alpha=0.05, power=0.80):
    """Calculates the required sample size per variation for a proportion test."""
    effect_size = sms.proportion_effectsize(bcr, bcr + (bcr * mde))
    sample_size = sms.NormalIndPower().solve_power(
        effect_size, 
        power=power, 
        alpha=alpha, 
        ratio=1
    )
    return math.ceil(sample_size)

def main():
    st.markdown("<h1 style='font-size: 2.5rem; font-weight: 700; margin-bottom: 0;'>🧪 A/B Testing Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>Experimentation platform for rigorous statistical analysis.</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 Pre-Experiment: Sample Size Calculator", "🔬 Post-Experiment: Results Analysis"])
    
    # ==========================================
    # TAB 1: SAMPLE SIZE CALCULATOR
    # ==========================================
    with tab1:
        st.markdown("### Pre-Experiment Planning")
        st.info("Before running an A/B test, you must calculate the required sample size to ensure statistical power and avoid the 'peeking' problem.")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            bcr = st.number_input("Baseline Conversion Rate (%)", min_value=0.1, max_value=99.0, value=5.0, step=0.1) / 100
            mde = st.number_input("Minimum Detectable Effect - Relative (%)", min_value=0.1, max_value=100.0, value=10.0, step=0.1, help="The smallest relative uplift you care about detecting.") / 100
            
            c1, c2 = st.columns(2)
            with c1:
                alpha = st.selectbox("Significance Level (α)", [0.01, 0.05, 0.10], index=1, help="False positive rate (Type I error). 0.05 = 95% Confidence.")
            with c2:
                power = st.selectbox("Statistical Power (1-β)", [0.80, 0.90, 0.95], index=0, help="Probability of detecting an effect if there is one (Type II error).")
            
            daily_traffic = st.number_input("Estimated Daily Traffic (Total)", min_value=100, value=5000, step=100)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            req_sample_size = calculate_sample_size(bcr, mde, alpha, power)
            total_req_sample = req_sample_size * 2
            days_required = math.ceil(total_req_sample / daily_traffic)
            
            st.markdown(f'''
            <div class="glass-card" style="border-top: 4px solid #3b82f6;">
                <div class="metric-label">Required Sample Size (Per Variation)</div>
                <div class="metric-value" style="color: #60a5fa;">{req_sample_size:,} users</div>
                <hr style="margin: 10px 0;">
                <div class="metric-label">Total Traffic Required</div>
                <div class="metric-value">{total_req_sample:,} users</div>
                <hr style="margin: 10px 0;">
                <div class="metric-label">Estimated Test Duration</div>
                <div class="metric-value" style="color: #f59e0b;">{days_required} days</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Simple Plotly visualization
            target_cr = bcr * (1 + mde)
            fig = go.Figure(data=[
                go.Bar(name='Control (Baseline)', x=['Control'], y=[bcr], marker_color='#3b82f6'),
                go.Bar(name='Variant (Target)', x=['Variant'], y=[target_cr], marker_color='#10b981')
            ])
            fig.update_layout(
                title='Target Conversion Rates',
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e6ed'), yaxis_tickformat='.2%',
                margin=dict(t=40, b=0, l=0, r=0), height=300
            )
            st.plotly_chart(fig, use_container_width=True)

    # ==========================================
    # TAB 2: POST-EXPERIMENT RESULTS
    # ==========================================
    with tab2:
        st.markdown("### Results Analysis & Simulation")
        st.info("Use the simulator below to generate realistic A/B test data, then view the statistical engine's analysis.")
        
        col_sim, col_res = st.columns([1, 2.5])
        
        with col_sim:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("**🎲 Data Simulator**")
            sim_visitors = st.number_input("Total Visitors in Test", min_value=1000, max_value=1000000, value=50000, step=1000)
            sim_baseline_cr = st.number_input("Simulate Control CR (%)", min_value=0.1, max_value=99.0, value=5.0, step=0.1) / 100
            sim_true_uplift = st.slider("Simulate True Relative Uplift (%)", min_value=-20.0, max_value=20.0, value=5.0, step=0.5) / 100
            
            if st.button("Generate Experiment Data", use_container_width=True, type="primary"):
                # Simulate binomial data
                np.random.seed()
                n_A = sim_visitors // 2
                n_B = sim_visitors - n_A
                
                true_p_A = sim_baseline_cr
                true_p_B = sim_baseline_cr * (1 + sim_true_uplift)
                
                # Use binomial distribution to generate realistic conversions
                conv_A = np.random.binomial(n=n_A, p=true_p_A)
                conv_B = np.random.binomial(n=n_B, p=true_p_B)
                
                st.session_state['exp_data'] = {
                    'visitors_A': n_A, 'conversions_A': conv_A,
                    'visitors_B': n_B, 'conversions_B': conv_B
                }
            st.markdown("</div>", unsafe_allow_html=True)

        with col_res:
            if 'exp_data' in st.session_state:
                data = st.session_state['exp_data']
                nA, cA = data['visitors_A'], data['conversions_A']
                nB, cB = data['visitors_B'], data['conversions_B']
                
                cr_A = cA / nA
                cr_B = cB / nB
                rel_uplift = (cr_B - cr_A) / cr_A
                
                # Statistical Testing (Z-Test for proportions)
                count = np.array([cB, cA])
                nobs = np.array([nB, nA])
                z_stat, p_val = proportions_ztest(count, nobs, alternative='two-sided')
                
                # Confidence Intervals
                ci_B, ci_A = proportion_confint(count, nobs, alpha=0.05, method='normal')
                
                # Determine Winner
                alpha_threshold = 0.05
                if p_val < alpha_threshold and rel_uplift > 0:
                    winner_msg = "<span class='winner-text'>✅ Variant B is the Winner!</span>"
                    insight = f"The result is statistically significant. We are 95% confident that Variant B increases conversion by approximately **{rel_uplift*100:.2f}%**."
                elif p_val < alpha_threshold and rel_uplift < 0:
                    winner_msg = "<span class='loser-text'>❌ Variant B Underperformed!</span>"
                    insight = f"The result is statistically significant, but Variant B decreased conversion by **{abs(rel_uplift)*100:.2f}%**. Stick to the Control."
                else:
                    winner_msg = "<span class='neutral-text'>⚖️ No Significant Difference</span>"
                    insight = f"We cannot reject the null hypothesis (p-value: {p_val:.4f}). Any observed difference is likely due to random chance. Keep running the test or stick to the Control."
                
                # Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Control CR", f"{cr_A*100:.2f}%", f"{cA}/{nA} conversions", delta_color="off")
                m2.metric("Variant CR", f"{cr_B*100:.2f}%", f"{cB}/{nB} conversions", delta_color="off")
                m3.metric("Observed Uplift", f"{rel_uplift*100:+.2f}%")
                m4.metric("P-Value", f"{p_val:.4f}", "Stat. Significant" if p_val < alpha_threshold else "Not Significant", delta_color="inverse" if p_val >= alpha_threshold else "normal")
                
                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                st.markdown(f"### {winner_msg}", unsafe_allow_html=True)
                st.write(insight)
                
                # Visualizations
                st.markdown("<br>", unsafe_allow_html=True)
                c_fig1, c_fig2 = st.columns(2)
                
                with c_fig1:
                    # Bar chart with error bars
                    fig_bar = go.Figure()
                    fig_bar.add_trace(go.Bar(
                        name='Control', x=['Control'], y=[cr_A],
                        error_y=dict(type='data', array=[ci_A[1]-cr_A], arrayminus=[cr_A-ci_A[0]]),
                        marker_color='#3b82f6'
                    ))
                    fig_bar.add_trace(go.Bar(
                        name='Variant B', x=['Variant B'], y=[cr_B],
                        error_y=dict(type='data', array=[ci_B[1]-cr_B], arrayminus=[cr_B-ci_B[0]]),
                        marker_color='#10b981' if rel_uplift > 0 else '#ef4444'
                    ))
                    fig_bar.update_layout(
                        title='Conversion Rates with 95% CI',
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e0e6ed'), yaxis_tickformat='.2%', height=350,
                        showlegend=False
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                with c_fig2:
                    # Bell Curve overlap
                    x_A = np.linspace(cr_A - 4*np.sqrt(cr_A*(1-cr_A)/nA), cr_A + 4*np.sqrt(cr_A*(1-cr_A)/nA), 100)
                    y_A = stats.norm.pdf(x_A, cr_A, np.sqrt(cr_A*(1-cr_A)/nA))
                    
                    x_B = np.linspace(cr_B - 4*np.sqrt(cr_B*(1-cr_B)/nB), cr_B + 4*np.sqrt(cr_B*(1-cr_B)/nB), 100)
                    y_B = stats.norm.pdf(x_B, cr_B, np.sqrt(cr_B*(1-cr_B)/nB))
                    
                    fig_dist = go.Figure()
                    fig_dist.add_trace(go.Scatter(x=x_A, y=y_A, fill='tozeroy', name='Control', line=dict(color='#3b82f6'), fillcolor='rgba(59, 130, 246, 0.3)'))
                    fig_dist.add_trace(go.Scatter(x=x_B, y=y_B, fill='tozeroy', name='Variant B', line=dict(color='#10b981' if rel_uplift>0 else '#ef4444'), fillcolor='rgba(16, 185, 129, 0.3)' if rel_uplift>0 else 'rgba(239, 68, 68, 0.3)'))
                    
                    fig_dist.update_layout(
                        title='Distribution of Sample Means',
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e0e6ed'), xaxis_tickformat='.2%', height=350,
                        hovermode="x unified"
                    )
                    st.plotly_chart(fig_dist, use_container_width=True)
            else:
                st.markdown("<div style='text-align: center; color: #94a3b8; padding: 50px;'>👈 Click <b>Generate Experiment Data</b> to see the results engine in action.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
