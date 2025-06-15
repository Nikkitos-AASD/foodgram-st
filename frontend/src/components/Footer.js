import React from 'react';
import { Box, Container, Typography, Link } from '@mui/material';

export const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[200],
      }}
    >
      <Container maxWidth="sm">
        <Typography variant="body1" align="center">
          {'© '}
          <Link color="inherit" href="https://github.com/yourusername/foodgram">
            Foodgram
          </Link>
          {' '}
          {new Date().getFullYear()}
        </Typography>
      </Container>
    </Box>
  );
}; 