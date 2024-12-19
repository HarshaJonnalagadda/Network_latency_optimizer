import axios from 'axios';

// Create an Axios instance with base settings
const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // Base URL for the Django backend
  timeout: 10000, // Set a request timeout of 10 seconds
  headers: {
    'Content-Type': 'application/json', // Ensure JSON format
    Accept: 'application/json',
  },
});

// Export the instance to reuse in components
export default api;
