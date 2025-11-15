import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')

  const handleSubmit = async () => {
    if (!input.trim()) return

    const userMessage = input
    setInput('')
        
    setMessages([...messages, { role: 'user', content: userMessage }])

    try {
      const response = await fetch('http://localhost:11434/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'gemma3:latest',
          prompt: userMessage,
          stream: false
        })
      })

      const data = await response.json()

      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.response 
      }])

    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Error: Could not connect to Ollama. Make sure it is running.' 
      }])      
    }
  }

  const handleKeyPress = (e) => {
    if (e.key == 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className='chat-container'>
      {/* Header area*/ }
      <div className='chat-header'>
        RAG Mentor
      </div>

      {/* Chat area*/ }
      <div className='message-area'>
        {messages.length === 0 ? (
          <div className='empty-state'>
            Start a Conversation!
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-label">
                {msg.role === 'user' ? 'You' : 'Assistant'}
              </div>
              <div className="message-content">{msg.content}</div>
            </div>         
          ))
        )}
      </div>

      {/* Input area */}
      <div className="input-area">
        <div className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Send a message..."
            className="message-input"
          />
          <button onClick={handleSubmit} className="send-button">
            Send
          </button>
        </div>
      </div>      
    </div>
  )
}

export default App
