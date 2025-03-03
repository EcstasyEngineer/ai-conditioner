import React, { useState, useEffect } from 'react';
import { Box, Drawer, List, ListItem, ListItemButton, Typography, Button } from '@mui/material';
import SessionList from './SessionList';
import SessionEditor from './SessionEditor';
import apiClient from '../api/apiClient';
import { useNavigate } from 'react-router-dom';

const MainDashboard = () => {
  const [activeTab, setActiveTab] = useState('default');
  const [defaultSessions, setDefaultSessions] = useState([]);
  const [mySessions, setMySessions] = useState([]);
  const [showEditor, setShowEditor] = useState(false);

  const navigate = useNavigate();

  const loadDefaultSessions = async () => {
    try {
      const data = await apiClient.get('/api/sessions/default');
      setDefaultSessions(data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadMySessions = async () => {
    try {
      const data = await apiClient.get('/api/sessions/my');
      setMySessions(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (activeTab === 'default') loadDefaultSessions();
    if (activeTab === 'my') loadMySessions();
  }, [activeTab]);

  const leftDrawer = (
    <Drawer variant="permanent" anchor="left">
      <List>
        <ListItem disablePadding>
          <ListItemButton onClick={() => setActiveTab('default')}>
            Default Sessions
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton onClick={() => setActiveTab('my')}>
            My Sessions
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton onClick={() => setActiveTab('create')}>
            Create Session
          </ListItemButton>
        </ListItem>
      </List>
    </Drawer>
  );

  let mainContent;
  if (activeTab === 'default') {
    mainContent = <SessionList sessions={defaultSessions} />;
  } else if (activeTab === 'my') {
    mainContent = (
      <Box>
        <SessionList sessions={mySessions} />
        <Button variant="outlined" onClick={() => setShowEditor(true)} sx={{ mt:2 }}>Edit</Button>
        {showEditor && <SessionEditor />}
      </Box>
    );
  } else if (activeTab === 'create') {
    mainContent = <SessionEditor />;
  }

  return (
    <Box sx={{ display: 'flex' }}>
      {leftDrawer}
      <Box sx={{ flexGrow: 1, p: 3, ml: '240px' }}>
        <Typography variant="h5" mb={2}>Dashboard</Typography>
        {mainContent}
      </Box>
    </Box>
  );
};

export default MainDashboard;
