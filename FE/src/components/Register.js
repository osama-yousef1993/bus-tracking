import React, { useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import aauLogo from '../aaulogo.png';
import { 
  TextField, 
  Typography, 
  InputAdornment, 
  IconButton, 
  Box, 
  Paper, 
  Link 
} from '@mui/material';
import { 
  Person as PersonIcon, 
  Lock as LockIcon, 
  Email as EmailIcon,
  Visibility, 
  VisibilityOff,
  Menu as MenuIcon,
  Translate as TranslateIcon,
  ArrowForward as ArrowForwardIcon
} from '@mui/icons-material';

const Register = () => {
  const [showPassword, setShowPassword] = useState(false);
  const brandBlue = '#2154be';

  const fieldStyle = {
    '& .MuiOutlinedInput-root': {
      borderRadius: '50px',
      backgroundColor: '#f1f1f1',
      height: '55px',
      '& fieldset': { borderColor: 'transparent' },
      '&:hover fieldset': { borderColor: '#d1d1d1' },
      '&.Mui-focused fieldset': { borderColor: brandBlue },
    },
    marginBottom: 2
  };

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      width: '100vw',
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: '#ffffff',
      overflowX: 'hidden'
    }}>
      
      {/* TOP WHITE SECTION */}
      <Box sx={{ flex: '0 0 45vh', p: 2, display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <IconButton><MenuIcon sx={{ color: brandBlue }} /></IconButton>
          <IconButton><TranslateIcon sx={{ color: brandBlue }} /></IconButton>
        </Box>
        
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <img src={aauLogo} alt="AAU Logo" style={{ height: '80px', marginBottom: '8px' }} />
          <Typography variant="subtitle1" sx={{ color: brandBlue, fontWeight: 'bold', fontSize: '1.1rem' }}>
            Al-Ahliyya Amman University
          </Typography>
        </Box>
      </Box>

      {/* BOTTOM BLUE SECTION */}
      <Box sx={{ 
        flex: '1', 
        backgroundColor: brandBlue, 
        position: 'relative', 
        display: 'flex', 
        justifyContent: 'center'
      }}>
        
        {/* REGISTRATION CARD */}
        <Paper elevation={0} sx={{ 
          width: '90%', 
          maxWidth: '450px', 
          p: 4, 
          pt: 5,
          borderRadius: '30px', 
          position: 'absolute',
          top: '-120px', // Matches the Login page overlap
          textAlign: 'center',
          backgroundColor: '#ffffff',
          border: '1px solid #e0e0e0',
          boxShadow: '0px 10px 30px rgba(0,0,0,0.1)'
        }}>
          <Typography variant="h5" sx={{ color: brandBlue, fontWeight: 'bold', mb: 3 }}>
            Register
          </Typography>

          <TextField
            fullWidth
            placeholder="Username"
            autoComplete="off"
            sx={fieldStyle}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <PersonIcon sx={{ color: brandBlue }} />
                </InputAdornment>
              ),
            }}
          />

          <TextField
            fullWidth
            type={showPassword ? 'text' : 'password'}
            placeholder="Password"
            autoComplete="new-password" // Fixes the default value issue
            sx={fieldStyle}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <LockIcon sx={{ color: brandBlue }} />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                    {showPassword ? <VisibilityOff /> : <Visibility sx={{ color: brandBlue }} />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <TextField
            fullWidth
            placeholder="University Email"
            autoComplete="off"
            sx={fieldStyle}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <EmailIcon sx={{ color: brandBlue }} />
                </InputAdornment>
              ),
            }}
          />

          <Box sx={{ textAlign: 'right', mb: 2, px: 1 }}>
            <Link 
              component={RouterLink} 
              to="/login" 
              sx={{ fontSize: '0.85rem', color: brandBlue, textDecoration: 'none', fontWeight: 600 }}
            >
              Already Have An Account? Login
            </Link>
          </Box>

          {/* CIRCULAR REGISTER BUTTON */}
          <IconButton 
            sx={{ 
              position: 'absolute', 
              bottom: '-40px', 
              left: '50%', 
              transform: 'translateX(-50%)',
              backgroundColor: 'white',
              border: `5px solid white`, 
              outline: `3px solid white`, 
              width: '80px',
              height: '80px',
              boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
              '&:hover': { backgroundColor: '#f0f0f0' },
              zIndex: 2
            }}
          >
            <Box sx={{ 
              width: '100%', 
              height: '100%', 
              borderRadius: '50%', 
              border: `2px solid ${brandBlue}`, 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center' 
            }}>
              <ArrowForwardIcon sx={{ color: brandBlue, fontSize: '40px' }} />
            </Box>
          </IconButton>
        </Paper>
      </Box>
    </Box>
  );
};

export default Register;