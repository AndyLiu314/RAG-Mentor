import { useState, useRef } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [uploading, setUploading] = useState(false)
  const [sessionId] = useState(() => `session_${Date.now()}`) // Generate unique session ID
  const fileInputRef = useRef(null)

  const handleSubmit = async () => {
    if (!input.trim()) return

    const userMessage = input
    setInput('')
        
    setMessages([...messages, { role: 'user', content: userMessage }])

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userMessage,
          session_id: sessionId
        }),
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
        content: 'Error: Could not connect to backend.' 
      }])      
    }
  }

  const handleKeyPress = (e) => {
    if (e.key == 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `✓ ${data.message} (${data.chunks_added} chunks added)`
      }])
    } catch (error) {
      console.error('Upload error:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '✗ Upload failed'
      }])
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handlePlusClick = () => {
    fileInputRef.current?.click()
  }

  const handleNewChat = async () => {
    setMessages([])
    
    try {
      await fetch(`http://localhost:8000/api/chat/history/${sessionId}`, {
        method: 'DELETE'
      })
    } catch (error) {
      console.error('Error clearing history:', error)
    }
    
    window.location.reload()
  }

  return (
    <div className='chat-container'>
      {/* Header area */}
      <div className='chat-header'>
        RAG Mentor
        <button 
          onClick={handleNewChat}
          style={{
            marginLeft: 'auto',
            padding: '8px 16px',
            background: '#444',
            border: 'none',
            borderRadius: '6px',
            color: 'white',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          New Chat
        </button>
      </div>

      {/* Chat area */}
      <div className='messages-area'>
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
          <button 
            onClick={handlePlusClick} 
            className="upload-button"
            disabled={uploading}
            title="Upload PDF"
          >
            {uploading ? '⋯' : '+'}
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
          />
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
