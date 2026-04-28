# 🧪 A/B Testing Engine & Experimentation Platform

An enterprise-grade statistical engine and interactive dashboard for designing, running, and analyzing A/B tests. This project demonstrates deep statistical maturity, focusing on rigorous experimental design and hypothesis testing—core requirements for Data Analysts at top-tier tech companies.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.33.0-FF4B4B)
![SciPy](https://img.shields.io/badge/SciPy-1.13.0-8CAAE6)
![Statsmodels](https://img.shields.io/badge/Statsmodels-0.14.1-3b82f6)

**[🌐 View the Live Interactive Dashboard Here](https://ab-testing-engine-8s2qzmappwxy5yxhxe426je.streamlit.app)** 

<img width="1915" height="951" alt="dashboard_image" src="https://github.com/user-attachments/assets/8c67ca69-772c-4ca5-9fd8-9edebc9ea816" />


## 📌 The Problem
"Peeking" at A/B test results too early or running tests without a calculated sample size are the most common statistical errors made by product teams, leading to false positives and bad product decisions.

## 🚀 Features & Statistical Modules

1. **Pre-Experiment: Sample Size Calculator**
   - Calculates the exact number of users required per variation to achieve statistical significance.
   - **Inputs:** Baseline Conversion Rate, Minimum Detectable Effect (MDE), Statistical Power (1-β), and Significance Level (α).
   - Prevents the "peeking" problem by defining a strict test duration before the experiment begins.

2. **Real-Time Data Simulator**
   - Instantly generates highly realistic binomial conversion data for a simulated A/B test, allowing recruiters and users to test the engine without uploading CSVs.

3. **Post-Experiment: Results Engine**
   - Performs a rigorous **Two-Proportion Z-Test**.
   - Calculates **P-Values** to test the null hypothesis.
   - Generates **95% Confidence Intervals** to show the true range of the uplift.
   - Provides a clear, human-readable insight ("We are 95% confident that Variant B increases conversion by X%").

4. **Interactive Visualizations**
   - **Distribution of Sample Means:** A beautiful Plotly visualization showing the overlap (or separation) of the Null and Alternative Hypothesis bell curves.
   - **Confidence Intervals:** Bar charts with error bars representing the 95% CI.

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <[your-github-repo-link](https://github.com/rishabhsuri667-code/ab-testing-engine.git)>
   cd ab_testing_engine
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Dashboard:**
   ```bash
   streamlit run app.py
   ```
