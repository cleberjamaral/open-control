import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [credential, setCredential] = useState('');

  const handleInputChange = (e) => {
    setCredential(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/credentials', { credential });
      setCredential('');
      alert('Credential enrolled successfully!');
    } catch (error) {
      console.error(error);
      alert('Error enrolling credential!');
    }
  };

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Credential Enrollment</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Credential:</label>
          <input
            type="text"
            className="form-control"
            value={credential}
            onChange={handleInputChange}
          />
        </div>
        <button type="submit" className="btn btn-primary">Enroll Credential</button>
      </form>
    </div>
  );
}

export default App;