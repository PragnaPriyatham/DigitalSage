// DeviceHomePage.tsx
import React from 'react';
import { motion } from 'framer-motion';

const devices = [
  {
    id: 1,
    name: 'Device 1',
    description: 'A powerful device for all your needs.',
    price: '$500',
    imageUrl: 'https://via.placeholder.com/150',
  },
  {
    id: 2,
    name: 'Device 2',
    description: 'The next-gen device for advanced users.',
    price: '$800',
    imageUrl: 'https://via.placeholder.com/150',
  },
  // Add more devices as needed
];

const DeviceHomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center py-6 mb-10 bg-white shadow-md rounded-lg"
      >
        <h1 className="text-4xl font-bold text-blue-600">Welcome to Device Store</h1>
        <p className="mt-2 text-lg text-gray-600">Explore the latest devices</p>
      </motion.header>

      {/* Device List */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {devices.map((device) => (
          <motion.div
            key={device.id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            whileHover={{ scale: 1.05 }}
            className="bg-white rounded-lg shadow-lg overflow-hidden"
          >
            <img
              src={device.imageUrl}
              alt={device.name}
              className="w-full h-48 object-cover"
            />
            <div className="p-6">
              <h2 className="text-2xl font-semibold text-gray-800">{device.name}</h2>
              <p className="mt-2 text-gray-600">{device.description}</p>
              <p className="mt-4 text-xl font-bold text-blue-600">{device.price}</p>
              <button className="mt-4 w-full py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                View Details
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default DeviceHomePage;
