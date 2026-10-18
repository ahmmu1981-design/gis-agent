import React, { useMemo, useState } from 'react';

export interface WidgetProps {
  id: string;
  config?: {
    backendUrl?: string;
    mapWidgetId?: string;
    maxResults?: number;
    resultsLayerTitle?: string;
  };
}

export default function ConversationalGISWidget(props: WidgetProps) {
  const [messages, setMessages] = useState<Array<{ role: string; text: string }>>([
    { role: 'assistant', text: 'Ask a GIS question to begin.' },
  ]);
  const [value, setValue] = useState('');

  const backendUrl = useMemo(() => props.config?.backendUrl || 'http://localhost:8000/api', [props.config]);

  const sendMessage = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    setMessages((previous) => [...previous, { role: 'user', text: trimmed }]);
    setValue('');
    void fetch(`${backendUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: trimmed, request_id: `${Date.now()}` }),
    }).catch(() => {
      setMessages((previous) => [...previous, { role: 'assistant', text: 'The backend is unavailable. Check the configured URL and ensure the service is running.' }]);
    });
  };

  return (
    <div className="gis-chat-widget">
      <h3>GIS Assistant</h3>
      <div className="messages">
        {messages.map((message, index) => (
          <div key={`${message.role}-${index}`} className={`message ${message.role}`}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="controls">
        <input
          aria-label="GIS question"
          value={value}
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter') sendMessage();
          }}
          placeholder="Ask a GIS question"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      <p className="status">Backend: {backendUrl}</p>
    </div>
  );
}
