// Get form elements
const form = document.getElementById('predictionForm');
const colorPreview = document.getElementById('colorPreview');
const resultCard = document.getElementById('resultCard');
const resultValue = document.getElementById('resultValue');
const inputSummary = document.getElementById('inputSummary');
const predictBtn = document.querySelector('.predict-btn');

// Input elements
const rInput = document.getElementById('r');
const gInput = document.getElementById('g');
const bInput = document.getElementById('b');
const brixInput = document.getElementById('brix');
const hardnessInput = document.getElementById('hardness');

// Update color preview when RGB values change
function updateColorPreview() {
    const r = rInput.value || 0;
    const g = gInput.value || 0;
    const b = bInput.value || 0;
    
    colorPreview.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
    colorPreview.textContent = `RGB(${r}, ${g}, ${b})`;
}

// Add event listeners to RGB inputs
[rInput, gInput, bInput].forEach(input => {
    input.addEventListener('input', updateColorPreview);
});

// Initialize color preview
updateColorPreview();

// API Configuration
const API_URL = 'http://localhost:5000/predict';  // Change this to your deployed API URL

// Prediction function using REST API
async function predictAntiOxidation(r, g, b, brix, hardness) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                r: r,
                g: g,
                b: b,
                brix: brix,
                hardness: hardness
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Prediction failed');
        }
        
        const data = await response.json();
        return data.prediction.toFixed(2);
        
    } catch (error) {
        console.error('Prediction error:', error);
        throw error;
    }
}

// Form submission handler
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Add loading state
    predictBtn.classList.add('loading');
    
    // Get input values
    const r = parseFloat(rInput.value);
    const g = parseFloat(gInput.value);
    const b = parseFloat(bInput.value);
    const brix = parseFloat(brixInput.value);
    const hardness = parseFloat(hardnessInput.value);
    
    try {
        // Make prediction
        const prediction = await predictAntiOxidation(r, g, b, brix, hardness);
        
        // Display results
        resultValue.textContent = prediction;
        
        // Update input summary
        inputSummary.innerHTML = `
            <li><strong>R:</strong> ${r}</li>
            <li><strong>G:</strong> ${g}</li>
            <li><strong>B:</strong> ${b}</li>
            <li><strong>Brix:</strong> ${brix} °Bx</li>
            <li><strong>Hardness:</strong> ${hardness}</li>
        `;
        
        // Show result card
        resultCard.style.display = 'block';
        
        // Scroll to results
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
    } catch (error) {
        // Show error message
        alert(`Prediction failed: ${error.message}\n\nPlease make sure the API server is running.`);
    } finally {
        // Remove loading state
        predictBtn.classList.remove('loading');
    }
});

// Optional: Add input validation
function validateInputs() {
    const r = parseInt(rInput.value);
    const g = parseInt(gInput.value);
    const b = parseInt(bInput.value);
    
    if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
        alert('RGB values must be between 0 and 255');
        return false;
    }
    
    return true;
}

// Export model notes for future implementation:
/*
To implement the actual XGBoost model, you have several options:

1. Export to ONNX and use ONNX.js:
   - In Python: model.save_model("model.json") or convert to ONNX
   - Load in JavaScript with ONNX Runtime Web

2. Create a REST API:
   - Deploy your Python model to a server (Flask, FastAPI)
   - Make fetch() calls from this JavaScript to your API

3. Use TensorFlow.js:
   - Convert XGBoost to TensorFlow format
   - Load with TensorFlow.js

Example API call approach:
async function predictAntiOxidation(r, g, b, brix, hardness) {
    const response = await fetch('YOUR_API_ENDPOINT', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ r, g, b, brix, hardness })
    });
    const data = await response.json();
    return data.prediction;
}
*/
