import React, { useState } from 'react';

function App() {
  const [inputText, setInputText] = useState('');
  const [selectedModel, setSelectedModel] = useState('custom');
  const [sentiment, setSentiment] = useState('');
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const handleAnalyzeClick = async () => {
    try {
      setSentiment(null);
      setConfidence(null);
      setLoading(true);
      setErrorMessage(null);
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
      setLoading(false);
      if (response.ok) {
        const data = await response.json();
        console.log(data)
        if (data.sentiment){
          setSentiment(data.sentiment);
          setConfidence(data.confidence); 
        }
        else {
          setErrorMessage('Error analyzing sentiment');
        }

      } else {
        setErrorMessage('Error analyzing sentiment');
      }
    } catch (error) {
      console.error('Error:', error);
      setErrorMessage('Error analyzing sentiment');
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
        <button onClick={handleAnalyzeClick} disabled={loading}>{loading ? "Analyzing sentiment... " : "Analyze sentiment"}</button>
      </div>

      {/* Error message */}
      {errorMessage && <div>{errorMessage}</div>}

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