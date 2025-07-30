import React from 'react';
import './index.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-Assisted Content Creation Platform</h1>
        <p>Welcome to your AI-powered content creation platform!</p>
        <div className="features">
          <div className="feature">
            <h3>🤖 AI Content Generation</h3>
            <p>Generate high-quality content with AI assistance</p>
          </div>
          <div className="feature">
            <h3>✏️ Content Refinement</h3>
            <p>Refine and improve your content with style adjustments</p>
          </div>
          <div className="feature">
            <h3>🔍 SEO Optimization</h3>
            <p>Optimize your content for search engines</p>
          </div>
          <div className="feature">
            <h3>✅ Plagiarism Check</h3>
            <p>Ensure your content is original and accurate</p>
          </div>
        </div>
        <div className="backend-info">
          <h4>Backend API Status</h4>
          <p>✅ Backend is running at: http://localhost:8000</p>
          <p>📚 API Documentation: <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">http://localhost:8000/docs</a></p>
        </div>
      </header>
    </div>
  );
}

export default App; 