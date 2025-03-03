import React, { useState, useEffect } from 'react';
import { Box, Typography, TextField, Button, Drawer, RadioGroup, FormControlLabel, Radio, FormControl, FormLabel } from '@mui/material';
import apiClient from '../api/apiClient';

// Placeholder line data:
const initialLines = [
  { text: "I am relaxed.", dom: null, dif: "basic", sub: null, tts: "salli" },
  { text: "Serve your Mistress.", dom: "mistress", dif: "light", sub: null, tts: "salli" },
];

const domOptions = ["master", "mistress", "daddy", "goddess"];
const difOptions = ["basic", "light", "moderate", "deep", "extreme"];
const subOptions = ["puppet", "bambi", "doll"];
const ttsOptions = ["salli", "ivy"]; // but greyed out, default salli

const LineCollectionEditor = () => {
  const [title, setTitle] = useState("My Theme");
  const [description, setDescription] = useState("Description of this line collection.");
  const [lines, setLines] = useState(initialLines);
  const [selectedLineIndex, setSelectedLineIndex] = useState(null);
  const [domVal, setDomVal] = useState(null);
  const [difVal, setDifVal] = useState(null);
  const [subVal, setSubVal] = useState(null);

  useEffect(() => {
    if (selectedLineIndex !== null) {
      const line = lines[selectedLineIndex];
      setDomVal(line.dom);
      setDifVal(line.dif);
      setSubVal(line.sub);
    }
  }, [selectedLineIndex]);

  const handleLineClick = (index) => {
    setSelectedLineIndex(index);
  };

  const handleUpdateLineTags = () => {
    const updated = [...lines];
    updated[selectedLineIndex] = {
      ...updated[selectedLineIndex],
      dom: domVal,
      dif: difVal,
      sub: subVal
    };
    setLines(updated);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', p:3 }}>
      <Typography variant="h4" mb={2}>Line Collection Editor</Typography>
      <Box sx={{ display: 'flex', alignItems: 'center', gap:2, mb:2 }}>
        <TextField
          label="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <TextField
          label="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          sx={{ width: 300 }}
        />
        <Button variant="contained">Generate Lines</Button>
      </Box>
      <Box sx={{ display: 'flex' }}>
        <Box sx={{ width: '50%' }}>
          <Typography variant="h6">Lines</Typography>
          {lines.map((line, index) => (
            <Box
              key={index}
              sx={{
                border: '1px solid #ccc', 
                p:1, 
                mb:1, 
                cursor:'pointer',
                backgroundColor: selectedLineIndex === index ? '#eef' : '#fff'
              }}
              onClick={() => handleLineClick(index)}
            >
              {line.text}
            </Box>
          ))}
        </Box>
        <Box sx={{ width: '50%', pl:3 }}>
          <Typography variant="h6">Line Details</Typography>
          {selectedLineIndex !== null ? (
            <Box>
              <FormControl component="fieldset" sx={{ mt:2 }}>
                <FormLabel>Dom</FormLabel>
                <RadioGroup
                  value={domVal || ''}
                  onChange={(e) => setDomVal(e.target.value)}
                >
                  {domOptions.map(opt => <FormControlLabel key={opt} value={opt} control={<Radio />} label={opt} />)}
                  <FormControlLabel value="" control={<Radio />} label="None" />
                </RadioGroup>
              </FormControl>

              <FormControl component="fieldset" sx={{ mt:2 }}>
                <FormLabel>Difficulty</FormLabel>
                <RadioGroup
                  value={difVal || ''}
                  onChange={(e) => setDifVal(e.target.value)}
                >
                  {difOptions.map(opt => <FormControlLabel key={opt} value={opt} control={<Radio />} label={opt} />)}
                </RadioGroup>
              </FormControl>

              <FormControl component="fieldset" sx={{ mt:2 }}>
                <FormLabel>Subject</FormLabel>
                <RadioGroup
                  value={subVal || ''}
                  onChange={(e) => setSubVal(e.target.value)}
                >
                  {subOptions.map(opt => <FormControlLabel key={opt} value={opt} control={<Radio />} label={opt} />)}
                  <FormControlLabel value="" control={<Radio />} label="None" />
                </RadioGroup>
              </FormControl>

              <Box sx={{ mt:2 }}>
                <Typography variant="subtitle1">Tags (greyed out, unselectable)</Typography>
                <Typography variant="body2" color="text.secondary">Will mirror title later</Typography>
              </Box>

              <Box sx={{ mt:2 }}>
                <Typography variant="subtitle1">TTS Service (greyed out, default salli)</Typography>
                <Typography variant="body2" color="text.secondary">Current: salli</Typography>
              </Box>

              <Button variant="contained" sx={{ mt:2 }} onClick={handleUpdateLineTags}>Update Line</Button>
            </Box>
          ) : (
            <Typography>Select a line to edit</Typography>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default LineCollectionEditor;
