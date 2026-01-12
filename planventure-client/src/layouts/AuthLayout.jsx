import { Box, Container } from '@mui/material';
import Navbar from '../components/navigation/Navbar';
import Footer from '../components/navigation/Footer';

const AuthLayout = ({
  children,
  maxWidth = 'xs',
  showFooter = true,
  containerSx = {},
  cardSx = {},
}) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: 'background.default' }}>
      <Navbar />
      <Container
        component="main"
        maxWidth={maxWidth}
        sx={[
          {
            flexGrow: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            mt: 8,
            mb: 10,
            px: { xs: 2, sm: 3 },
          },
          containerSx,
        ]}
      >
        <Box
          sx={[
            {
              width: '100%',
              bgcolor: 'background.paper',
              p: 4,
              borderRadius: 2,
              boxShadow: 1,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 2,
            },
            cardSx,
          ]}
        >
          {children}
        </Box>
      </Container>
      {showFooter && <Footer />}
    </Box>
  );
};

export default AuthLayout;