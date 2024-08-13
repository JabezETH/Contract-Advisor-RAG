import React from 'react';
import './App.css';
import Chat from '/home/jabez/dockerized_projects/Contract-Advisor-RAG/frontend/chatbot-frontend/src/chatbot.js';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Lizzy AI</h1>
        <h2> Legal Contract Assistant </h2>
        <Chat />
      </header>
    </div>
  );
}

export default App;
