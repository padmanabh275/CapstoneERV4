import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext.tsx';
import { contentApi, ContentRequest } from '../../services/contentApi';

export default function ContentEditor() {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    title: '',
    content_type: 'blog_post',
    description: '',
    target_audience: '',
    tone: 'professional',
    word_count: 500,
    keywords: '',
    preferred_model: 'auto'
  });

  const [generatedContent, setGeneratedContent] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    
    try {
      const request: ContentRequest = {
        title: formData.title,
        content_type: formData.content_type,
        description: formData.description,
        target_audience: formData.target_audience,
        tone: formData.tone,
        word_count: parseInt(formData.word_count.toString()),
        keywords: formData.keywords ? formData.keywords.split(',').map(k => k.trim()) : [],
        preferred_model: formData.preferred_model
      };

      const response = await contentApi.generateContent(request);
      setGeneratedContent(response.content);
    } catch (error) {
      console.error('Content generation failed:', error);
      setGeneratedContent('Content generation failed. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSave = () => {
    if (generatedContent) {
      console.log('Saving content:', generatedContent);
      alert('Content saved! (Check console for details)');
    }
  };

  const handleCopy = () => {
    if (generatedContent) {
      navigator.clipboard.writeText(generatedContent);
      alert('Content copied to clipboard!');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Modern Header */}
      <div className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-white text-xl font-bold">AI</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Content Creator</h1>
                <p className="text-sm text-gray-500">AI-Powered Content Generation</p>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              <Link
                to="/dashboard"
                className="px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors font-medium"
              >
                📊 Dashboard
              </Link>
              <Link
                to="/projects"
                className="px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors font-medium"
              >
                📁 Projects
              </Link>
              <Link
                to="/profile"
                className="px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors font-medium"
              >
                👤 Profile
              </Link>
              <div className="w-px h-6 bg-gray-200"></div>
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                  {user?.username?.charAt(0)?.toUpperCase() || 'U'}
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-gray-900">{user?.username || 'User'}</div>
                  <div className="text-xs text-gray-500">{user?.email || 'user@example.com'}</div>
                </div>
                <Link to="/logout" className="text-gray-400 hover:text-gray-600 transition-colors">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Left Column - Content Parameters */}
          <div className="xl:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
                  <span className="text-white text-lg">⚙️</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900">Content Parameters</h3>
                  <p className="text-sm text-gray-500">Configure your content generation</p>
                </div>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Content Title
                  </label>
                  <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="Enter your content title"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Content Type
                  </label>
                  <select
                    name="content_type"
                    value={formData.content_type}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    required
                  >
                    <option value="blog_post">📝 Blog Post</option>
                    <option value="article">📄 Article</option>
                    <option value="marketing_copy">💼 Marketing Copy</option>
                    <option value="social_media">📱 Social Media</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Description
                  </label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
                    placeholder="Describe what you want to create"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Target Audience
                    </label>
                    <input
                      type="text"
                      name="target_audience"
                      value={formData.target_audience}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="e.g., Business professionals"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Tone
                    </label>
                    <select
                      name="tone"
                      value={formData.tone}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      required
                    >
                      <option value="professional">👔 Professional</option>
                      <option value="casual">😊 Casual</option>
                      <option value="friendly">😊 Friendly</option>
                      <option value="formal">🎩 Formal</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Word Count
                    </label>
                    <input
                      type="number"
                      name="word_count"
                      value={formData.word_count}
                      onChange={handleInputChange}
                      min="100"
                      max="2000"
                      className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      AI Model
                    </label>
                    <select
                      name="preferred_model"
                      value={formData.preferred_model}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    >
                      <option value="auto">🤖 Auto (Best Available)</option>
                      <option value="ollama">🖥️ Ollama (Local AI)</option>
                      <option value="openai">🧠 OpenAI GPT-4</option>
                      <option value="claude"> Claude 3</option>
                      <option value="gemini">⭐ Google Gemini</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Keywords (comma-separated)
                  </label>
                  <input
                    type="text"
                    name="keywords"
                    value={formData.keywords}
                    onChange={handleInputChange}
                    placeholder="AI, technology, innovation"
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isGenerating}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-semibold text-lg shadow-lg hover:shadow-xl"
                >
                  {isGenerating ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Generating Content...</span>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center space-x-2">
                      <span>▶️ Generate Content</span>
                    </div>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Right Column - Generated Content */}
          <div className="xl:col-span-2">
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
                    <span className="text-white text-lg">📄</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">Generated Content</h3>
                    <p className="text-sm text-gray-500">Your AI-generated content will appear here</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <button
                    onClick={handleSave}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
                  >
                    💾 Save
                  </button>
                  <button
                    onClick={handleCopy}
                    className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors font-medium"
                  >
                    📋 Copy
                  </button>
                </div>
              </div>
              
              <div className="bg-gray-50 border border-gray-200 rounded-xl p-6 min-h-[500px]">
                {generatedContent ? (
                  <div className="prose max-w-none">
                    <div className="text-gray-800 whitespace-pre-wrap leading-relaxed text-base">
                      {generatedContent}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-16">
                    <div className="w-20 h-20 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-4xl">✨</span>
                    </div>
                    <h4 className="text-lg font-semibold text-gray-700 mb-2">Ready to Create</h4>
                    <p className="text-gray-500">Fill out the form and click "Generate Content" to get started</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
