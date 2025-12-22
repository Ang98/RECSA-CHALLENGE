import { useState, useEffect } from 'react';
import { LoginPage } from './features/auth/LoginPage';
import { ChatPage } from './features/chat/ChatPage'; // <--- Importamos el chat real

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) setIsAuthenticated(true);
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsAuthenticated(false);
  };

  return (
    <>
      {isAuthenticated ? (
        <ChatPage onLogout={handleLogout} /> 
      ) : (
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      )}
    </>
  );
}

export default App;