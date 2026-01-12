import { AppBar, Box, Toolbar, Typography, Button, Stack } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar = () => {
  const navigate = useNavigate();
  const { isAuthenticated, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <AppBar position="fixed">
      <Toolbar>
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ flexGrow: 1, cursor: 'pointer', textAlign: 'left' }}
          onClick={() => navigate('/')}
        >
          Planventure
        </Typography>
        <Stack direction="row" spacing={1.5}>
          {isAuthenticated ? (
            <>
              <Button 
                color="inherit" 
                onClick={() => navigate('/trips')}
              >
                My Trips
              </Button>
              <Button 
                color="inherit" 
                variant="outlined" 
                onClick={handleLogout}
                sx={{ borderColor: 'inherit' }}
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button 
                color="inherit" 
                onClick={() => navigate('/login')}
              >
                Login
              </Button>
              <Button 
                variant="contained" 
                color="secondary"
                onClick={() => navigate('/login')}
                sx={{ color: 'common.white' }}
              >
                Get Started
              </Button>
            </>
          )}
        </Stack>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;