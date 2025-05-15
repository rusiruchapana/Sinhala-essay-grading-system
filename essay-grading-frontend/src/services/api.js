import axios from 'axios';

class ApiError extends Error {
  constructor(message, details = '', status = 500) {
    super(message);
    this.name = 'ApiError';
    this.details = details;
    this.status = status;
  }
}

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
    if (error.response) {
      // The request was made and the server responded with a status code
      throw new ApiError(
        error.response.data.error || 'An error occurred',
        error.response.data.details || '',
        error.response.status
      );
    } else if (error.request) {
      // The request was made but no response was received
      throw new ApiError('Server is not responding. Please try again later.');
    } else {
      // Something happened in setting up the request that triggered an Error
      throw new ApiError(error.message || 'An unexpected error occurred');
    }
  }
};

export const getAllEssays = async () => {
  try {
    const response = await api.get('/get-all-essays/');
    return response.data.essays;
  } catch (error) {
    if (error.response) {
      throw new ApiError(
        error.response.data.error || 'Failed to fetch essays',
        error.response.data.details || '',
        error.response.status
      );
    }
    throw new ApiError('Network error while fetching essays');
  }
};

export const deleteEssay = async (id) => {
  try {
    await api.delete(`/delete-essay/${id}/`);
  } catch (error) {
    if (error.response) {
      throw new ApiError(
        error.response.data.error || 'Failed to delete essay',
        error.response.data.details || '',
        error.response.status
      );
    }
    throw new ApiError('Network error while deleting essay');
  }
};