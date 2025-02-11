

import React, { useState } from "react";
import axios from "axios";

const Deep = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [predictedClass, setPredictedClass] = useState(null);
  const [predictedLabel, setPredictedLabel] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      // Send the file to the server for processing
      const response = await axios.post("http://localhost:8060/predict_video", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setPredictedClass(response.data.max_predicted_class);
      setPredictedLabel(response.data.predicted_label);
    } catch (error) {
      console.error("Error processing video:", error.message);
    }
  };

  return (
    <div>
      <h1>Video Processing </h1>
      <form onSubmit={handleFormSubmit}>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button type="submit">Process Video</button>
      </form>
      {selectedFile && (
        <div>
          <h3>Input Video:</h3>
          <video width="400" controls>
            <source src={URL.createObjectURL(selectedFile)} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
      {predictedClass !== null && (
        <div>
          <h3>Predicted Class:</h3>
          <p>{predictedClass}</p>
          <h3>Predicted Label:</h3>
          <p>{predictedLabel}</p>
        </div>
      )}
    </div>
  );
};

export default Deep;