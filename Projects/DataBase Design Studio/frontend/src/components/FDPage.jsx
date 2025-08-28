// src/components/FDPage.jsx
import React from 'react';
import { useStateContext } from '../context/StateContext';
import { useNavigate } from 'react-router-dom';

const FDPage = () => {
  const { originalFDs } = useStateContext();
  const navigate = useNavigate();

  return (
    <div className="fd-page">
      <button onClick={() => navigate(-1)} style={{ marginBottom: '1rem' }}>
        ← Back
      </button>
      <h2>Functional Dependencies</h2>
      {originalFDs.length === 0 ? (
        <p>No Functional Dependencies found.</p>
      ) : (
        <ul>
          {originalFDs.map((fd, index) => (
            <li key={index}>
              {Array.isArray(fd.lhs) ? fd.lhs.join(', ') : fd.lhs} → {fd.rhs}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FDPage;
