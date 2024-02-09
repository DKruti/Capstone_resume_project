import React, { useState } from "react"



const FileUploader = () => {

    const [file, setFile] = useState(null)
    const [data_resume, setDataResume] = useState("")

    const onFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const onFileUpload = async () => {
        if (!file) {
            alert("Please Upload your Resume");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        const url = "http://127.0.0.1:8000/resume_process/";

        try {
            const response = await fetch(url, {
                method : "POST",
                body : formData, 
            });

            if (response.ok) {
                const data = await response.json();
                console.log("File uploaded and sent to backend successfully")
                console.log(data)
                setDataResume(data.parsed_resume);
            } else {
                console.error("File upload failed to backend")
            }
        } catch (error){
            console.error("error during the uploading process ")
        }
    };


    return (
        <div className="file-uploader">
            <input type="file" onChange={onFileChange}/>
            <button onClick={onFileUpload}>Upload</button>
            {data_resume && <div className="resume-text">{data_resume}</div>} {/* Conditional rendering */}
        </div>
    );
};

export default FileUploader;