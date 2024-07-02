import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [conversation, setConversation] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setConversation([...conversation, { type: 'user', text: message }]);

        try {
            const res = await axios.post('http://localhost:5000/chat', { message });
            setResponse(res.data.response);
            setConversation([...conversation, { type: 'user', text: message }, { type: 'bot', text: res.data.response }]);
        } catch (error) {
            console.error('Error:', error);
            if (error.response) {
                // Server responded with a status other than 200 range
                setError(`Error: ${error.response.status} ${error.response.data.output}`);
            } else if (error.request) {
                // Request was made but no response received
                setError('No response from server. Please try again later.');
            } else {
                // Something else happened in setting up the request
                setError('Something went wrong. Please try again.');
            }
        } finally {
            setLoading(false);
        }
        setMessage('');
    };

    return (
        <div style={styles.container}>
            <div style={styles.chatWindow}>
                {conversation.map((msg, index) => (
                    <div key={index} style={msg.type === 'user' ? styles.userMessage : styles.botMessage}>
                        {msg.text}
                    </div>
                ))}
                {loading && <div style={styles.botMessage}>Bot is typing...</div>}
            </div>
            <form onSubmit={handleSubmit} style={styles.form}>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Type your message"
                    style={styles.input}
                />
                <button type="submit" style={styles.button} disabled={loading}>
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </form>
            {error && <p style={styles.error}>{error}</p>}
        </div>
    );
};

const styles = {
    container: {
        maxWidth: '600px',
        margin: '0 auto',
        padding: '20px',
        textAlign: 'center',
        fontFamily: 'Arial, sans-serif',
    },
    chatWindow: {
        height: '400px',
        border: '1px solid #ccc',
        borderRadius: '10px',
        padding: '10px',
        overflowY: 'scroll',
        backgroundColor: '#f9f9f9',
        marginBottom: '20px',
        boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
    },
    form: {
        display: 'flex',
        alignItems: 'center',
    },
    input: {
        flex: '1',
        padding: '10px',
        fontSize: '16px',
        borderRadius: '20px',
        border: '1px solid #ccc',
        marginRight: '10px',
    },
    button: {
        padding: '10px 20px',
        fontSize: '16px',
        borderRadius: '20px',
        border: 'none',
        backgroundColor: '#007BFF',
        color: 'white',
        cursor: 'pointer',
    },
    userMessage: {
        textAlign: 'right',
        margin: '10px 0',
        padding: '10px',
        borderRadius: '10px',
        backgroundColor: '#007BFF',
        color: 'white',
        display: 'inline-block',
        maxWidth: '70%',
    },
    botMessage: {
        textAlign: 'left',
        margin: '10px 0',
        padding: '10px',
        borderRadius: '10px',
        backgroundColor: '#e5e5ea',
        color: 'black',
        display: 'inline-block',
        maxWidth: '70%',
    },
    error: {
        color: 'red',
        marginTop: '20px',
    },
};

export default Chat;
