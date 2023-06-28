import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CredentialEnrollment(props) {
  const [credential, setCredential] = useState('');
  const [registrationNumber, setRegistrationNumber] = useState('');
  const [userName, setUserName] = useState('');

  useEffect(() => {
    if (props.location.state && props.location.state.credential) {
      const { credential, registration_number, user_name } = props.location.state.credential;
      setCredential(credential);
      setRegistrationNumber(registration_number);
      setUserName(user_name);
    }
  }, [props.location.state]);

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
      await axios.post('http://191.36.9.231:5000/api/credentials', data);
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
        <button type="submit" className="btn btn-primary">Enroll Credential</button>
      </form>
    </div>
  );
}

export default CredentialEnrollment;