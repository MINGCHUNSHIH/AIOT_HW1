# AIOT_HW1: Data Science Project

## 1. Project Description (Business Understanding)

This project is an interactive Streamlit application for visualizing and understanding linear regression. It allows users to generate synthetic data, fit a regression model, and evaluate its performance in real-time. The project was built following the CRISP-DM methodology, from initial setup to the final deployed application.

## 2. CRISP-DM Framework

This project was structured around the Cross-Industry Standard Process for Data Mining (CRISP-DM), which consists of the following phases:

1.  **Business Understanding:** Defining project objectives and requirements.
2.  **Data Understanding:** Initial data collection and exploration.
3.  **Data Preparation:** Cleaning, transforming, and feature engineering.
4.  **Modeling:** Selecting and applying modeling techniques.
5.  **Evaluation:** Evaluating model performance against business objectives.
6.  **Deployment:** Integrating the model into a production environment (e.g., via this Streamlit app).

## 3. Installation and Setup

To set up the development environment, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MINGCHUNSHIH/AIOT_HW1.git
    cd AIOT_HW1
    ```

2.  **Create a Python virtual environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\.venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## 4. Usage

Once the setup is complete, you can run the Streamlit application with the following command:

```bash
streamlit run app.py
```

## 5. Project Structure

The main files and directories are organized as follows:

```
.
├── .venv/                  # Python virtual environment
├── app.py                  # Main Streamlit application file
├── requirements.txt        # Project dependencies
├── README.md               # This file
├── prompt.md               # Development log for user prompts
└── devLog.md               # Development log for assistant actions
```
