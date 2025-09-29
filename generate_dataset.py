import pandas as pd
import random
from datetime import datetime, timedelta

templates = {
    "Bug Report": [
        "App crashes when I click on {button}.",
        "The {feature} is not working after the latest update.",
        "Error message '{error}' appears when I try to {action}.",
        "The screen goes blank when I open {section}.",
        "Login fails even with correct credentials."
    ],
    "Feature Request": [
        "Can you add {feature} to the dashboard?",
        "It would be great if we could {action}.",
        "Please consider adding dark mode support.",
        "I suggest improving the {workflow} for better usability.",
        "Add export to PDF functionality."
    ],
    "Technical Issue": [
        "I can't connect to the {service} despite correct settings.",
        "API returns 500 error when calling {endpoint}.",
        "Integration with {tool} is failing.",
        "Server response time is too slow for {operation}.",
        "SSL certificate error on your domain."
    ],
    "Billing Inquiry": [
        "I was charged twice for my subscription.",
        "My invoice doesn't match the plan I selected.",
        "How do I upgrade my billing plan?",
        "Refund request for unused service period.",
        "Billing cycle date seems incorrect."
    ],
    "Account Management": [
        "I can't reset my password.",
        "My account is locked without reason.",
        "How do I delete my account permanently?",
        "Email not updating in profile settings.",
        "Two-factor authentication not working."
    ]
}

subjects = {
    "Bug Report": ["App Crash", "Login Error", "Feature Broken"],
    "Feature Request": ["New Feature Suggestion", "UX Improvement"],
    "Technical Issue": ["Connection Failed", "API Error", "Slow Performance"],
    "Billing Inquiry": ["Double Charge", "Invoice Question", "Refund Request"],
    "Account Management": ["Password Reset", "Account Locked", "2FA Issue"]
}

categories = list(templates.keys())
priorities = ["Low", "Medium", "High", "Critical"]

data = []
start_time = datetime.now() - timedelta(days=180)

for i in range(2000):
    category = random.choice(categories)
    template = random.choice(templates[category])
    
    # ✅ Provide ALL possible placeholders used anywhere in templates
    desc = template.format(
        button=random.choice(["Save", "Submit", "Delete", "Refresh"]),
        feature=random.choice(["search", "notifications", "dark mode", "export"]),
        error=random.choice(["404", "500", "Timeout", "Connection lost"]),
        action=random.choice(["log in", "upload file", "sync data", "reset password"]),
        section=random.choice(["dashboard", "settings", "profile", "billing"]),
        service=random.choice(["database", "email server", "cloud storage", "API gateway"]),
        endpoint=random.choice(["/api/users", "/api/payments", "/api/logs"]),
        tool=random.choice(["Slack", "Zapier", "Google Workspace", "Salesforce"]),
        workflow=random.choice(["onboarding", "checkout", "user management", "reporting"]),
        operation=random.choice(["login", "file upload", "search query", "data export"])  # ← ADDED!
        # Note: Templates like "Add export to PDF..." don't use all fields — that's OK!
    )
    
    ticket = {
        "Ticket_ID": i + 1,
        "Subject": random.choice(subjects[category]),
        "Description": desc,
        "Category": category,
        "Priority": random.choices(priorities, weights=[1, 3, 4, 2])[0],
        "Timestamp": start_time + timedelta(minutes=random.randint(0, 259200))
    }
    data.append(ticket)

# Ensure data folder exists
import os
os.makedirs("data", exist_ok=True)

pd.DataFrame(data).to_csv("data/tickets.csv", index=False)
print("✅ Dataset saved: data/tickets.csv (2000 tickets)")