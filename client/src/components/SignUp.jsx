
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; 
import { Grid, Typography, TextField, Button, IconButton, Box, InputAdornment, Snackbar } from '@mui/material';
import { ArrowBack as ArrowBackIcon, Visibility, VisibilityOff } from '@mui/icons-material';
import emailIcon from './Assets/email-icn.svg';
import image from './Assets/home.png';

const styles = {
  signUpOption: {display: "flex",alignItems: 'center',padding: "15px",width: '250px',boxShadow: 'rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px',cursor: "pointer"},
  signUpImage: { width: '100%', height: 'auto', borderRadius: '8px' },
  container: { minHeight: '100vh', backgroundColor: 'white' },
  backButton: { marginBottom: '1rem' },
  formContainer: { padding: 4, width: '100%', bgcolor: 'background.paper', borderRadius: '8px' },
  signUpWrapper: { marginTop: '20px', textAlign: 'center' }, 
};

const SignUp = () => {
  const navigate = useNavigate(); 
  const [showSignInForm, setShowSignInForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    role: '',
    phone_number: '',
    password: '',
    repeatPassword: '',
    showPassword: false,
    showRepeatPassword: false,
  });
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [formErrors, setFormErrors] = useState({
    name: false,
    email: false,
    role: false,
    phone_number: false,
    password: false,
    repeatPassword: false,
  });

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (formErrors[e.target.name]) {
      setFormErrors({ ...formErrors, [e.target.name]: false });
    }
  };

  const handleShowPassword = () => {
    setFormData({ ...formData, showPassword: !formData.showPassword });
  };

  const handleShowRepeatPassword = () => {
    setFormData({ ...formData, showRepeatPassword: !formData.showRepeatPassword });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (formData.password !== formData.repeatPassword) {
      setErrorMessage("Passwords do not match!");
      setFormErrors({ ...formErrors, password: true, repeatPassword: true });
      return;
    }
  
    const requiredFields = ['name', 'email', 'role', 'phone_number', 'password', 'repeatPassword'];
    let hasError = false;
    const newFormErrors = { ...formErrors };
  
    requiredFields.forEach(field => {
      if (!formData[field]) {
        newFormErrors[field] = true;
        hasError = true;
      } else {
        newFormErrors[field] = false;
      }
    });
  
    setFormErrors(newFormErrors);
  
    if (hasError) {
      setErrorMessage('Please fill out all required fields.');
      return;
    }
  
    const user = {
      name: formData.name,
      password: formData.password,
      role: formData.role,
      email: formData.email,
      phone_number: formData.phone_number
    };
  
    try {
      const response = await fetch('http://127.0.0.1:5000/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
      });
    
      if (response.ok) {
        const result = await response.json();
        localStorage.setItem('access_token', result.access_token);
        setSuccessMessage('User signed up successfully!');
        handleClose(); 
        navigate('/login', { replace: true });
      } else if (response.status === 409) {
        setErrorMessage('Email already exists. Please use a different email.');
      } else {
        throw new Error(`Sign up failed: ${response.statusText}`);
      }
    } catch (error) {
      setErrorMessage(`Error: ${error.message}`);
    }    
  };

  const handleSnackbarClose = () => {
    setSuccessMessage('');
    setErrorMessage('');
  };

  const handleOpen = () => {
    setShowSignInForm(true);
  };

  const handleClose = () => {
    setShowSignInForm(false);
  };

  return (
    <Grid container justifyContent="center" alignItems="center" sx={styles.container}>
      <Grid item xs={12} sm={6}>
        <img src={image} alt="Auth" style={styles.signUpImage} />
      </Grid>
      <Grid item xs={12} sm={6} container justifyContent="center" alignItems="center">
        <div style={styles.signUpWrapper}>
          <Typography variant="h5" style={{ marginBottom: '20px' }}>Let's sign you up</Typography>
          {showSignInForm ? (
            <Box sx={styles.formContainer}>
              <IconButton onClick={handleClose} style={styles.backButton}>
                <ArrowBackIcon />
              </IconButton>
              <Typography variant="h4">Sign Up</Typography>
              <form onSubmit={handleSubmit}>
                <TextField label="Full Name" variant="outlined" fullWidth margin="normal" name="name" value={formData.name} onChange={handleInputChange} required error={formErrors.name}/>
                <TextField label="Email" variant="outlined" fullWidth margin="normal" name="email" value={formData.email} onChange={handleInputChange} required error={formErrors.email}/>
                <TextField label="Role" variant="outlined" fullWidth margin="normal" name="role" value={formData.role} onChange={handleInputChange} required error={formErrors.role}/>
                <TextField label="Phone" variant="outlined" type="tel" fullWidth margin="normal" name="phone_number" value={formData.phone_number} onChange={handleInputChange} required error={formErrors.phone_number}/>
                <TextField label="Password" type={formData.showPassword ? 'text' : 'password'} variant="outlined" fullWidth margin="normal" name="password" value={formData.password} onChange={handleInputChange} required error={formErrors.password}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle password visibility"
                          onClick={handleShowPassword}
                          edge="end"
                        >
                          {formData.showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField label="Repeat Password" type={formData.showRepeatPassword ? 'text' : 'password'} variant="outlined" fullWidth margin="normal" name="repeatPassword" value={formData.repeatPassword} onChange={handleInputChange} required error={formErrors.repeatPassword}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle repeat password visibility"
                          onClick={handleShowRepeatPassword}
                          edge="end"
                        >
                          {formData.showRepeatPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
                <Button type="submit" variant="contained" color="primary" fullWidth style={{ marginTop: '1rem' }}>
                  Sign Up
                </Button>
              </form>
            </Box>
          ) : (
            <div onClick={handleOpen} style={styles.signUpOption}>
              <img src={emailIcon} height={"30px"} alt="Email Icon" />
              <Typography style={{ color: '#032541', marginLeft: '10px' }}>Sign up with email</Typography>
            </div>
          )}
          <Snackbar
            open={!!successMessage || !!errorMessage}
            autoHideDuration={6000}
            onClose={handleSnackbarClose}
            message={successMessage || errorMessage}
            anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            ContentProps={{
              style: {
                backgroundColor: errorMessage ? '#4CAF50' : '#4CAF50',
                color: 'white'
              },
            }}
          />
        </div>
      </Grid>
    </Grid>
  );
};

export default SignUp;