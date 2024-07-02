import React from 'react';
import './App.css';
import Chat from '/home/jabez/week_11/Contract-Advisor-RAG/frontend/chatbot-frontend/src/components/chatbot.js';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Lizzy AI</h1>
        <h4> Chat with the contract </h4>
        <Chat />
      </header>
    </div>
  );
}

export default App;
