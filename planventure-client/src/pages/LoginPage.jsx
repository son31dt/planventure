import { Box, Grid, Stack, Typography, Chip } from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import AuthLayout from '../layouts/AuthLayout';
import LoginForm from '../components/auth/LoginForm';

const LoginPage = () => {
  return (
    <AuthLayout
      maxWidth="md"
      cardSx={{
        p: { xs: 3, sm: 4 },
        gap: { xs: 3, md: 4 },
      }}
    >
      <Grid container spacing={{ xs: 3, md: 4 }} alignItems="stretch">
        <Grid item xs={12} md={6}>
          <Stack spacing={2} sx={{ height: '100%' }}>
            <Chip label="Planventure" color="primary" variant="outlined" sx={{ alignSelf: 'flex-start' }} />
            <Typography variant="h4" component="h1">
              Welcome back
            </Typography>
            <Typography color="text.secondary">
              Sign in to pick up where you left off, update your itineraries, and keep your travel plans in sync.
            </Typography>
            <Stack spacing={1}>
              {["Save trips in one place", "Invite friends and share plans", "Stay synced across devices"].map(text => (
                <Stack key={text} direction="row" spacing={1} alignItems="center" color="text.secondary">
                  <CheckCircleOutlineIcon color="primary" fontSize="small" />
                  <Typography variant="body2">{text}</Typography>
                </Stack>
              ))}
            </Stack>
          </Stack>
        </Grid>

        <Grid item xs={12} md={6}>
          <Box sx={{ height: '100%', display: 'flex', alignItems: 'center' }}>
            <LoginForm />
          </Box>
        </Grid>
      </Grid>
    </AuthLayout>
  );
};

export default LoginPage;
