import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';


function CredentialEnrollment(props) {
  const [credential, setCredential] = useState('');
  const [registrationNumber, setRegistrationNumber] = useState('');
  const [userName, setUserName] = useState('');
  const location = useLocation();
  const navigate = useNavigate();


  useEffect(() => {
    if (location.state && location.state.credential) {
      const { credential, registration_number, user_name } = location.state.credential;
      setCredential(credential);
      setRegistrationNumber(registration_number);
      setUserName(user_name);
    }
  }, [location.state]);

  const isEditMode = !!location.state && !!location.state.credential;

  const handleCredentialChange = (e) => {
    setCredential(e.target.value);
  };

  const handleRegistrationNumberChange = (e) => {
    setRegistrationNumber(e.target.value);
  };

  const handleUserNameChange = (e) => {
    setUserName(e.target.value);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        credential: credential,
        registrationNumber: registrationNumber,
        userName: userName
      };
      if (isEditMode) {
        // Update existing credential
        await axios.put(`http://191.36.9.231:5000/api/credentials/${location.state.credential.credential}`, data);

      } else {
        // Add new credential
        await axios.post('http://191.36.9.231:5000/api/credentials', data);
      }
      navigate('/');

      setCredential('');
      setRegistrationNumber('');
      setUserName('');
      alert('Credential enrolled successfully!');
    } catch (error) {
      console.error(error);
      alert('Error enrolling credential!');
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">Credential Enrollment</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Registration Number:</label>
          <input
            type="text"
            className="form-control"
            value={registrationNumber}
            onChange={handleRegistrationNumberChange}
          />
        </div>
        <div className="mb-3">
          <label className="form-label">User Name:</label>
          <input
            type="text"
            className="form-control"
            value={userName}
            onChange={handleUserNameChange}
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Credential:</label>
          <input
            type="text"
            className="form-control"
            value={credential}
            onChange={handleCredentialChange}
          />
        </div>
        <button type="submit" className="btn btn-primary">{isEditMode ? 'Update' : 'Add'} Credential</button>
      </form>
    </div>
  );
}

export default CredentialEnrollment;