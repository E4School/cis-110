import React, { useRef, useEffect, useState } from 'react';
import './YouTube.css';

function YouTube({ url, title, width = 560, height = 315, timestamps = [] }) {
  const iframeRef = useRef(null);
  const [isPlayerReady, setIsPlayerReady] = useState(false);

  // Extract video ID from various YouTube URL formats
  const extractVideoId = (url) => {
    const regex = /(?:youtube\.com\/(?:[^/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?/\s]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
  };

  const videoId = extractVideoId(url);
  
  if (!videoId) {
    return (
      <div className="youtube-error">
        <p>Invalid YouTube URL: {url}</p>
      </div>
    );
  }

  // Convert timestamp string (e.g., "1:23" or "12:34") to seconds
  const parseTimestamp = (timestamp) => {
    const parts = timestamp.split(':').map(part => parseInt(part, 10));
    if (parts.length === 2) {
      return parts[0] * 60 + parts[1]; // minutes:seconds
    } else if (parts.length === 3) {
      return parts[0] * 3600 + parts[1] * 60 + parts[2]; // hours:minutes:seconds
    }
    return 0;
  };

  // Handle timestamp click
  const handleTimestampClick = (timestamp) => {
    if (!isPlayerReady) {
      console.warn('YouTube player not ready yet');
      return;
    }

    const seconds = parseTimestamp(timestamp);
    
    // Send message to YouTube iframe to seek to specific time
    if (iframeRef.current && iframeRef.current.contentWindow) {
      const message = {
        event: 'command',
        func: 'seekTo',
        args: [seconds, true]
      };
      
      iframeRef.current.contentWindow.postMessage(
        JSON.stringify(message),
        'https://www.youtube.com'
      );
    }
  };

  // Enable YouTube API when iframe loads
  useEffect(() => {
    const iframe = iframeRef.current;
    if (iframe) {
      const handleLoad = () => {
        // Enable API by sending a listening message
        iframe.contentWindow.postMessage(
          '{"event":"listening","id":"ytplayer"}',
          'https://www.youtube.com'
        );
        setIsPlayerReady(true);
      };

      iframe.addEventListener('load', handleLoad);
      return () => iframe.removeEventListener('load', handleLoad);
    }
  }, []);

  // Build embed URL with API enabled
  const embedUrl = `https://www.youtube.com/embed/${videoId}?enablejsapi=1&origin=${window.location.origin}`;

  return (
    <div className="youtube-container">
      <iframe
        ref={iframeRef}
        width={width}
        height={height}
        src={embedUrl}
        title={title || "YouTube video player"}
        frameBorder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerPolicy="strict-origin-when-cross-origin"
        allowFullScreen
      />
      {title && <p className="youtube-caption">{title}</p>}
      
      {timestamps && timestamps.length > 0 && Array.isArray(timestamps) && (
        <div className="youtube-timestamps">
          <h4>Jump to:</h4>
          <div className="timestamp-list">
            {timestamps.map((timestamp, index) => (
              <button
                key={index}
                className="timestamp-button"
                onClick={() => handleTimestampClick(timestamp)}
                title={`Jump to ${timestamp}`}
              >
                <span className="timestamp-time">{timestamp}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default YouTube;