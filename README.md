Customer Support Ticket Auto-Triage
An advanced machine learning project focused on revolutionizing customer support through intelligent ticket classification and automated routing systems.

🎯 Project Objective
Core Mission
To enhance operational efficiency and improve customer satisfaction by automating the initial processing of support tickets, reducing manual effort, and accelerating resolution times.

Primary Goal
Develop and deploy a robust machine learning model capable of accurately classifying customer support tickets into predefined categories and routing them to the most appropriate team or agent.

📋 Key Ticket Categories
Bug Report: Reporting software defects or errors for immediate action.
Feature Request: Gathering user suggestions for new functionalities and enhancements.
Technical Issue: Addressing problems requiring specialized technical assistance and troubleshooting.
Billing Inquiry: Handling questions and discrepancies related to invoices, payments, and subscriptions.
Account Management: Resolving issues regarding user accounts, profiles, and access controls.
🗃️ Dataset Structure
The system uses a synthetic dataset that mirrors real-world support tickets with the following schema:
<img width="944" height="536" alt="image" src="https://github.com/user-attachments/assets/1de6d537-813c-4b6c-992d-75af6d3b34c8" />


🛠️ How to Run This Project (Step-by-Step)
Prerequisites
Python 3.8 or higher
pip package manager
Step 1: Install Dependencies:
pip install -r requirements.txt
Step 2: Generate Synthetic Dataset:
python generate_dataset.py
Step 3: Train the ML Model:
python src/train.py
Launch the Web Application:
python src/app.py

Step 5: Use the System
Enter a Subject and Description in the web form.
Click "Classify Ticket".
View the predicted category, confidence score, and latency.

.
📊 Evaluation Framework
<img width="961" height="371" alt="image" src="https://github.com/user-attachments/assets/e7f40efd-a68b-4e07-85a8-e85617dbdf83" />


🧰 Technical Requirements
Python: 3.8+
Key Libraries: scikit-learn, pandas, numpy, nltk, flask, joblib
Version Control: Git (mandatory)
