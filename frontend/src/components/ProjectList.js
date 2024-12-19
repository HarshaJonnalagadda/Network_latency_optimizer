import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Reintroduce Link for navigation
import api from '../api/axios';
import './ProjectList.css';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects/');
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const createProject = async () => {
    try {
      await api.post('/projects/', { name, description });
      fetchProjects();
      setName('');
      setDescription('');
    } catch (error) {
      console.error('Error creating project:', error);
    }
  };

  const deleteProject = async (id) => {
    try {
      await api.delete(`/projects/${id}/`);
      fetchProjects();
    } catch (error) {
      console.error('Error deleting project:', error);
    }
  };

  return (
    <div className="container">
      <h1 className="heading">Network Latency Optimizer</h1>
      <h2 className="sub-heading">Projects</h2>
      <div className="form">
        <input
          type="text"
          placeholder="Project Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button onClick={createProject}>Create Project</button>
      </div>

      <table className="project-table">
        <thead>
          <tr>
            <th>Project Name</th>
            <th>Description</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project) => (
            <tr key={project.id} className="project-row">
              <td>
                <Link to={`/projects/${project.id}`} className="project-link">
                  {project.name}
                </Link>
              </td>
              <td>{project.description}</td>
              <td>
                <button className="delete-button" onClick={() => deleteProject(project.id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProjectList;
