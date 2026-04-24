import React, { useState } from 'react';

const API_BASE = 'https://solid-barnacle-97jvw9gg5g4j3px6x-8000.app.github.dev';

function Login({ onLogin }: { onLogin: (token: string) => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const response = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `username=${email}&password=${password}`
      });
      const data = await response.json();
      if (data.access_token) {
        onLogin(data.access_token);
      } else {
        setError('Invalid credentials');
      }
    } catch {
      setError('Login failed');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: '#f0f2f5' }}>
      <div style={{ background: 'white', padding: '40px', borderRadius: '10px', width: '350px', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
        <h2 style={{ textAlign: 'center', color: '#1a1a2e' }}>🎫 AI ITSM Platform</h2>
        <p style={{ textAlign: 'center', color: '#666' }}>Login to continue</p>
        {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
        <input
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          style={{ width: '100%', padding: '12px', margin: '8px 0', borderRadius: '6px', border: '1px solid #ddd', boxSizing: 'border-box' }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          style={{ width: '100%', padding: '12px', margin: '8px 0', borderRadius: '6px', border: '1px solid #ddd', boxSizing: 'border-box' }}
        />
        <button
          onClick={handleLogin}
          style={{ width: '100%', padding: '12px', background: '#4361ee', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '16px', marginTop: '10px' }}
        >
          Login
        </button>
      </div>
    </div>
  );
}

function Dashboard({ token }: { token: string }) {
  const [tickets, setTickets] = useState<any[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [message, setMessage] = useState('');

  const TICKET_API = 'https://solid-barnacle-97jvw9gg5g4j3px6x-8001.app.github.dev';

  const createTicket = async () => {
    try {
      const response = await fetch(`${TICKET_API}/tickets`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ title, description, priority })
      });
      const data = await response.json();
      if (data.id) {
        setMessage('Ticket created successfully!');
        setTitle('');
        setDescription('');
        fetchTickets();
      }
    } catch {
      setMessage('Failed to create ticket');
    }
  };

  const fetchTickets = async () => {
    try {
      const response = await fetch(`${TICKET_API}/tickets`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setTickets(data.tickets || data);
    } catch {
      setMessage('Failed to fetch tickets');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <h1 style={{ color: '#1a1a2e' }}>🎫 AI ITSM Dashboard</h1>

      <div style={{ background: 'white', padding: '20px', borderRadius: '10px', marginBottom: '20px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
        <h3>Create New Ticket</h3>
        {message && <p style={{ color: 'green' }}>{message}</p>}
        <input
          placeholder="Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          style={{ width: '100%', padding: '10px', margin: '6px 0', borderRadius: '6px', border: '1px solid #ddd', boxSizing: 'border-box' }}
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={e => setDescription(e.target.value)}
          style={{ width: '100%', padding: '10px', margin: '6px 0', borderRadius: '6px', border: '1px solid #ddd', boxSizing: 'border-box', height: '80px' }}
        />
        <select
          value={priority}
          onChange={e => setPriority(e.target.value)}
          style={{ width: '100%', padding: '10px', margin: '6px 0', borderRadius: '6px', border: '1px solid #ddd', boxSizing: 'border-box' }}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <button
          onClick={createTicket}
          style={{ padding: '10px 20px', background: '#4361ee', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', marginRight: '10px' }}
        >
          Create Ticket
        </button>
        <button
          onClick={fetchTickets}
          style={{ padding: '10px 20px', background: '#7209b7', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
        >
          Load Tickets
        </button>
      </div>

      <div>
        {tickets.map((ticket: any) => (
          <div key={ticket.id} style={{ background: 'white', padding: '15px', borderRadius: '10px', marginBottom: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', borderLeft: `4px solid ${ticket.priority === 'high' ? 'red' : ticket.priority === 'medium' ? 'orange' : 'green'}` }}>
            <h4 style={{ margin: '0 0 5px 0' }}>#{ticket.id} — {ticket.title}</h4>
            <p style={{ margin: '0 0 5px 0', color: '#666' }}>{ticket.description}</p>
            <span style={{ background: '#e8f4fd', padding: '3px 8px', borderRadius: '4px', fontSize: '12px', marginRight: '8px' }}>Priority: {ticket.priority}</span>
            <span style={{ background: '#f0fff4', padding: '3px 8px', borderRadius: '4px', fontSize: '12px' }}>Status: {ticket.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  const [token, setToken] = useState('');

  if (!token) return <Login onLogin={setToken} />;
  return <Dashboard token={token} />;
}

export default App;