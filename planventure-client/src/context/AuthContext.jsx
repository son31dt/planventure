import { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AuthContext = createContext(null);

const TOKEN_KEY = 'token';
const USER_KEY = 'user';

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state from localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem(TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);

    if (storedToken) {
      setToken(storedToken);
      setIsAuthenticated(true);
      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch (e) {
          console.error('Failed to parse stored user data:', e);
          localStorage.removeItem(USER_KEY);
        }
      }
    }
    setLoading(false);
  }, []);

  const login = useCallback((authData) => {
    try {
      setError(null);
      const token = authData.token;
      const userData = authData.user || authData;

      localStorage.setItem(TOKEN_KEY, token);
      if (userData) {
        localStorage.setItem(USER_KEY, JSON.stringify(userData));
      }

      setToken(token);
      setUser(userData);
      setIsAuthenticated(true);
    } catch (err) {
      setError('Login failed. Please try again.');
      console.error('Login error:', err);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const value = {
    // State
    isAuthenticated,
    token,
    user,
    loading,
    error,
    // Methods
    login,
    logout,
    clearError,
  };

  if (loading) {
    return null;
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};