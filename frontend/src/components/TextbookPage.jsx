import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import './TextbookPage.css';

// Custom link component for internal textbook links
function TextbookLink({ href, children, ...props }) {
  const navigate = useNavigate();
  
  // Check if this is an internal textbook link (or old wiki link)
  const isInternalTextbookLink = href && (href.startsWith('/textbook') || href.startsWith('/wiki'));
  
  if (isInternalTextbookLink) {
    // Convert old wiki links to textbook links
    const updatedHref = href.startsWith('/wiki') ? href.replace('/wiki', '/textbook') : href;
    
    return (
      <a
        {...props}
        href={updatedHref}
        onClick={(e) => {
          e.preventDefault();
          navigate(updatedHref);
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

function TextbookPage() {
  const { '*': path } = useParams();
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Default to index if no path provided
  const textbookPath = path || 'index';
  const markdownUrl = `/textbook/${textbookPath}.md`;

  useEffect(() => {
    const fetchMarkdown = async () => {
      setLoading(true);
      setError(null);
      
      try {
        let response;
        let attemptedUrls = [];
        
        // For 'index' path, try /textbook/index.md directly
        if (textbookPath === 'index') {
          const url = `/textbook/index.md`;
          attemptedUrls.push(url);
          response = await fetch(url);
        } else {
          // Strategy: Try multiple URL patterns to handle both folder and direct file links
          // Try direct file first (more common), then folder with index.md
          const urlsToTry = [
            `/textbook/${textbookPath}.md`,         // For direct file links like /textbook/content/overviews/01-hardware-how-we-got-physics-to-do-math-r
            `/textbook/${textbookPath}/index.md`   // For folder-style links like /textbook/hardware
          ];
          
          // Try each URL until we find one that works
          for (const url of urlsToTry) {
            attemptedUrls.push(url);
            console.log(`Trying to fetch: ${url}`);
            response = await fetch(url);
            console.log(`Response for ${url}:`, response.status, response.ok);
            
            if (response.ok) {
              // Check if we got HTML instead of markdown (happens when file doesn't exist)
              const text = await response.text();
              if (text.trim().startsWith('<!doctype html>') || text.trim().startsWith('<html')) {
                console.log(`Got HTML response for ${url}, trying next URL...`);
                continue; // Try the next URL
              }
              console.log(`Successfully found content at: ${url}`);
              response.text = () => Promise.resolve(text); // Cache the text we already read
              break;
            }
          }
        }

        if (!response || !response.ok) {
          throw new Error(`Textbook page not found. Tried: ${attemptedUrls.join(', ')}`);
        }

        const text = await response.text();
        setContent(text);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMarkdown();
  }, [textbookPath, markdownUrl]);

  if (loading) {
    return (
      <div className="textbook-page loading">
        <div className="textbook-header">
          <Link to="/textbook" className="textbook-home-link">← Textbook Home</Link>
          <h1>Loading...</h1>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="textbook-page error">
        <div className="textbook-header">
          <Link to="/textbook" className="textbook-home-link">← Textbook Home</Link>
          <h1>Page Not Found</h1>
        </div>
        <div className="textbook-content">
          <p>The requested textbook page could not be found.</p>
          <p><strong>Path:</strong> {textbookPath}</p>
          <p><strong>Error:</strong> {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="textbook-page">
      <div className="textbook-header">
        <Link to="/textbook" className="textbook-home-link">← Textbook Home</Link>
        <div className="textbook-breadcrumb">
          <span>Textbook</span>
          {textbookPath !== 'index' && (
            <span> / {textbookPath.replace(/\//g, ' / ')}</span>
          )}
        </div>
      </div>
      
      <div className="textbook-content">
        <ReactMarkdown 
          components={{
            a: TextbookLink
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}

export default TextbookPage;
