Project learning purpose: upskilling on AWS SageMaker, BedRock & Lambda.
Data Source: Kaggle: https://www.kaggle.com/datasets/shahriarkabir/drug-discovery-virtual-screening-dataset

🧬 End-to-End Biotech Drug Discovery Pipeline with Agentic AI
(Note: Upload the image generated above to your repo and name it architecture_diagram.png)

🚀 Project Overview
This project implements a scalable, event-driven AI pipeline for early-stage drug discovery. It automates the screening of small molecules for potential therapeutic use by predicting their Binding Affinity (Regression) and Biological Activity (Classification).

Moving beyond traditional static scripts, this architecture leverages AWS Serverless and Generative AI technologies. It allows scientists to simply upload a CSV file of molecular data and receive instant predictions, or query an AI Agent (Claude 3.7) in natural language to identify high-priority drug candidates.

🔑 Key Features
Automated MLOps Pipeline: Seamless transition from local data preparation to cloud-based model tuning.

Dual-Model Architecture: Simultaneously runs classification (Random Forest) and regression (Random Forest/Linear) models to score molecules.

Serverless Inference: Uses AWS Lambda to orchestrate real-time predictions without managing persistent servers.

Agentic AI Interface: Features an Amazon Bedrock Agent that can "use tools" to read S3 results and summarize scientific findings for users.

Scalable Infrastructure: Built on AWS SageMaker and S3 to handle datasets from MBs to GBs.

📂 Repository Structure
1. Local Development & Data Prep
00_split_test_set.py: Initial utilities for splitting raw chemical datasets into training and validation sets to ensure robust model evaluation.

01_placeholder_initial_data_vis.py: Scripts for Exploratory Data Analysis (EDA) to understand molecular property distributions.

02_jupyter_nb_model_selection_v2.ipynb: The research sandbox. This notebook compares multiple algorithms (Linear Regression, XGBoost, Random Forest) to identify the best performers for this specific biological dataset.

04_transformation_bronzetogold_copy.py: An ETL script that simulates a "Bronze to Gold" data lake transformation, cleaning raw data and engineering features for the model.

2. Cloud Orchestration (MLOps)
03_upload_to_s3_copy.py: Handles the secure transfer of processed datasets to the AWS S3 Data Lake.

07_sagemaker_notebook.ipynb: The Master Orchestrator. This notebook runs on AWS SageMaker to:

Launch parallel Hyperparameter Tuning Jobs on the cloud.

Deploy the best-performing models to real-time HTTPS endpoints.

Manage model artifacts and versioning.

3. Serverless Automation & AI Agent
05_lambda_drug_screener.py: The "Worker" function.

Trigger: S3 Upload (Event Notification).

Action: Pre-processes data, invokes both SageMaker endpoints, merges results, and saves a scored CSV back to S3.

06_lambda_resultsreader_agent_tool.py: The "Agent Tool."

Role: Connects the Amazon Bedrock Agent to the S3 bucket.

Logic: Reads the latest screening results, filters for high-affinity candidates, and formats the data into a JSON response that the LLM can interpret and narrate.

🛠️ Technology Stack
Cloud Provider: AWS (eu-north-1)

Machine Learning: Amazon SageMaker, Scikit-learn (Random Forest, Ridge Regression)

Serverless: AWS Lambda, Amazon EventBridge

Generative AI: Amazon Bedrock (Anthropic Claude 3.7 Sonnet)

Storage: Amazon S3

Language: Python 3.12

⚙️ How It Works
Phase 1: Training (The "Brain")
Data is cleaned and uploaded to S3 (04_..., 03_...).

The SageMaker Notebook (07_...) spins up a cluster of instances.

It runs a Hyperparameter Tuning Job to find the optimal settings for both Affinity and Activity models.

The winning models are deployed to persistent endpoints.

Phase 2: Automated Screening (The "Muscle")
A user uploads a file (e.g., new_molecules.csv) to the incoming/ S3 folder.

S3 Event Notifications trigger the 05_lambda_drug_screener.

The Lambda function sends the data to both SageMaker endpoints.

Predictions are aggregated and a "priority candidate" flag is calculated.

The final results are saved to results/scored_molecules.csv.

Phase 3: The AI Assistant (The "Voice")
A user asks the chatbot: "Did we find any hits in the last run?"

The Bedrock Agent interprets the intent and calls the 06_lambda_resultsreader tool.

The Lambda fetches the latest CSV from S3, identifies top compounds, and returns the data.

Claude 3.7 summarizes the findings: "Yes, we identified 3 high-priority candidates. The top hit is Molecule CID_123 with a binding affinity of 9.8."

🔮 Future Improvements
Knowledge Base Integration: Connect the Bedrock Agent to a vector database of research papers (RAG) to cross-reference hits with existing literature.

Molecular Visualization: Update the Lambda to generate 2D structure images (SMILES) for top candidates.

Containerization: Dockerize the Lambda functions for easier deployment across different environments
