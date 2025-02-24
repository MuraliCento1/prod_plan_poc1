import React, { useState } from "react";
import axios from "axios";

import "../styles/TemplateAction.css"

const TemplateAction = () => {
  const [file, setFile] = useState(null);
  const [selection, setSelection] = useState("");
  const [isFileUploaded, setIsFileUploaded] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setIsFileUploaded(e.target.files[0] ? true : false);
  };

  const handleSelectionChange = (e) => {
    setSelection(e.target.value);
  };

  const handleUploadSubmit = async (e) => {
    e.preventDefault();

    if (!file || !selection) {
      console.log("Please select a file and a valid dropdown option.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("selection", selection);

    console.log({selection, file});
    // try {
    //   
    // } catch (error) {
    //   console.error("Error uploading file:", error);
    // }
  };

  const handleDownloadSubmit = async (e) => {
    e.preventDefault();

    if (!selection) {
      console.log("Please select a valid dropdown option.");
      return;
    }
    console.log({selection});
    

    // try {
    // } catch (error) {
    //   console.error("Error downloading file:", error);
    // }
  };

  return (
    <div style={{margin: '10px', padding: '10px', width: 'fit-content', border: '1px solid black', borderRadius: '10px'}}>
      <form>
        <div className="dropdown-container">
          <select
            className="dropdown"
            value={selection}
            onChange={handleSelectionChange}
          >
            <option value="">Select option</option>
            <option value="BOM">BOM</option>
            <option value="Production Plan">Production Plan</option>
            <option value="Sku Master">Sku Master</option>
            <option value="Vendor Master">Vendor Master</option>
            <option value="Stock Master">Stock Master</option>
            <option value="Vendor Inwarding Master">
              Vendor Inwarding Master
            </option>
          </select>
        </div>

        <div className="input-group">
          <input
            type="file"
            onChange={handleFileChange}
            className="file-input"
          />
          <button
            type="button"
            className="blue-button"
            onClick={handleUploadSubmit}
            disabled={!selection || !file}
          >
            Upload
          </button>
        </div>

        <button
          type="button"
          className="blue-button"
          onClick={handleDownloadSubmit}
          disabled={!selection}
        >
          Download
        </button>
      </form>
    </div>
  );
};

export default TemplateAction;
