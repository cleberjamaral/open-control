import React, { useEffect, useState } from 'react';
import axios from 'axios';

function EventsList() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await axios.get('http://191.36.9.231:5000/api/events');
      setEvents(response.data.events);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container">
      <h2 className="mt-4 mb-4">Events List</h2>
      {events.length === 0 ? (
        <div className="alert alert-info" role="alert">
          No events found.
        </div>
      ) : (
        <table className="table table-striped table-bordered">
          <thead className="table-dark" >
            <tr>
              <th scope="col">Datetime</th>
              <th scope="col" className="text-center">Credential</th>
              <th scope="col" className="col-lg-4">User Name</th>
              <th scope="col" className="text-center">Event Type</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event, index) => (
              <tr key={index}>
                <td>{event.date}</td>
                <td className="text-center">{event.credential}</td>
                <td className="col-lg-4">{event.user_name}</td>
                <td className="col-lg-4">{event.event_type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default EventsList;