import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext.tsx';
import { contentApi, ContentResponse } from '../../services/contentApi';

export default function ProjectDetail() {
  const { user } = useAuth();
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState<ContentResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProject = async () => {
      if (!id) return;
      
      try {
        const data = await contentApi.getContent(id);
        setProject(data);
      } catch (error) {
        console.error('Failed to fetch project:', error);
        setError('Project not found or access denied');
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [id]);

  const handleDelete = async () => {
    if (!project || !window.confirm('Are you sure you want to delete this project?')) {
      return;
    }

    try {
      await contentApi.deleteContent(project.id);
      navigate('/projects');
    } catch (error) {
      console.error('Failed to delete project:', error);
      alert('Failed to delete project. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="flex h-full">
        <div className="w-64 bg-gray-800 text-white p-6">
          <h2 className="text-2xl font-bold mb-8">AI Content Creator</h2>
          <nav className="space-y-4">
            <Link to="/dashboard" className="block py-2 px-4 rounded hover:bg-gray-700">
              📊 Dashboard
            </Link>
            <Link to="/projects" className="block py-2 px-4 rounded bg-blue-600 text-white">
              📁 Projects
            </Link>
            <Link to="/editor" className="block py-2 px-4 rounded hover:bg-gray-700">
              ✏️ Content Editor
            </Link>
            <Link to="/profile" className="block py-2 px-4 rounded hover:bg-gray-700">
              👤 Profile
            </Link>
          </nav>
          
          <div className="mt-auto pt-8">
            <div className="text-sm text-gray-300">
              <div className="flex items-center mb-2">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold mr-2">
                  {user?.username?.charAt(0)?.toUpperCase() || 'U'}
                </div>
                <div>
                  <div>{user?.username || 'User'}</div>
                  <div className="text-xs">{user?.email || 'user@example.com'}</div>
                </div>
              </div>
              <Link to="/logout" className="text-blue-400 hover:text-blue-300 text-sm">
                → Logout
              </Link>
            </div>
          </div>
        </div>

        <div className="flex-1 bg-gray-50">
          <div className="bg-white border-b border-gray-200 px-8 py-4">
            <h1 className="text-2xl font-bold text-gray-800">Project Details</h1>
          </div>
          
          <div className="p-8">
            <div className="text-center py-12">
              <div className="animate-spin text-4xl mb-4">⏳</div>
              <div className="text-gray-600">Loading project...</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="flex h-full">
        <div className="w-64 bg-gray-800 text-white p-6">
          <h2 className="text-2xl font-bold mb-8">AI Content Creator</h2>
          <nav className="space-y-4">
            <Link to="/dashboard" className="block py-2 px-4 rounded hover:bg-gray-700">
              📊 Dashboard
            </Link>
            <Link to="/projects" className="block py-2 px-4 rounded bg-blue-600 text-white">
              📁 Projects
            </Link>
            <Link to="/editor" className="block py-2 px-4 rounded hover:bg-gray-700">
              ✏️ Content Editor
            </Link>
            <Link to="/profile" className="block py-2 px-4 rounded hover:bg-gray-700">
              👤 Profile
            </Link>
          </nav>
          
          <div className="mt-auto pt-8">
            <div className="text-sm text-gray-300">
              <div className="flex items-center mb-2">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold mr-2">
                  {user?.username?.charAt(0)?.toUpperCase() || 'U'}
                </div>
                <div>
                  <div>{user?.username || 'User'}</div>
                  <div className="text-xs">{user?.email || 'user@example.com'}</div>
                </div>
              </div>
              <Link to="/logout" className="text-blue-400 hover:text-blue-300 text-sm">
                → Logout
              </Link>
            </div>
          </div>
        </div>

        <div className="flex-1 bg-gray-50">
          <div className="bg-white border-b border-gray-200 px-8 py-4">
            <h1 className="text-2xl font-bold text-gray-800">Project Details</h1>
          </div>
          
          <div className="p-8">
            <div className="text-center py-12">
              <div className="text-4xl mb-4">❌</div>
              <div className="text-gray-600 mb-4">{error || 'Project not found'}</div>
              <Link
                to="/projects"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                Back to Projects
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-full">
      {/* Left Sidebar */}
      <div className="w-64 bg-gray-800 text-white p-6">
        <h2 className="text-2xl font-bold mb-8">AI Content Creator</h2>
        <nav className="space-y-4">
          <Link to="/dashboard" className="block py-2 px-4 rounded hover:bg-gray-700">
            📊 Dashboard
          </Link>
          <Link to="/projects" className="block py-2 px-4 rounded bg-blue-600 text-white">
            📁 Projects
          </Link>
          <Link to="/editor" className="block py-2 px-4 rounded hover:bg-gray-700">
            ✏️ Content Editor
          </Link>
          <Link to="/profile" className="block py-2 px-4 rounded hover:bg-gray-700">
            👤 Profile
          </Link>
        </nav>
        
        <div className="mt-auto pt-8">
          <div className="text-sm text-gray-300">
            <div className="flex items-center mb-2">
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold mr-2">
                {user?.username?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <div>
                <div>{user?.username || 'User'}</div>
                <div className="text-xs">{user?.email || 'user@example.com'}</div>
              </div>
            </div>
            <Link to="/logout" className="text-blue-400 hover:text-blue-300 text-sm">
              → Logout
            </Link>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 bg-gray-50">
        {/* Top Header */}
        <div className="bg-white border-b border-gray-200 px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-800">Project Details</h1>
            <div className="flex space-x-2">
              <Link
                to="/editor"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                ✏️ Edit
              </Link>
              <button
                onClick={handleDelete}
                className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
              >
                🗑️ Delete
              </button>
            </div>
          </div>
        </div>
        
        {/* Project Content */}
        <div className="p-8">
          <div className="max-w-4xl mx-auto">
            {/* Project Header */}
            <div className="bg-white p-6 rounded-lg shadow-md mb-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-2">{project.title}</h2>
                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <span>📝 {project.content_type.replace('_', ' ')}</span>
                    <span>📊 {project.word_count} words</span>
                    <span>📅 {new Date(project.created_at).toLocaleDateString()}</span>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      project.status === 'completed' ? 'bg-green-100 text-green-800' :
                      project.status === 'failed' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {project.status}
                    </span>
                  </div>
                </div>
              </div>

              {/* Metadata */}
              {project.content_metadata && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Target Audience:</span>
                    <span className="ml-2 text-gray-600">{project.content_metadata.target_audience}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Tone:</span>
                    <span className="ml-2 text-gray-600">{project.content_metadata.tone}</span>
                  </div>
                  {project.content_metadata.keywords && (
                    <div className="md:col-span-2">
                      <span className="font-medium text-gray-700">Keywords:</span>
                      <span className="ml-2 text-gray-600">{project.content_metadata.keywords.join(', ')}</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Project Content */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold mb-4">Content</h3>
              <div className="prose max-w-none">
                <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                  {project.content}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
