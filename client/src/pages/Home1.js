import React, { useState } from "react";
import axios from "axios";

const Home1=()=>{
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState({});
  const [fileName,setFileName]=useState(null)

  const fileSelectedHandler = (event) => {
    setSelectedFile(event.target.files[0]);
    
    console.log(selectedFile)
  };

  const fileUploadHandler = async () => {
    if (!selectedFile) {
      console.error("No file selected.");
      return;
    }
  
    setFileName(selectedFile.name.split('_')[0])

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await axios.post("http://localhost:8091/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(res.data);
    } catch (error) {
      console.log(error);
    }
  };  
  console.log(result.class)

  return (
    <div>
      <div>
        <br/><br/><br/>
        <div className="container d-flex justify-content-center mt-80">
          <div className="row">
            <div className="col-md-12">
              <div className="file-drop-area">
                 <input type="file" className="file-input" onChange={fileSelectedHandler} />
              </div>
            </div>
          </div>
        </div>
        <div className="container d-flex justify-content-center" style={{marginTop:30}}>
          <div className="row">
            <div className="col-md-12">
              <button className="btn btn-dark justify-content-center" onClick={fileUploadHandler}>Upload</button>
            </div>
          </div>
        </div>
        <div className="container d-flex justify-content-center" style={{marginTop:30}}>
        {selectedFile && 
              <table>
                <tr>
                    <td>
                    <img src={URL.createObjectURL(selectedFile)} alt="selected" height={232} width={232} />
                    </td>
                    {result.class && (
                     <>
                    <td>
                      <tr>
                          <td> <b>PREDICTION CLASS:</b> </td>
                          <td> {result.class} </td>
                      </tr>
                      <tr>
                          <td> <b>ACTUAL CLASS :</b> </td>
                          <td>{fileName === null ? "null" : fileName}</td>
                      </tr>
                    </td>
                    </>
                    )}
                </tr>
              </table>
            }
        </div>
    </div>
      </div>
  );
}

export default Home1