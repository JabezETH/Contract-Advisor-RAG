import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
    const [message, setMessage] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [conversation, setConversation] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setConversation([...conversation, { type: 'user', text: message }]);

        const formData = new FormData();
        formData.append('message', message);
        if (file) {
            formData.append('file', file);
        }

        try {
            const res = await axios.post('http://localhost:5000/chat', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            const chatbotResponse = res.data.response;

            setConversation([...conversation, { type: 'user', text: message }, { type: 'bot', text: chatbotResponse.content }]);
        } catch (error) {
            console.error('Error:', error);
            if (error.response) {
                setError(`Error: ${error.response.status} ${error.response.data.output}`);
            } else if (error.request) {
                setError('No response from server. Please try again later.');
            } else {
                setError('Something went wrong. Please try again.');
            }
        } finally {
            setLoading(false);
        }
        setMessage('');
        setFile(null);
    };

    return (
        <div style={styles.page}>
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
                    <input
                        type="file"
                        onChange={(e) => setFile(e.target.files[0])}
                        style={styles.fileInput}
                    />
                    <button type="submit" style={styles.button} disabled={loading}>
                        {loading ? 'Sending...' : 'Send'}
                    </button>
                </form>
                {error && <p style={styles.error}>{error}</p>}
            </div>
        </div>
    );
};

const styles = {
    page: {
        minHeight: '50vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
    },
    container: {
        maxWidth: '600px',
        width: '100%',
        margin: '0 auto',
        padding: '20px',
        textAlign: 'center',
        fontFamily: 'Arial, sans-serif',
        backgroundColor: 'rgba(255, 255, 255, 0.5)', // White background for chat box
        borderRadius: '20px', // Rounded corners for chat box
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Optional: Add a subtle shadow for better appearance
    },
    chatWindow: {
        display: 'flex',
        flexDirection: 'column',
        height: '400px',
        border: '1px solid #003366', // Dark blue border
        borderRadius: '10px',
        padding: '10px',
        overflowY: 'scroll',
        backgroundColor: 'rgba(255, 255, 255, 0.5)', // White background for chat window
        marginBottom: '20px',
        boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)',
    },
    form: {
        display: 'flex',
        alignItems: 'center',
    },
    input: {
        textAlign: 'left',
        flex: '1',
        padding: '10px',
        fontSize: '16px',
        borderRadius: '20px',
        border: '1px solid #003366', // Dark blue border
        marginRight: '10px',
    },
    fileInput: {
        flex: '1',
        padding: '10px',
        fontSize: '16px',
        borderRadius: '20px',
        border: '1px solid #003366', // Dark blue border
        marginRight: '10px',
    },
    button: {
        padding: '10px 20px',
        fontSize: '16px',
        borderRadius: '20px',
        border: 'none',
        backgroundColor: '#003366', // Dark blue background
        color: 'white',
        cursor: 'pointer',
    },
    userMessage: {
        alignSelf: 'flex-end',
        textAlign: 'right',
        margin: '10px 0',
        padding: '10px',
        borderRadius: '10px',
        backgroundColor: '#007BFF', // Blue background for user messages
        color: 'white',
        display: 'inline-block',
        maxWidth: '70%',
        fontSize: '16px',
    },
    botMessage: {
        alignSelf: 'flex-start',
        textAlign: 'left',
        margin: '10px 0',
        padding: '10px',
        borderRadius: '10px',
        backgroundColor: '#e5e5ea', // Light grey background for bot messages
        color: 'black',
        display: 'inline-block',
        maxWidth: '70%',
        fontSize: '14px',
    },
    error: {
        color: 'red',
        marginTop: '20px',
    },
};

export default Chat;
