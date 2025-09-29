from flask import Flask, request, jsonify, render_template_string
import joblib
import time
from preprocess import clean_text

app = Flask(__name__)

# Load model once at startup
try:
    vectorizer, model = joblib.load("models/best_model.pkl")
except FileNotFoundError:
    raise RuntimeError("❌ Model not found! Run 'python src/train.py' first.")

# Modern HTML/CSS/JS UI
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Support Ticket Auto-Triage</title>
  <style>
    :root {
      --primary: #4CAF50;
      --secondary: #2196F3;
      --danger: #f44336;
      --warning: #ff9800;
      --info: #00bcd4;
      --success: #4caf50;
      --dark: #333;
      --light: #f9f9f9;
      --gray: #ddd;
      --white: #fff;
      --shadow: 0 2px 10px rgba(0,0,0,0.1);
      --transition: all 0.3s ease;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
      padding: 20px;
      color: var(--dark);
    }

    .container {
      max-width: 800px;
      margin: 0 auto;
      padding: 30px;
      background: var(--white);
      border-radius: 12px;
      box-shadow: var(--shadow);
      animation: fadeIn 0.5s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    h1 {
      text-align: center;
      color: var(--dark);
      margin-bottom: 20px;
      font-weight: 600;
      letter-spacing: 1px;
    }

    .form-group {
      margin-bottom: 20px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 600;
      color: var(--dark);
    }

    input, textarea {
      width: 100%;
      padding: 12px;
      border: 1px solid var(--gray);
      border-radius: 8px;
      font-size: 16px;
      transition: var(--transition);
      background: var(--light);
    }

    input:focus, textarea:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);
    }

    button {
      background: var(--primary);
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 16px;
      font-weight: 600;
      transition: var(--transition);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      max-width: 200px;
      margin: 20px auto;
    }

    button:hover {
      background: #45a049;
      transform: translateY(-2px);
    }

    button:active {
      transform: translateY(0);
    }

    .loading {
      display: none;
      text-align: center;
      padding: 20px;
      color: var(--dark);
    }

    .loading::after {
      content: " ";
      display: inline-block;
      width: 20px;
      height: 20px;
      border: 3px solid var(--primary);
      border-radius: 50%;
      border-top-color: transparent;
      animation: spin 1s linear infinite;
      margin-left: 10px;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .result-card {
      display: none;
      background: var(--white);
      border: 1px solid var(--gray);
      border-radius: 12px;
      padding: 20px;
      margin-top: 20px;
      box-shadow: var(--shadow);
      animation: slideIn 0.5s ease;
    }

    @keyframes slideIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .category-badge {
      display: inline-block;
      padding: 6px 12px;
      border-radius: 20px;
      font-weight: bold;
      color: white;
      margin-right: 10px;
      font-size: 14px;
    }

    .bug-report { background: var(--danger); }
    .feature-request { background: var(--info); }
    .technical-issue { background: var(--secondary); }
    .billing-inquiry { background: var(--warning); }
    .account-management { background: var(--success); }

    .confidence-meter {
      width: 100%;
      height: 8px;
      background: var(--gray);
      border-radius: 4px;
      margin: 10px 0;
      overflow: hidden;
    }

    .confidence-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--success), var(--warning), var(--danger));
      transition: width 0.5s ease;
    }

    .metric {
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid var(--gray);
      font-size: 14px;
    }

    .metric:last-child {
      border-bottom: none;
    }

    .copy-btn {
      background: var(--light);
      border: 1px solid var(--gray);
      border-radius: 6px;
      padding: 6px 12px;
      cursor: pointer;
      font-size: 12px;
      margin-top: 10px;
      transition: var(--transition);
    }

    .copy-btn:hover {
      background: var(--gray);
    }

    .footer {
      text-align: center;
      margin-top: 30px;
      font-size: 12px;
      color: var(--dark);
      opacity: 0.7;
    }

    @media (max-width: 600px) {
      .container {
        padding: 15px;
        margin: 10px;
      }

      h1 {
        font-size: 24px;
      }

      button {
        max-width: 100%;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🚀 Customer Support Ticket Auto-Triage</h1>
    
    <form id="ticketForm">
      <div class="form-group">
        <label for="subject">Subject:</label>
        <input type="text" id="subject" required placeholder="e.g., Login fails with error 500" />
      </div>

      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" rows="5" required placeholder="Describe your issue in detail..."></textarea>
      </div>

      <button type="submit" id="classifyBtn">
        <span>Classify Ticket</span>
      </button>
    </form>

    <div class="loading" id="loading">Analyzing ticket...</div>

    <div class="result-card" id="resultCard">
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
        <span id="categoryBadge" class="category-badge">Bug Report</span>
        <span id="categoryText">Predicted Category</span>
      </div>

      <div class="confidence-meter">
        <div id="confidenceFill" class="confidence-fill" style="width: 69%;"></div>
      </div>

      <div class="metric">
        <span>✅ Confidence:</span>
        <span id="confidenceValue">69.16%</span>
      </div>

      <div class="metric">
        <span>⏱️ Latency:</span>
        <span id="latencyValue">0.0092 seconds</span>
      </div>

      <button class="copy-btn" id="copyBtn">📋 Copy Prediction</button>
    </div>

    <div class="footer">
      Powered by Machine Learning • Built for Speed & Accuracy
    </div>
  </div>

  <script>
    document.getElementById('ticketForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const subject = document.getElementById('subject').value;
      const description = document.getElementById('description').value;
      const classifyBtn = document.getElementById('classifyBtn');
      const loadingDiv = document.getElementById('loading');
      const resultCard = document.getElementById('resultCard');
      const copyBtn = document.getElementById('copyBtn');

      // Show loading
      classifyBtn.disabled = true;
      classifyBtn.innerHTML = '<span>Processing...</span>';
      loadingDiv.style.display = 'block';
      resultCard.style.display = 'none';

      try {
        const response = await fetch('/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ Subject: subject, Description: description })
        });

        const data = await response.json();

        if (response.ok) {
          // Update UI
          const category = data.predicted_category;
          const confidence = data.confidence * 100;
          const latency = data.latency_seconds;

          // Set category badge
          const categoryBadge = document.getElementById('categoryBadge');
          const categoryText = document.getElementById('categoryText');
          
          categoryBadge.textContent = category;
          categoryText.textContent = `Predicted Category`;

          // Add color class based on category
          categoryBadge.className = 'category-badge';
          if (category === 'Bug Report') categoryBadge.classList.add('bug-report');
          else if (category === 'Feature Request') categoryBadge.classList.add('feature-request');
          else if (category === 'Technical Issue') categoryBadge.classList.add('technical-issue');
          else if (category === 'Billing Inquiry') categoryBadge.classList.add('billing-inquiry');
          else if (category === 'Account Management') categoryBadge.classList.add('account-management');

          // Update confidence meter
          document.getElementById('confidenceFill').style.width = `${confidence}%`;
          document.getElementById('confidenceValue').textContent = `${confidence.toFixed(2)}%`;

          // Update latency
          document.getElementById('latencyValue').textContent = `${latency.toFixed(4)} seconds`;

          // Show result
          loadingDiv.style.display = 'none';
          resultCard.style.display = 'block';

          // Copy button functionality
          copyBtn.onclick = () => {
            const text = `Category: ${category}\nConfidence: ${confidence.toFixed(2)}%\nLatency: ${latency.toFixed(4)} seconds`;
            navigator.clipboard.writeText(text).then(() => {
              copyBtn.textContent = '✅ Copied!';
              setTimeout(() => { copyBtn.textContent = '📋 Copy Prediction'; }, 2000);
            });
          };

        } else {
          throw new Error(data.error || 'Unknown error');
        }

      } catch (err) {
        alert(`Error: ${err.message}`);
        console.error(err);
      } finally {
        classifyBtn.disabled = false;
        classifyBtn.innerHTML = '<span>Classify Ticket</span>';
      }
    });
  </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    start = time.time()
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    
    subject = data.get("Subject", "")
    description = data.get("Description", "")
    text = clean_text(subject + " " + description)
    
    try:
        vec = vectorizer.transform([text])
        pred = model.predict(vec)[0]
        conf = max(model.predict_proba(vec)[0])
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
    return jsonify({
        "predicted_category": pred,
        "confidence": round(float(conf), 4),
        "latency_seconds": round(time.time() - start, 4)
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    print("🚀 Starting Support Ticket Auto-Triage System...")
    print("👉 Open your browser and go to: http://localhost:5001")
    app.run(host='127.0.0.1', port=5001, debug=True)