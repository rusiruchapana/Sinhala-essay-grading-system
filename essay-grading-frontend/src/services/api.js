import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const gradeEssay = async (formData) => {
  try {
    const response = await api.post('/evaluate-essay/', formData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};