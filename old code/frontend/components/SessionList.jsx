import React from 'react';
import { List, ListItem, ListItemText } from '@mui/material';

const SessionList = ({ sessions }) => {
  if (!sessions || sessions.length === 0) {
    return <div>No sessions available</div>;
  }

  return (
    <List>
      {sessions.map((s) => (
        <ListItem key={s.session_id || s.title} divider>
          <ListItemText
            primary={s.title}
            secondary={`Duration: ${s.duration_min || 'N/A'} - ${s.duration_max || 'N/A'} | Themes: ${s.themes ? s.themes.join(', ') : ''}`}
          />
        </ListItem>
      ))}
    </List>
  );
};

export default SessionList;
