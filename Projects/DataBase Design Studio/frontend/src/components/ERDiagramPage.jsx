import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';

const ERDiagramPage = () => {
  const [imageURL, setImageURL] = useState(null);
  const [error, setError] = useState(null);
  const containerRef = useRef(null);
  const scaleRef = useRef(1); // store current scale

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const onWheel = (e) => {
      if (!e.ctrlKey) return; // zoom only if Ctrl pressed
      e.preventDefault();

      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      scaleRef.current = Math.min(Math.max(0.5, scaleRef.current + delta), 3);

      container.style.transform = `scale(${scaleRef.current})`;
    };

    container.addEventListener('wheel', onWheel, { passive: false });

    return () => {
      container.removeEventListener('wheel', onWheel);
    };
  }, []);

  const resetZoom = () => {
    const container = containerRef.current;
    if (!container) return;

    scaleRef.current = 1;
    container.style.transform = 'scale(1)';
  };

  const goBack = () => {
    window.history.back();
  };

  useEffect(() => {
    const fetchERDiagram = async () => {
      try {
        const response = await axios.get('/api/get_er_diagram_image', { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(response.data);
        setImageURL(blobUrl);
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to load ER Diagram');
      }
    };

    fetchERDiagram();
  }, []);

  // Small button styles
  const smallButtonStyle = {
    padding: '4px 8px',
    fontSize: 12,
    cursor: 'pointer',
    borderRadius: 3,
    border: '1px solid #ccc',
    backgroundColor: 'transparent',
    color: '#333',
    transition: 'background-color 0.2s ease',
  };

  const onMouseEnter = (e) => (e.currentTarget.style.backgroundColor = 'rgba(0,0,0,0.05)');
  const onMouseLeave = (e) => (e.currentTarget.style.backgroundColor = 'transparent');

  return (
    <div>
      <h2
      style={{
          textAlign: 'center',
          color: '#b3e5fc',
          fontSize: '2.4 rem',
          fontFamily: "'Georgia', serif",

      }}
      >ER Diagram</h2>

      {/* Buttons container below header */}
      <div
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom: '12px',
          backgroundColor: 'rgba(149, 183, 225, 1)', // subtle background
          padding: '6px 12px',
          borderRadius: 4,
          alignItems: 'center',
          userSelect: 'none',
          width: 'fit-content',
          marginLeft: 'auto',
          marginRight: 'auto',
        }}
      >
        <button
          onClick={resetZoom}
          style={smallButtonStyle}
          onMouseEnter={onMouseEnter}
          onMouseLeave={onMouseLeave}
          aria-label="Reset Zoom"
          type="button"
        >Reset
        </button>
        <button
          onClick={goBack}
          style={smallButtonStyle}
          onMouseEnter={onMouseEnter}
          onMouseLeave={onMouseLeave}
          aria-label="Go Back"
          type="button"
        >
          Back
        </button>
      </div>

      {error && <div style={{ color: 'red', marginBottom: 16 }}>{error}</div>}

      <div
        ref={containerRef}
        style={{
          border: '1px solid #ccc',
          overflow: 'auto',
          width: '100%',
          height: '72vh',
          cursor: 'grab',
          transformOrigin: '0 0',
        }}
      >
        {imageURL && (
          <img
            src={imageURL}
            alt="ER Diagram"
            style={{ width: '100%', height: 'auto', display: 'block' }}
            draggable={false}
          />
        )}
      </div>

      <p style={{ fontSize: '0.9rem', color: '#666', marginTop: 12, textAlign: 'center' }}>
        Use <strong>Ctrl + Mouse Wheel</strong> to zoom. Drag to pan.
      </p>
    </div>
  );
};

export default ERDiagramPage;
