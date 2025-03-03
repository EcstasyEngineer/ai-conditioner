import React, { useState } from 'react';
import { Box, Typography, List, ListItem, Slider, TextField, Button } from '@mui/material';

// Placeholder theme data:
const availableThemes = ['Relaxation', 'Focus', 'Obedience', 'Deepening'];

const SessionEditor = () => {
  const [selectedThemes, setSelectedThemes] = useState([]);
  const [frequencies, setFrequencies] = useState({});

  const handleAddTheme = (theme) => {
    if (!selectedThemes.includes(theme)) {
      setSelectedThemes([...selectedThemes, theme]);
      setFrequencies({ ...frequencies, [theme]: 50 });
    }
  };

  const handleFreqChange = (theme, newValue) => {
    setFrequencies({ ...frequencies, [theme]: newValue });
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <Box sx={{ width: '50%' }}>
        <Typography variant="h6">Session Editor</Typography>
        <List>
          {selectedThemes.map((theme) => (
            <ListItem key={theme}>
              <Typography>{theme}</Typography>
              <Slider
                value={frequencies[theme]}
                onChange={(e, val) => handleFreqChange(theme, val)}
                sx={{ ml:2, width:200 }}
              />
            </ListItem>
          ))}
        </List>
        <Button variant="contained" sx={{ mt:2 }}>Save Session</Button>
      </Box>
      <Box sx={{ width: '50%', pl:3 }}>
        <Typography variant="h6">Theme Picker</Typography>
        {availableThemes.map((t) => (
          <Button key={t} onClick={() => handleAddTheme(t)} sx={{mr:1, mt:1}}>
            {t}
          </Button>
        ))}
      </Box>
    </Box>
  );
};

export default SessionEditor;
