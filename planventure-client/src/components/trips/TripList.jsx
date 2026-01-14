import { useState, useEffect } from 'react';
import { 
  Grid, 
  Typography, 
  Box, 
  Alert,
  Button,
  CircularProgress,
  Container
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import TripCard from './TripCard';
import { useNavigate } from 'react-router-dom';
import { tripService } from '../../services/tripService';

const TripList = ({ WelcomeMessage, ErrorState }) => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await tripService.getAllTrips();
      
      if (!data || !data.trips) {
        console.error('Invalid data format:', data);
        setError('Unexpected data format received');
        return;
      }
      
      setTrips(data.trips);
    } catch (err) {
      console.error('TripList error:', err);
      setError(err.message || 'Failed to load trips');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTrip = async (tripId) => {
    try {
      await tripService.deleteTrip(tripId);
      setTrips(trips.filter(trip => trip.id !== tripId));
    } catch (err) {
      setError('Failed to delete trip: ' + err.message);
    }
  };

  // Loading state with skeleton cards
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
      </Box>
    );
  }

  // Error state
  if (error) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={fetchTrips}>
          Try Again
        </Button>
      </Container>
    );
  }

  // Empty state
  if (trips.length === 0) {
    return <WelcomeMessage />;
  }

  // Loaded state with trips
  return (
    <>
      <Grid container spacing={3}>
        {trips.map((trip) => (
          <Grid item xs={12} sm={6} md={4} key={trip.id}>
            <TripCard trip={trip} onDelete={handleDeleteTrip} />
          </Grid>
        ))}
        <Grid item xs={12} sm={6} md={4}>
          <Button
            variant="outlined"
            fullWidth
            sx={{ 
              height: '100%', 
              minHeight: 200,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.3s ease',
              '&:hover': {
                backgroundColor: 'action.hover',
                borderColor: 'primary.main'
              }
            }}
            onClick={() => navigate('/trips/new')}
          >
            <AddIcon sx={{ mb: 1, fontSize: 40 }} />
            <Typography>Add New Trip</Typography>
          </Button>
        </Grid>
      </Grid>
    </>
  );
};

export default TripList;
