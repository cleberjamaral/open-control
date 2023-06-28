import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function CredentialsList() {
  const [credentials, setCredentials] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCredentials();
  }, []);

  const fetchCredentials = async () => {
    try {
      const response = await axios.get('http://191.36.9.231:5000/api/credentials');
      setCredentials(response.data.credentials);
    } catch (error) {
      console.error(error);
    }
  };

  const handleEdit = (credential) => {
    // Implement your edit logic here
    console.log(`Edit clicked for credential: ${credential.credential}`);
    navigate('/enrollment', { state: { credential } });
  };

  const handleDelete = async (credential) => {
    try {
      await axios.delete(`http://191.36.9.231:5000/api/credentials/${credential}`);
      fetchCredentials();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container">
      <h2 className="mt-4 mb-4">Credentials List</h2>
      {credentials.length === 0 ? (
        <div className="alert alert-info" role="alert">
          No credentials found.
        </div>
      ) : (
        <table className="table table-striped table-bordered">
          <thead className="table-dark" >
            <tr>
              <th scope="col">Registration Number</th>
              <th scope="col">User Name</th>
              <th scope="col">Credential</th>
              <th scope="col" className="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            {credentials.map((credential, index) => (
              <tr key={index}>
                <td>{credential.registration_number}</td>
                <td>{credential.user_name}</td>
                <td>{credential.credential}</td>
                <td className="d-flex justify-content-center align-items-center">
                  <button className="btn btn-primary btn-sm me-2" onClick={() => handleEdit(credential)}>
                    Edit
                  </button>
                  <button className="btn btn-danger btn-sm" onClick={() => handleDelete(credential.credential)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default CredentialsList;