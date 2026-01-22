import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import aauLogo from '../aaulogo.png';
import { 
  Box, Typography, IconButton, Paper, Button, Stack, Menu, MenuItem 
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  Translate as TranslateIcon, 
  DirectionsBus as BusIcon, 
  KeyboardArrowDown as ArrowDownIcon,
  SmartToy as BotIcon 
} from '@mui/icons-material';

const HomePage = () => {
  const navigate = useNavigate();
  const brandBlue = '#2154be';

  // State for Dropdowns
  const [timeAnchor, setTimeAnchor] = useState(null);
  const [locationAnchor, setLocationAnchor] = useState(null);

  // Handlers for Time Menu
  const handleTimeClick = (event) => setTimeAnchor(event.currentTarget);
  const handleTimeClose = () => setTimeAnchor(null);

  // Handlers for Location Menu
  const handleLocationClick = (event) => setLocationAnchor(event.currentTarget);
  const handleLocationClose = () => setLocationAnchor(null);

  const scheduleData = [
    { location: 'Abdoun', time: '7:30am-8:30am' },
    { location: 'Abdoun', time: '8:00am-9:00am' },
    { location: 'Abdoun', time: '9:00am-10:00am' },
    { location: 'Abdoun', time: '10:00am-11:00am' },
  ];

  return (
    <Box sx={{ minHeight: '100vh', width: '100vw', display: 'flex', flexDirection: 'column', backgroundColor: '#ffffff', overflowX: 'hidden' }}>
      
      {/* HEADER SECTION */}
      <Box sx={{ p: 1, display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
          <IconButton onClick={() => navigate(-1)} size="small" sx={{ p: 1 }}>
            <MenuIcon sx={{ color: brandBlue, fontSize: '1.8rem' }} />
          </IconButton>
          <IconButton size="small" sx={{ p: 1 }}>
            <TranslateIcon sx={{ color: brandBlue, fontSize: '1.5rem' }} />
          </IconButton>
        </Box>
        
        <Box sx={{ textAlign: 'center', mt: 0.5 }}>
          <img src={aauLogo} alt="AAU Logo" style={{ height: '60px', marginBottom: '4px' }} />
          <Typography variant="subtitle1" sx={{ color: brandBlue, fontWeight: 'bold', fontSize: '1rem' }}>
            Al-Ahliyya Amman University
          </Typography>
        </Box>
      </Box>

      {/* CENTERED CONTENT AREA */}
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', mt: 4 }}>
        <Box sx={{ width: '100%', maxWidth: '480px', px: 3 }}>
          
          {/* Filters Row */}
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 4, gap: 2 }}>
            <BusIcon sx={{ fontSize: 45, color: brandBlue }} />
            
            {/* TIME DROPDOWN */}
            <Button 
              variant="contained" 
              onClick={handleTimeClick}
              endIcon={<ArrowDownIcon />}
              sx={{ 
                borderRadius: '20px', bgcolor: '#fce4ec', color: brandBlue, boxShadow: 'none', 
                textTransform: 'none', fontWeight: 'bold', px: 2, fontSize: '0.8rem',
                '&:hover': { bgcolor: '#f8bbd0', boxShadow: 'none' }
              }}
            >
              Time
            </Button>
            <Menu anchorEl={timeAnchor} open={Boolean(timeAnchor)} onClose={handleTimeClose}>
              <MenuItem onClick={handleTimeClose}>Morning (8:00 AM)</MenuItem>
              <MenuItem onClick={handleTimeClose}>Noon (12:10 PM)</MenuItem>
              <MenuItem onClick={handleTimeClose}>Evening (3:15 PM)</MenuItem>
            </Menu>

            {/* LOCATION DROPDOWN */}
            <Button 
              variant="contained" 
              onClick={handleLocationClick}
              endIcon={<ArrowDownIcon />}
              sx={{ 
                borderRadius: '20px', bgcolor: '#fce4ec', color: brandBlue, boxShadow: 'none', 
                textTransform: 'none', fontWeight: 'bold', px: 2, fontSize: '0.8rem',
                '&:hover': { bgcolor: '#f8bbd0', boxShadow: 'none' }
              }}
            >
              Location
            </Button>
            <Menu anchorEl={locationAnchor} open={Boolean(locationAnchor)} onClose={handleLocationClose}>
              <MenuItem onClick={handleLocationClose}>Abdoun</MenuItem>
              <MenuItem onClick={handleLocationClose}>Khalda</MenuItem>
              <MenuItem onClick={handleLocationClose}>Seventh Circle</MenuItem>
              <MenuItem onClick={handleLocationClose}>University Campus</MenuItem>
            </Menu>
          </Box>

          {/* Schedule List */}
          <Stack spacing={2}>
            {scheduleData.map((item, index) => (
              <Paper key={index} elevation={0} sx={{ p: 1.8, display: 'flex', justifyContent: 'space-between', alignItems: 'center', bgcolor: '#f5f5f5', borderRadius: '15px', px: 4 }}>
                <Typography sx={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{item.location}</Typography>
                <Typography sx={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{item.time}</Typography>
              </Paper>
            ))}
          </Stack>
        </Box>
      </Box>

      {/* CHATBOT ICON */}
      <Box sx={{ position: 'fixed', bottom: 20, right: 20 }}>
        <IconButton sx={{ color: brandBlue }}>
          <BotIcon sx={{ fontSize: 40 }} />
        </IconButton>
      </Box>
    </Box>
  );
};

export default HomePage;