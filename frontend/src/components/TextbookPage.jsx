import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import ExamQuestions from './ExamQuestions';
import './TextbookPage.css';

// Custom link component for internal textbook links
function TextbookLink({ href, children, currentPath, ...props }) {
  const navigate = useNavigate();
  
  if (!href) {
    return <a {...props}>{children}</a>;
  }
  
  // Handle external links (http, https, mailto, etc.)
  if (href.startsWith('http') || href.startsWith('mailto') || href.startsWith('#')) {
    return (
      <a href={href} {...props} target="_blank" rel="noopener noreferrer">
        {children}
      </a>
    );
  }
  
  // Check if this is an internal textbook link (absolute) or old wiki link
  const isAbsoluteInternalLink = href.startsWith('/textbook') || href.startsWith('/wiki');
  
  // Check if this is a relative link (doesn't start with / or protocol)
  const isRelativeLink = !href.startsWith('/') && !href.includes('://');
  
  if (isAbsoluteInternalLink || isRelativeLink) {
    let finalHref;
    
    if (isAbsoluteInternalLink) {
      // Convert old wiki links to textbook links
      finalHref = href.startsWith('/wiki') ? href.replace('/wiki', '/textbook') : href;
    } else if (isRelativeLink) {
      // Resolve relative link based on current path
      const currentDir = currentPath === 'index' ? '' : currentPath;
      const basePath = currentDir ? `/textbook/${currentDir}` : '/textbook';
      finalHref = `${basePath}/${href}`;
    }
    
    return (
      <a
        {...props}
        href={finalHref}
        onClick={(e) => {
          e.preventDefault();
          navigate(finalHref);
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

// Function to render content with custom components
function renderContentWithComponents(content, textbookPath) {
  console.log('renderContentWithComponents called with content:', content.substring(0, 200) + '...');
  console.log('textbookPath:', textbookPath);
  
  // Look for exam questions marker: {{ExamQuestions:filename.yml}}
  const examQuestionsRegex = /\{\{ExamQuestions:([\w\-\.]+)\}\}/g;
  
  const parts = [];
  let lastIndex = 0;
  let match;
  
  while ((match = examQuestionsRegex.exec(content)) !== null) {
    console.log('Found ExamQuestions marker:', match[0], 'File:', match[1]);
    // Add markdown content before the component
    if (match.index > lastIndex) {
      const markdownContent = content.slice(lastIndex, match.index);
      parts.push(
        <ReactMarkdown 
          key={`md-${parts.length}`}
          rehypePlugins={[rehypeRaw]}
          components={{
            a: (props) => <TextbookLink {...props} currentPath={textbookPath} />
          }}
        >
          {markdownContent}
        </ReactMarkdown>
      );
    }
    
    // Add the ExamQuestions component
    const yamlFile = match[1];
    parts.push(
      <ExamQuestions 
        key={`eq-${parts.length}`}
        yamlPath={yamlFile} 
        currentPath={textbookPath} 
      />
    );
    
    lastIndex = match.index + match[0].length;
  }
  
  // Add remaining markdown content
  if (lastIndex < content.length) {
    const remainingContent = content.slice(lastIndex);
    parts.push(
      <ReactMarkdown 
        key={`md-${parts.length}`}
        rehypePlugins={[rehypeRaw]}
        components={{
          a: (props) => <TextbookLink {...props} currentPath={textbookPath} />
        }}
      >
        {remainingContent}
      </ReactMarkdown>
    );
  }
  
  console.log('renderContentWithComponents: parts.length =', parts.length);
  
  return parts.length > 0 ? parts : [
    <ReactMarkdown 
      key="default"
      rehypePlugins={[rehypeRaw]}
      components={{
        a: (props) => <TextbookLink {...props} currentPath={textbookPath} />
      }}
    >
      {content}
    </ReactMarkdown>
  ];
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
          <h1>Loading...</h1>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="textbook-page error">
        <div className="textbook-header">
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
        <div className="textbook-breadcrumb">
          <span>Textbook</span>
          {textbookPath !== 'index' && (
            <span> / {textbookPath.replace(/\//g, ' / ')}</span>
          )}
        </div>
      </div>
      
      <div className="textbook-content">
        {renderContentWithComponents(content, textbookPath)}
      </div>
    </div>
  );
}

export default TextbookPage;
