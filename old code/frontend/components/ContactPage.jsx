import React from 'react';
import { Box, Typography } from '@mui/material';

const ContactUsPage = () => {
  return (
    <Box sx={{ p:3 }}>
      <Typography variant="h4" mb={2}>Contact Us</Typography>
      <Typography>For super user access, please contact admin@example.com.</Typography>
    </Box>
  );
};

export default ContactUsPage;
