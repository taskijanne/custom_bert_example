import React, { useState } from 'react';

function App() {
  const [inputText, setInputText] = useState('');
  const [selectedModel, setSelectedModel] = useState('custom');
  const [sentiment, setSentiment] = useState('');
  const [confidence, setConfidence] = useState(null);

  const handleAnalyzeClick = async () => {
    try {
      // Call your backend API here
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputText,
          model: selectedModel,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setSentiment(data.sentiment);
        setConfidence(data.confidence);  // Optional: Only if confidence score is provided
      } else {
        console.error('Error analyzing sentiment');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <h1>Sentiment Analysis</h1>

      {/* Text input */}
      <div>
        <label htmlFor="inputText">Enter text:</label>
        <input
          type="text"
          id="inputText"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
      </div>

      {/* Model dropdown */}
      <div>
        <label htmlFor="modelSelect">Select Model:</label>
        <select
          id="modelSelect"
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
        >
          <option value="custom">Custom Model</option>
          <option value="llama">Llama 3</option>
        </select>
      </div>

      {/* Analyze button */}
      <div>
        <button onClick={handleAnalyzeClick}>Analyze Sentiment</button>
      </div>

      {/* Result display */}
      <div>
        {sentiment && (
          <div>
            <h2>Sentiment: {sentiment}</h2>
            {confidence !== null && <h3>Confidence: {confidence}</h3>}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;