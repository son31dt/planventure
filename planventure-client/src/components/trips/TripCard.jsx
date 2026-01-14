import { 
  Card, 
  CardContent, 
  CardMedia, 
  Typography, 
  CardActions, 
  Button,
  Chip,
  Box,
  Skeleton,
  IconButton
} from '@mui/material';
import { 
  LocationOn, 
  DateRange,
  ArrowForward,
  Edit as EditIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

const TripCard = ({ trip, loading, onDelete }) => {
  const navigate = useNavigate();
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this trip?')) {
      setDeleting(true);
      try {
        await onDelete(trip.id);
      } finally {
        setDeleting(false);
      }
    }
  };

  if (loading) {
    return (
      <Card sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        transition: 'all 0.3s ease'
      }}>
        <Skeleton variant="rectangular" height={140} />
        <CardContent>
          <Skeleton variant="text" height={32} width="80%" />
          <Skeleton variant="text" height={24} width="60%" sx={{ mt: 1 }} />
          <Skeleton variant="text" height={24} width="40%" sx={{ mt: 1 }} />
        </CardContent>
        <CardActions>
          <Skeleton variant="rectangular" width={100} height={36} />
        </CardActions>
      </Card>
    );
  }

  const daysUntilTrip = Math.ceil(
    (new Date(trip.start_date) - new Date()) / (1000 * 60 * 60 * 24)
  );
  const tripStatus = daysUntilTrip > 0 ? 'upcoming' : daysUntilTrip === 0 ? 'today' : 'past';
  const statusColor = tripStatus === 'upcoming' ? 'info' : tripStatus === 'today' ? 'success' : 'default';

  return (
    <Card sx={{ 
      height: '100%', 
      display: 'flex', 
      flexDirection: 'column',
      transition: 'all 0.3s ease',
      '&:hover': {
        boxShadow: 4,
        transform: 'translateY(-4px)'
      }
    }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 1 }}>
          <Typography gutterBottom variant="h5" component="h2" sx={{ m: 0 }}>
            {trip.title}
          </Typography>
          <Chip 
            label={tripStatus.charAt(0).toUpperCase() + tripStatus.slice(1)} 
            size="small"
            color={statusColor}
            variant="outlined"
          />
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <LocationOn fontSize="small" color="primary" />
          <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
            {trip.destination}
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <DateRange fontSize="small" color="primary" />
          <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
            {new Date(trip.start_date).toLocaleDateString()} - {new Date(trip.end_date).toLocaleDateString()}
          </Typography>
        </Box>

        {trip.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {trip.description.substring(0, 100)}...
          </Typography>
        )}
      </CardContent>
      
      <CardActions sx={{ justifyContent: 'space-between' }}>
        <Button 
          size="small" 
          endIcon={<ArrowForward />}
          onClick={() => navigate(`/trips/${trip.id}`)}
        >
          View Details
        </Button>
        <Box>
          <IconButton 
            size="small" 
            onClick={() => navigate(`/trips/${trip.id}/edit`)}
            title="Edit trip"
          >
            <EditIcon fontSize="small" />
          </IconButton>
          <IconButton 
            size="small" 
            onClick={handleDelete}
            disabled={deleting}
            title="Delete trip"
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        </Box>
      </CardActions>
    </Card>
  );
};

export default TripCard;
