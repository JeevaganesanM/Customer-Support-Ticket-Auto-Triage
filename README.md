# Customer Support Ticket Auto-Triage

An advanced machine learning project focused on revolutionizing customer support through intelligent ticket classification and automated routing systems.

## 🎯 Project Objective

### Core Mission
To enhance operational efficiency and improve customer satisfaction by automating the initial processing of support tickets, reducing manual effort, and accelerating resolution times.

### Primary Goal
Develop and deploy a robust machine learning model capable of accurately classifying customer support tickets into predefined categories and routing them to the most appropriate team or agent.

## 📋 Key Ticket Categories

- **Bug Report**: Reporting software defects or errors for immediate action.  
- **Feature Request**: Gathering user suggestions for new functionalities and enhancements.  
- **Technical Issue**: Addressing problems requiring specialized technical assistance and troubleshooting.  
- **Billing Inquiry**: Handling questions and discrepancies related to invoices, payments, and subscriptions.  
- **Account Management**: Resolving issues regarding user accounts, profiles, and access controls.

## 🗃️ Dataset Structure

The system uses a synthetic dataset that mirrors real-world support tickets with the following schema:

| Field        | Description                              | Type             |
|--------------|------------------------------------------|------------------|
| `Ticket_ID`  | Unique identifier for each ticket        | Integer          |
| `Subject`    | Short summary of the issue               | String (Text)    |
| `Description`| Detailed explanation of the problem      | String (Long Text)|
| `Category`   | Pre-assigned issue type (target variable)| Categorical String|
| `Priority`   | Urgency level of the ticket              | Categorical String|
| `Timestamp`  | Date and time of ticket creation         | Datetime         |

## Technical Requirements
- **Python**: 3.8+
- **Key Libraries**: `scikit-learn`, `pandas`, `numpy`, `NLTK`/`SpaCy`, `TensorFlow`/`PyTorch`
- **Version Control**: Git (mandatory for collaboration)

## Project Deliverables
- **Trained ML Model**: A fully trained and optimized classification model, ready for production.
- **API Endpoint**: A robust RESTful API for real-time ticket classification and integration.
- **Technical Documentation**: Comprehensive report on methodology, results, and usage guidelines.

## Evaluation Framework
Model performance will be rigorously assessed using the following metrics and their respective weightages:

| Metric (Weight)      | Description |
|----------------------|-------------|
| **Accuracy (40%)**   | Overall correct predictions across all categories, reflecting general model effectiveness. |
| **Precision & Recall (30%)** | Critical for identifying positive cases and minimizing false positives/negatives for each specific ticket category. |
| **F1-Score (20%)**   | The harmonic mean of precision and recall, providing a balanced measure of the model's accuracy. |
| **Latency (10%)**    | Measures the time taken for real-time classification, ensuring quick response times in operational environments. |

## 🛠️ How to Run This Project (Step-by-Step)

### Example Output Image
(Output.png)

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt

### Step 2: Generate Synthetic Dataset
```bash
python generate_dataset.py

### Step 3: Train the ML Model
```bash
python src/train.py

### Step 4: Launch the Web Application
```bash
python src/app.py
