import { api } from './api';

export const tripService = {
  getAllTrips: async () => {
    try {
      const response = await api.get('/api/trips');
      return response;
    } catch (error) {
      console.error('Error fetching trips:', error);
      throw error;
    }
  },

  createTrip: async (tripData) => {
    try {
      const response = await api.post('/api/trips', tripData);
      return response;
    } catch (error) {
      console.error('Error creating trip:', error);
      throw error;
    }
  },

  getTrip: async (tripId) => {
    try {
      const response = await api.get(`/api/trips/${tripId}`);
      return response;
    } catch (error) {
      console.error('Error fetching trip:', error);
      throw error;
    }
  },

  updateTrip: async (tripId, tripData) => {
    try {
      const response = await api.put(`/api/trips/${tripId}`, tripData);
      return response;
    } catch (error) {
      console.error('Error updating trip:', error);
      throw error;
    }
  },

  deleteTrip: async (tripId) => {
    try {
      const response = await api.delete(`/api/trips/${tripId}`);
      return response;
    } catch (error) {
      console.error('Error deleting trip:', error);
      throw error;
    }
  }
};

