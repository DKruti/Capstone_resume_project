

// App.js latest modification

import './styles.css';
import React, { useState } from 'react';

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [pdfInformation, setPdfInformation] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (selectedFile) {
      // Simulate storing PDF information in temporary memory
      const uploadedPdfInfo = {
        name: selectedFile.name,
        size: selectedFile.size,
        type: selectedFile.type,
      };
      setPdfInformation(uploadedPdfInfo);

      // Log the information to the console
      console.log('Uploaded PDF Information:', uploadedPdfInfo);
    }
  };

  return (
    <div className="container">
      <div className="text-center">
        <h1>Resume Analysis and Job Recommendation System</h1>
        <div className="menu">
          <a href="#">Upload</a>
          <a href="#">Job Recommendation</a>
          <a href="#">Resume Analysis</a>
        </div>
      </div>
      <div className="upload-container">
        <label htmlFor="fileInput" className="label">
          Browse PDF file:
        </label>
        <input
          type="file"
          id="fileInput"
          className="file-input"
          onChange={handleFileChange}
        />
        <button className="browse-btn" onClick={() => document.getElementById('fileInput').click()}>
          Browse
        </button>
        <button className="upload-btn" onClick={handleUpload}>
          Upload
        </button>
        {pdfInformation && (
          <div className="mt-2">
            <h3>Uploaded PDF Information:</h3>
            <p>Name: {pdfInformation.name}</p>
            <p>Size: {pdfInformation.size} bytes</p>
            <p>Type: {pdfInformation.type}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;


// App.js 1 trial 

/*import './styles.css';
import React, { useState } from 'react';

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = () => {
    console.log(selectedFile.name);
  };

  return (
    <div className="container">
      <div className="text-center">
        <h1>Resume Analysis and Job Recommendation System</h1>
        <div className="menu">
          <a href="#">Upload</a>
          <a href="#">Job Recommendation</a>
          <a href="#">Resume Analysis</a>
        </div>
      </div>
      <div className="upload-container">
        <label htmlFor="fileInput" className="label">
          Browse PDF file:
        </label>
        <input
          type="file"
          id="fileInput"
          className="file-input"
          onChange={handleFileChange}
        />
        <button className="browse-btn" onClick={() => document.getElementById('fileInput').click()}>
          Browse
        </button>
        <button className="upload-btn" onClick={handleUpload}>
          Upload
        </button>
        {selectedFile && (
          <input type="text" value={selectedFile.name} readOnly className="form-control mt-2" />
        )}
      </div>
    </div>
  );
};

export default App;*/

