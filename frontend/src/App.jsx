import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')

  const handleSubmit = () => {
    if (!input.trim()) return
        
    setMessages([...messages, { role: 'user', content: input }])

    // Simulate AI response (replace with actual API call later)
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'This is a placeholder' 
      }])
    }, 500)

    setInput('')
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
