import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext.tsx';
import Layout from './components/Layout/Layout.tsx';
import Dashboard from './pages/Dashboard/Dashboard.tsx';
import Projects from './pages/Projects/Projects.tsx';
import Profile from './pages/Profile/Profile.tsx';
import ContentEditor from './pages/ContentEditor/ContentEditor.tsx';
import Register from './pages/Auth/Register.tsx';
import Login from './pages/Auth/Login.tsx';
import ProjectDetail from './pages/Projects/ProjectDetail.tsx';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="projects" element={<Projects />} />
            <Route path="projects/:id" element={<ProjectDetail />} />
            <Route path="profile" element={<Profile />} />
            <Route path="editor" element={<ContentEditor />} />
          </Route>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;