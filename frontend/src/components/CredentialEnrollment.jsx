import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [credential, setCredential] = useState('');
  const [registrationNumber, setRegistrationNumber] = useState('');
  const [userName, setUserName] = useState('');

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
      await axios.post('http://localhost:5000/api/credentials', data);
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

export default App;