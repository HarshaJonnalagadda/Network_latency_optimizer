import React, { useEffect, useState, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api/axios';
import PcapFileUpload from './PcapFileUpload';
import './ProjectDetail.css'; // Import the updated CSS

const ProjectDetail = () => {
  const { id } = useParams();
  const [project, setProject] = useState(null);

  // Fetch the project details
  const fetchProject = useCallback(async () => {
    try {
      const response = await api.get(`/projects/${id}/`);
      setProject(response.data);
    } catch (error) {
      console.error('Error fetching project:', error);
    }
  }, [id]);

  useEffect(() => {
    fetchProject();
  }, [fetchProject]);

  if (!project) {
    return <p>Loading project...</p>;
  }

  return (
    <div className="container">
      <h2 className="project-title">Project Name</h2>
      <p className="project-info">{project.name}</p>

      <h2 className="project-title">Project Description</h2>
      <p className="project-info">{project.description}</p>

      <PcapFileUpload projectId={id} />

      <Link to="/" className="back-link">
        Back to Projects
      </Link>
    </div>
  );
};

export default ProjectDetail;
