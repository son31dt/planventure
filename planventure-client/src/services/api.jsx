const BASE_URL = 'http://localhost:5000';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
};

const handleResponse = async (response) => {
  console.log('API Response Status:', response.status);
  
  if (response.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
    throw new Error('Session expired. Please login again.');
  }

  if (response.status === 404) {
    throw new Error('Trip not found');
  }

  const data = await response.json();
  console.log('API Response Data:', data);
  
  if (!response.ok) {
    throw new Error(data.error || data.message || `Request failed with status ${response.status}`);
  }

  return data;
};

export const api = {
  get: async (endpoint) => {
    try {
      console.log('GET Request to:', `${BASE_URL}${endpoint}`);
      const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('API GET Error:', error);
      throw error;
    }
  },
  
  post: async (endpoint, data) => {
    try {
      console.log('POST Request to:', `${BASE_URL}${endpoint}`, 'Data:', data);
      const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('API POST Error:', error);
      throw error;
    }
  },

  put: async (endpoint, data) => {
    try {
      console.log('PUT Request to:', `${BASE_URL}${endpoint}`, 'Data:', data);
      const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('API PUT Error:', error);
      throw error;
    }
  },

  delete: async (endpoint) => {
    try {
      console.log('DELETE Request to:', `${BASE_URL}${endpoint}`);
      const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('API DELETE Error:', error);
      throw error;
    }
  },

  auth: {
    login: async (credentials) => {
      return api.post('/auth/login', credentials);
    },

    register: async (userData) => {
      return api.post('/auth/register', userData);
    }
  }
};

export default api;