import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import CredentialEnrollment from './components/CredentialEnrollment';
import CredentialsList from './components/CredentialsList';

function App() {
  return (
    <Router>
      <div className="container mt-5">
        <h1 className="mb-4">Credential Management</h1>
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link to="/" className="nav-link">Enroll Credential</Link>
            </li>
            <li className="nav-item">
              <Link to="/list" className="nav-link">Credentials List</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route exact path="/" element={<CredentialEnrollment />} ></Route>
          <Route path="/list" element={<CredentialsList />}></Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;