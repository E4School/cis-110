import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import './WikiPage.css';

// Custom link component for internal wiki links
function WikiLink({ href, children, ...props }) {
  const navigate = useNavigate();
  
  // Check if this is an internal wiki link
  const isInternalWikiLink = href && href.startsWith('/wiki');
  
  if (isInternalWikiLink) {
    return (
      <a
        {...props}
        href={href}
        onClick={(e) => {
          e.preventDefault();
          navigate(href);
        }}
        style={{ cursor: 'pointer' }}
      >
        {children}
      </a>
    );
  }
  
  // For external links, use normal anchor tag
  return (
    <a href={href} {...props} target="_blank" rel="noopener noreferrer">
      {children}
    </a>
  );
}

function WikiPage() {
  const { '*': path } = useParams();
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Default to index if no path provided
  const wikiPath = path || 'index';
  const markdownUrl = `/wiki/${wikiPath}.md`;

  useEffect(() => {
    const fetchMarkdown = async () => {
      setLoading(true);
      setError(null);
      
      try {
        let response;
        let attemptedUrl;
        
        // For 'index' path, try /wiki/index.md directly
        if (wikiPath === 'index') {
          attemptedUrl = `/wiki/index.md`;
          response = await fetch(attemptedUrl);
        } else {
          // For other paths, try directory/index.md first
          attemptedUrl = `/wiki/${wikiPath}/index.md`;
          response = await fetch(attemptedUrl);
          
          // If directory/index.md fails, try the exact path as .md file
          if (!response.ok) {
            attemptedUrl = `/wiki/${wikiPath}.md`;
            response = await fetch(attemptedUrl);
          }
        }

        if (!response.ok) {
          throw new Error(`Wiki page not found. Tried: ${attemptedUrl}`);
        }

        const text = await response.text();
        
        // Check if we got HTML instead of markdown (happens when file doesn't exist)
        if (text.trim().startsWith('<!doctype html>') || text.trim().startsWith('<html')) {
          throw new Error(`Wiki page not found - got HTML response for: ${attemptedUrl}`);
        }
        
        setContent(text);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMarkdown();
  }, [wikiPath, markdownUrl]);

  if (loading) {
    return (
      <div className="wiki-page loading">
        <div className="wiki-header">
          <Link to="/wiki" className="wiki-home-link">← Wiki Home</Link>
          <h1>Loading...</h1>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="wiki-page error">
        <div className="wiki-header">
          <Link to="/wiki" className="wiki-home-link">← Wiki Home</Link>
          <h1>Page Not Found</h1>
        </div>
        <div className="wiki-content">
          <p>The requested wiki page could not be found.</p>
          <p><strong>Path:</strong> {wikiPath}</p>
          <p><strong>Error:</strong> {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="wiki-page">
      <div className="wiki-header">
        <Link to="/wiki" className="wiki-home-link">← Wiki Home</Link>
        <div className="wiki-breadcrumb">
          <span>Wiki</span>
          {wikiPath !== 'index' && (
            <span> / {wikiPath.replace(/\//g, ' / ')}</span>
          )}
        </div>
      </div>
      
      <div className="wiki-content">
        <ReactMarkdown 
          components={{
            a: WikiLink
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}

export default WikiPage;
