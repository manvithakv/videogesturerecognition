// App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';
import Headers from './components/Headers';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Otp from './pages/Otp';
import Error from './pages/Error';
import Mediapipe from './pages/Mediapipe';
import Haarcascade from './pages/Haarcascade';
import Opencv from './pages/Opencv';
import Deeplearning from './pages/Home';  // Updated import for Deeplearning
import Deeplearning1 from './pages/Home1';
import Deeplearning2 from './pages/Deep.js';
function App() {
  return (
    <>
      <Headers />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/user/otp" element={<Otp />} />
        <Route path="/mediapipe" element={<Mediapipe />} />
        <Route path="/haarcascade" element={<Haarcascade />} />
        <Route path="/opencv" element={<Opencv />} />
        <Route path="/Home" element={<Deeplearning />} />
        <Route path="/Home1" element={<Deeplearning1 />} />
        <Route path="/Deep" element={<Deeplearning2 />} />
        <Route path="*" element={<Error />} />
      </Routes>
    </>
  );
}

export default App;
