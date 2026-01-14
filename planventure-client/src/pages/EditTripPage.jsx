import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Alert, Button, Skeleton } from '@mui/material';
import EditTripForm from '../components/trips/EditTripForm';
import { tripService } from '../services/tripService';

const EditTripPage = () => {
  const { tripId } = useParams();
  const navigate = useNavigate();
  const [trip, setTrip] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTrip = async () => {
      try {
        const response = await tripService.getTrip(tripId);
        // Handle different response formats
        let tripData = null;
        if (response && response.trip) {
          tripData = response.trip;
        } else if (response && response.id) {
          tripData = response;
        }

        if (!tripData) {
          throw new Error('Trip not found');
        }
        setTrip(tripData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTrip();
  }, [tripId]);

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Skeleton variant="rectangular" height={400} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert 
          severity="error"
          action={
            <Button color="inherit" size="small" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </Button>
          }
        >
          {error}
        </Alert>
      </Box>
    );
  }

  if (!trip) {
    return null;
  }

  return (
    <Box sx={{ p: 3 }}>
      <EditTripForm trip={trip} />
    </Box>
  );
};

export default EditTripPage;
