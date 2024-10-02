import React from 'react';
import './index.css'; // Ensure the CSS is imported in App.tsx
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DeviceHomePage from './components/DeviceHomePage'; // Import your home page component

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<DeviceHomePage />} />
                {/* Add more routes here as needed */}
            </Routes>
        </Router>
    );
};

export default App;
