import { useState } from 'react';
import './App.css';

const API_BASE_URL = 'http://localhost:8000/api';

async function callApi(endpoint, payload) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`API call failed: ${response.statusText}`);
  }

  return response.json();
}


function App() {
  const [question, setQuestion] = useState('');
  const [lastQuestion, setLastQuestion] = useState("")
  const [answer, setAnswer] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }
    
    setIsLoading(true);
    try {
      const data = await callApi('/ask', { question });
      setAnswer(data.answer);
      setLastQuestion(question);
      setQuestion('');
    } catch {
      setAnswer('Error fetching answer.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    if (e.target.value.length <= 200) {
      setQuestion(e.target.value);
    }
  };

  return (
    <div className="app-container">
      <h1>AI FAQ Chatbot</h1>
      {answer && (
        <div className="answer-block">
          <strong>Q:</strong> {lastQuestion}
          <br /><br />
          <strong>A:</strong> {answer}
        </div>
      )}
      <div className="input-block">
        <input
          type="text"
          placeholder="Ask your question..."
          value={question}
          onChange={handleInputChange}
          maxLength={200}
          className="question-input"
        />
        <button onClick={askQuestion} disabled={isLoading}>
          {isLoading ? 'Getting answers...' : 'Submit'}
        </button>
      </div>
    </div>
  );
}

export default App;
