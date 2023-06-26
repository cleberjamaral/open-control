import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import CredentialEnrollment from './components/CredentialEnrollment';
import CredentialsList from './components/CredentialsList';

function App() {
  const [isMenuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!isMenuOpen);
  };

  return (
    <Router>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <button className="navbar-toggler" type="button" onClick={toggleMenu}>
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className={`collapse navbar-collapse${isMenuOpen ? ' show' : ''}`}>
          <ul className="navbar-nav">
          <li className="nav-item">
              <Link to="/" className="nav-link" onClick={toggleMenu}>
                Credentials List
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/enrollment" className="nav-link" onClick={toggleMenu}>
                Enroll Credential
              </Link>
            </li>
          </ul>
        </div>
      </nav>
      <div className="container mt-4">
      <Routes>
      <Route path="/" element={<CredentialsList />}></Route>
          <Route exact path="/enrollment" element={<CredentialEnrollment />} ></Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;