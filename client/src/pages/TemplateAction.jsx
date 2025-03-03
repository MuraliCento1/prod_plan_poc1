import React, { useState } from "react";
import { Card, CardContent, Typography, Button, Select, MenuItem, InputLabel, FormControl, Box, IconButton } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import DownloadIcon from "@mui/icons-material/Download";
import DeleteIcon from "@mui/icons-material/Delete";
import axios from "axios";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const TemplateAction = () => {
  const [file, setFile] = useState(null);
  const [selection, setSelection] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDeleteFile = () => {
    setFile(null);
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
    
    const baseUrl = process.env.REACT_APP_BASE_URL;
    const url = `${baseUrl}/uploadfile/?table_name=${selection}`;

    try {
      const response = await axios.post(url, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (response.status === 200) {
        toast.success("File uploaded successfully!");
      } else {
        toast.warn("Upload completed, but check response for details.");
      }
    } catch (error) {
      console.error("Upload Error:", error);
      toast.error("File upload failed. Please try again.");
    }
    
    console.log({ selection, file });
  };

  const handleDownloadSubmit = async (e) => {
    e.preventDefault();
    if (!selection) {
      console.log("Please select a valid dropdown option.");
      return;
    }
    console.log({ selection });
  };

  return (
    <Card sx={{ maxWidth: 400, margin: "auto", mt: 4, p: 2, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Template Actions
        </Typography>
        
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Select an Option</InputLabel>
          <Select value={selection} onChange={handleSelectionChange}>
            <MenuItem value="bom">BOM</MenuItem>
            <MenuItem value="production_plan">Production Plan</MenuItem>
            <MenuItem value="sku_master">Sku Master</MenuItem>
            <MenuItem value="vendor_master">Vendor Master</MenuItem>
            <MenuItem value="stock_master">Stock Master</MenuItem>
            <MenuItem value="vendor_inwarding_master">Vendor Inwarding Master</MenuItem>
          </Select>
        </FormControl>

        {!file ? (
          <>
            <input type="file" onChange={handleFileChange} style={{ display: "none" }} id="upload-file" />
            <label htmlFor="upload-file">
              <Button
                variant="contained"
                component="span"
                fullWidth
                startIcon={<CloudUploadIcon />}
                sx={{ mb: 2 }}
              >
                Choose File
              </Button>
            </label>
          </>
        ) : (
          <Box display="flex" alignItems="center" justifyContent="space-between" sx={{ mb: 2, p: 1, border: "1px solid #ccc", borderRadius: 1 }}>
            <Typography variant="body2" noWrap>{file.name}</Typography>
            <IconButton size="small" onClick={handleDeleteFile} color="error">
              <DeleteIcon />
            </IconButton>
          </Box>
        )}

        <Button
          variant="contained"
          color="primary"
          fullWidth
          onClick={handleUploadSubmit}
          disabled={!selection || !file}
          sx={{ mb: 2 }}
        >
          Upload
        </Button>

        <Button
          variant="outlined"
          color="secondary"
          fullWidth
          startIcon={<DownloadIcon />}
          onClick={handleDownloadSubmit}
          disabled
        >
          Download
        </Button>
      </CardContent>
    </Card>
  );
};

export default TemplateAction;
