# Anti-oxidation Prediction System

A web-based application that predicts anti-oxidation levels from RGB color values, Brix (sugar content), and hardness measurements using an XGBoost machine learning model.

## 🌐 Live Demo
- **Frontend**: Deploy to GitHub Pages
- **API**: Deploy to Heroku, Railway, or any cloud platform

## 📁 Project Structure
```
RGB_authorization/
├── index.html          # Main web interface
├── style.css          # Styling
├── script.js          # Frontend JavaScript
├── app.py             # Flask REST API
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## 🚀 Quick Start

### 1. Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the API Server
```bash
python app.py
```
The API will start at `http://localhost:5000`

### 3. Test the API
Open another terminal and test:
```bash
# Health check
curl http://localhost:5000/health

# Make a prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d "{\"r\": 200, \"g\": 150, \"b\": 100, \"brix\": 12.5, \"hardness\": 8.3}"
```

### 4. Open the Web Interface
Simply open `index.html` in your browser, or use:
```bash
# On Windows:
start index.html

# On Mac:
open index.html

# On Linux:
xdg-open index.html
```

## 🌍 Deployment

### Deploy API to Heroku
1. Create a `Procfile`:
   ```
   web: python app.py
   ```

2. Update `app.py` to use environment port:
   ```python
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Deploy Frontend to GitHub Pages
1. Create a new GitHub repository
2. Push your code:
   ```bash
   git init
   git add index.html style.css script.js
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

3. Enable GitHub Pages in repository settings
4. Update `script.js` with your API URL:
   ```javascript
   const API_URL = 'https://your-heroku-app.herokuapp.com/predict';
   ```

### Alternative Deployment Options

#### Railway.app (Recommended - Free Tier)
1. Connect your GitHub repository
2. Railway auto-detects Python and deploys
3. Get your API URL and update `script.js`

#### Render.com
1. Create new Web Service
2. Connect repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `python app.py`

#### Vercel (Serverless)
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json` for API routes
3. Deploy: `vercel`

## 📊 API Endpoints

### `GET /`
API documentation and available endpoints

### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### `POST /predict`
Make anti-oxidation prediction
```json
Request:
{
  "r": 200,
  "g": 150,
  "b": 100,
  "brix": 12.5,
  "hardness": 8.3
}

Response:
{
  "prediction": 85.42,
  "input": {
    "r": 200,
    "g": 150,
    "b": 100,
    "brix": 12.5,
    "hardness": 8.3
  },
  "status": "success"
}
```

## 🔧 Configuration

### Update Dataset Path
Edit `app.py` line 18:
```python
csv_path = r"YOUR_PATH_TO\total_rgb_Brix_Hardness_AC.csv"
```

### Update API URL for Production
Edit `script.js` line 2:
```javascript
const API_URL = 'https://your-deployed-api.com/predict';
```

## 🛠️ Model Details
- **Algorithm**: XGBoost Regression
- **Features**: R, G, B, Brix, Hardness
- **Target**: Anti-oxidation
- **Parameters**:
  - max_depth: 4
  - eta: 0.1
  - subsample: 0.8
  - colsample_bytree: 0.8

## 📝 License
MIT License

## 👤 Author
ME AND AI

## 🤝 Contributing
Pull requests are welcome!

