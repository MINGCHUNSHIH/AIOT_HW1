import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# --- App Configuration ---
st.set_page_config(
    page_title="Interactive Linear Regression",
    layout="wide"
)

st.title("Interactive Linear Regression")

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.title("Model Configuration")

    st.header("Data Generation")
    n_points = st.slider("Number of data points (n)", 5, 500, 100)
    x_range = st.slider("X-axis range", -10.0, 10.0, (-5.0, 5.0))
    true_a = st.slider("True slope (a)", -5.0, 5.0, 2.0, 0.1)
    use_intercept = st.checkbox("Add intercept (b)", value=True)
    true_b = st.slider("True intercept (b)", -10.0, 10.0, 3.0, 0.5) if use_intercept else 0
    noise_var = st.slider("Noise Variance (σ²)", 0.0, 10.0, 1.0, 0.1)
    random_seed = st.number_input("Random Seed", value=42)

    st.header("Model Evaluation")
    show_ci = st.checkbox("Show 95% Confidence Interval", value=True)
    if show_ci:
        bootstrap_iterations = st.slider("Bootstrap Iterations", 100, 5000, 1000, 100)

# --- Main Application Logic ---

# 1. Generate Data
np.random.seed(random_seed)
X = np.linspace(x_range[0], x_range[1], n_points)
noise = np.random.normal(0, np.sqrt(noise_var), n_points)
y = true_a * X + true_b + noise

# 2. Fit the Model
model_coeffs = np.polyfit(X, y, 1)
model_a, model_b = model_coeffs[0], model_coeffs[1]
y_pred = model_a * X + model_b

# 3. Bootstrap Confidence Interval
@st.cache_data
def bootstrap_regression(X_data, y_data, iterations, X_line):
    bootstrap_preds = np.zeros((iterations, len(X_line)))
    n_data_points = len(X_data)
    for i in range(iterations):
        indices = np.random.choice(range(n_data_points), size=n_data_points, replace=True)
        X_sample, y_sample = X_data[indices], y_data[indices]
        
        coeffs = np.polyfit(X_sample, y_sample, 1)
        bootstrap_preds[i, :] = coeffs[0] * X_line + coeffs[1]
        
    lower_bound = np.percentile(bootstrap_preds, 2.5, axis=0)
    upper_bound = np.percentile(bootstrap_preds, 97.5, axis=0)
    return lower_bound, upper_bound

# 4. Plotting
st.header("Regression Model and Data")
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(X, y, alpha=0.6, label="Generated Data")
ax.plot(X, y_pred, color='red', linewidth=2, label=f"Regression Line (y = {model_a:.2f}x + {model_b:.2f})")

if show_ci:
    with st.spinner(f"Running {bootstrap_iterations} bootstrap iterations..."):
        lower_ci, upper_ci = bootstrap_regression(X, y, bootstrap_iterations, X)
    ax.fill_between(X, lower_ci, upper_ci, color='red', alpha=0.2, label="95% Confidence Interval")

# --- Outlier Identification ---
residuals = y - y_pred
outlier_indices = np.argsort(np.abs(residuals))[-5:]

ax.scatter(X[outlier_indices], y[outlier_indices], color='orange', s=100, edgecolors='k', label="Top 5 Outliers")
for i in outlier_indices:
    ax.text(X[i], y[i], f'  ({X[i]:.1f}, {y[i]:.1f})', fontsize=9)

ax.set_title("Interactive Linear Regression")
ax.set_xlabel("X")
ax.set_ylabel("y")
ax.legend()
ax.grid(True)
st.pyplot(fig)


# 5. Evaluation Metrics
st.header("Model Evaluation")
r2 = r2_score(y, y_pred)

st.subheader("Model Coefficients")
col1, col2 = st.columns(2)
col1.metric("Fitted Slope (a)", f"{model_a:.4f}", delta=f"{model_a - true_a:.4f} from true value")
col2.metric("Fitted Intercept (b)", f"{model_b:.4f}", delta=f"{model_b - true_b:.4f} from true value")

st.subheader("Goodness of Fit")
st.metric("R-squared (R²)", f"{r2:.4f}")

st.subheader("Outlier Analysis")
outlier_indices_desc = np.argsort(np.abs(residuals))[-5:][::-1] # Top 5, descending order
outlier_df = pd.DataFrame({
    "X": X[outlier_indices_desc],
    "y_actual": y[outlier_indices_desc],
    "y_predicted": y_pred[outlier_indices_desc],
    "Residual": residuals[outlier_indices_desc]
})
st.write("Top 5 data points with the largest absolute residuals:")
st.dataframe(outlier_df)
