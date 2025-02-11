// Dashboard.js
import React, { useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import '../styles/mix.css';

const Dashboard = () => {
  const navigate = useNavigate();

  const userValid = useCallback(() => {
    let token = localStorage.getItem('userdbtoken');
    if (!token) {
      navigate('*');
    }
  }, [navigate]);

  useEffect(() => {
    userValid();
  }, [userValid]);

  return (
    <div className="container">
      <h1>Dashboard</h1>
      <h3>Select an option:</h3>

      <div className="d-grid gap-2 col-2 mx-auto my-5">
        <Link to="/mediapipe">
          <button className="btn btn-primary btn-lg" type="button" style={{ backgroundColor: '#67b9ef' }}>
            MediaPipe
          </button>
        </Link>
        <Link to="/opencv">
          <button className="btn btn-primary btn-lg" type="button" style={{ backgroundColor: '#67b9ef' }}>
            OpenCV
          </button>
        </Link>
        <Link to="/haarcascade">
          <button className="btn btn-primary btn-lg" type="button" style={{ backgroundColor: '#67b9ef' }}>
            Haarcascade
          </button>
        </Link>
        {/* Add the Deep Learning button here */}
        <Link to="/Home"> {/* Assuming "/deep-learning" is your desired route */}
          <button className="btn btn-primary btn-lg" type="button" style={{ backgroundColor: '#67b9ef' }}>
            Deeplearning 
          </button>
        </Link>
        <Link to="/Home1"> {/* Assuming "/deep-learning" is your desired route */}
          <button className="btn btn-primary btn-lg" type="button" style={{ backgroundColor: '#67b9ef' }}>
            Deeplearning 
            Natural
          </button>
          </Link>
          <Link to="/Deep"> {/* Assuming "/deep-learning" is your desired route */}
          <button className="btn btn-primary btn-lg" type="button" style={{ backgroundColor: '#67b9ef' }}>
            Deeplearning 
            Natural1
          </button>
          </Link>
      </div>
    </div>
  );
};

export default Dashboard;
