import React, { useState, useEffect, useCallback } from 'react';
import api from '../api/axios';
import './PcapFileUpload.css';
import { Bar, Line } from 'react-chartjs-2';
import 'chart.js/auto';

const PcapFileUpload = ({ projectId }) => {
  const [files, setFiles] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [analysisResult, setAnalysisResult] = useState(null);

  // Fetch existing PCAP files for the project
  const fetchFiles = useCallback(async () => {
    try {
      const response = await api.get(`/projects/${projectId}/pcap_files/`);
      setFiles(response.data);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  }, [projectId]);

  // Fetch analysis result
  const fetchAnalysisResult = useCallback(async () => {
    try {
      const response = await api.get(`/analysis/projects/${projectId}/result/`);
      setAnalysisResult(response.data);
    } catch (error) {
      console.error('No analysis result found:', error);
    }
  }, [projectId]);

  useEffect(() => {
    fetchFiles();
    fetchAnalysisResult();
  }, [fetchFiles, fetchAnalysisResult]);

  // Handle file selection
  const handleFileChange = (e) => {
    setSelectedFiles(e.target.files);
  };

  // Upload selected files
  const uploadFiles = async () => {
    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append('files', selectedFiles[i]);
    }

    try {
      await api.post(`/projects/${projectId}/pcap_files/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      fetchFiles();
      setSelectedFiles([]);
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };

  // Delete a file by ID
  const deleteFile = async (fileId) => {
    try {
      await api.delete(`/pcap_files/${fileId}/delete/`);
      fetchFiles();
    } catch (error) {
      console.error('Error deleting file:', error);
    }
  };

  // Analyze the project
  const analyzeProject = async () => {
    try {
      const response = await api.post(`/analysis/projects/${projectId}/analyze/`, null, { timeout: 1800000 });
      setAnalysisResult(response.data);
    } catch (error) {
      console.error('Error analyzing project:', error);
    }
  };

  return (
    <div className="card">
      <h3>Upload PCAP Files</h3>
      <div className="upload-section">
        <input type="file" multiple onChange={handleFileChange} />
        <button className="upload-button" onClick={uploadFiles} disabled={selectedFiles.length === 0}>
          Upload Files
        </button>
      </div>

      <h3>Uploaded Files</h3>
      <table className="file-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Filename</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {files.map((file, index) => (
            <tr key={file.id}>
              <td>{index + 1}</td>
              <td>{file.file.split('/').pop()}</td>
              <td>
                <button className="delete-button" onClick={() => deleteFile(file.id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button className="analyze-button" onClick={analyzeProject} disabled={files.length === 0}>
        Analyze
      </button>

      {analysisResult && (
        <div className="analysis-results">
          <h3>Analysis Results</h3>
          <p><strong>Anomalies Detected:</strong> {analysisResult.anomalies_detected}</p>
          <p><strong>Average Latency:</strong> {analysisResult.average_latency} ms</p>

          <h4>Optimization Table</h4>
          <table className="optimization-table">
            <thead>
              <tr>
                <th>Source</th>
                <th>Destination</th>
                <th>Current Path</th>
                <th>Anomalies in Path</th>
                <th>Current Latency</th>
                <th>Optimized Path</th>
                <th>Predicted Latency</th>
              </tr>
            </thead>
            <tbody>
              {(Array.isArray(analysisResult.optimizations) ? analysisResult.optimizations : []).map((opt, index) => (
                <tr key={index}>
                  <td>{opt.source}</td>
                  <td>{opt.destination}</td>
                  <td>{`${opt.source} -> ${opt.destination}`}</td>
                  <td>{analysisResult.anomalies_detected > 0 ? 'Yes' : 'No'}</td>
                  <td>{opt.current_latency}</td>
                  <td>{opt.optimized_path}</td>
                  <td>{opt.optimized_latency}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="charts">
            <div className="chart">
              <h4>Anomalies Chart</h4>
              <Bar
                data={{
                  labels: ['Anomalies Detected'],
                  datasets: [
                    {
                      label: 'Anomalies',
                      data: [analysisResult.anomalies_detected || 0],
                      backgroundColor: '#ff6b6b',
                    },
                  ],
                }}
              />
            </div>
            <div className="chart">
              <h4>Latency Chart</h4>
              <Line
                data={{
                  labels: ['Latency'],
                  datasets: [
                    {
                      label: 'Average Latency (ms)',
                      data: [analysisResult.average_latency || 0],
                      backgroundColor: '#4a90e2',
                    },
                  ],
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PcapFileUpload;
