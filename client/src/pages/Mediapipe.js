import React, { useEffect } from 'react';

const App = () => {
  useEffect(() => {
    // Auto-refresh the video feed every 100 milliseconds
    const refreshVideoFeed = () => {
      const videoFeed = document.getElementById('video_feed_mp');
      if (videoFeed) {
        videoFeed.src = `http://localhost:8000/video_feed_mp?${new Date().getTime()}`;
      }
    };

    const intervalId = setInterval(refreshVideoFeed, 100);

    // Cleanup the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  // Function to stop the Python file
  const stopPythonFile = async () => {
    try {
      // Display a confirmation dialog
      const confirmed = window.confirm('Are you sure you want to stop the Python file?');
      if (!confirmed) {
        return; // Do nothing if the user cancels the operation
      }

      // Send a POST request to the endpoint responsible for stopping the Python file
      const response = await fetch('http://localhost:8000/stop_python_file', {
        method: 'POST',
      });

      if (response.ok) {
        console.log('Python file stopped successfully');
      } else {
        console.error('Failed to stop Python file');
      }
    } catch (error) {
      console.error('Error stopping Python file:', error);
    }
  };

  return (
    <div>
      <h1>Hand Gesture Recognition</h1>
      <img id="video_feed" src="http://localhost:8000/video_feed_mp" alt="Hand Gesture Feed" />

      {/* Button to stop the Python file */}
      <button onClick={stopPythonFile}>Stop Python File</button>
    </div>
  );
};

export default App;