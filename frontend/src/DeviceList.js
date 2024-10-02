import React, { useState, useEffect } from 'react';

const DeviceList = () => {
  // State to store the fetched data
  const [devices, setDevices] = useState([]);

  // Fetch data from Django API when the component is mounted
  useEffect(() => {
    fetch('http://localhost:8000/device/divlist')
      .then((response) => response.json())
      .then((data) => setDevices(data))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h1>Device List</h1>
      {/* Display fetched data */}
      <ul>
        {devices.map((device) => (
          <li key={device.laptop_id}>
            {device.Brand} - {device.laptop_id} {/* Adjusted to show laptop_id as well */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DeviceList;