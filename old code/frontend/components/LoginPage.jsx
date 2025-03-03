import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Link } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import apiClient from '../api/apiClient';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogin = async (superUser = false) => {
    try {
      const data = await apiClient.post('/api/login', {
        username,
        password,
        superuser: superUser,
      });
      if (data.success) {
        navigate('/dashboard');
      }
    } catch (err) {
      // If error is 403 and redirect to contact, just navigate:
      if (err.message.includes('403')) {
        navigate('/contact');
      } else {
        alert('Login failed');
      }
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', maxWidth: 300, margin: 'auto', mt:10 }}>
      <Typography variant="h4" mb={2}>Login</Typography>
      <TextField
        label="Username"
        variant="outlined"
        fullWidth
        margin="normal"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <TextField
        label="Password"
        variant="outlined"
        fullWidth
        margin="normal"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button variant="contained" onClick={() => handleLogin(false)} sx={{ mt:2 }}>Login</Button>
      <Link
        href="#"
        underline="hover"
        onClick={(e) => {
          e.preventDefault();
          handleLogin(true);
        }}
        sx={{ mt:2 }}
      >
        Super User Login
      </Link>
    </Box>
  );
};

export default LoginPage;
