import React, { useState, useEffect } from 'react';
import ChatBot from 'react-chatbotify';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

function App() {
  const [count, setCount] = useState(0);
  const [userInput, setUserInput] = useState('');
  const [output, setOutput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const handleUserGesture = () => {
      if (typeof AudioContext !== 'undefined') {
        const audioContext = new AudioContext();
        if (audioContext.state === 'suspended') {
          audioContext.resume();
        }
      }
    };

    document.addEventListener('click', handleUserGesture, { once: true });

    return () => {
      document.removeEventListener('click', handleUserGesture);
    };
  }, []);

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: userInput }),
      });

      const data = await response.json();
      if (response.ok) {
        setOutput(data.output);
      } else {
        setOutput(data.output || "An error occurred. Please try again.");
        console.error(`Server error: ${data.output}`);
      }
    } catch (error) {
      setOutput("Sorry, I do not understand your message 😢! If you require further assistance, you may click on the Github option and open an issue there or visit our discord.");
      console.error(`Fetch error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <ChatBot />
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <div>
        <input type="text" value={userInput} onChange={handleInputChange} />
        <button onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? 'Loading...' : 'Submit'}
        </button>
        <p>{output}</p>
      </div>
    </>
  );
}

export default App;
