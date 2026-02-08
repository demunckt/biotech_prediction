# 🧬 AI-Driven Drug Discovery Pipeline

## Overview
This project demonstrates an end-to-end machine learning pipeline for drug target prediction. It integrates on-premises screening, cloud-based feature engineering, and Agentic AI to automate the identification of potential biotech targets.

## 🏗 Architecture
The system operates on a hybrid cloud architecture:
1.  **Ingestion:** Raw molecular data is processed locally.
2.  **Engineering (Databricks):** Distributed PySpark clusters handle feature extraction (RDKit) and Silver/Gold Delta tables.
3.  **Training (AWS SageMaker):** Hyperparameter tuning jobs identify the optimal binding affinity model.
4.  **Inference (AWS Lambda & Bedrock):** An Event-driven architecture triggers predictions, and a Generative AI Agent allows natural language queries of the results.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Orchestration:** AWS Lambda, Amazon EventBridge
* **Machine Learning:** XGBoost, Graph Neural Networks (GNN), AWS SageMaker
* **Data Engineering:** Databricks (PySpark), Delta Lake, AWS S3
* **GenAI:** Amazon Bedrock (Claude 3.5 Sonnet), Agents for Bedrock

## 📂 Project Structure
```text
├── data/                  # Local datasets (gitignored)
├── notebooks/             # Jupyter/Databricks notebooks for EDA
├── src/
│   ├── ingestion/         # Scripts for S3 uploads
│   ├── training/          # SageMaker training scripts
│   └── lambda/            # AWS Lambda function logic
├── infrastructure/        # IaC or setup scripts
└── results/               # Prediction outputs
