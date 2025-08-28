import React, { useState } from 'react';
import { useStateContext } from '../context/StateContext';
import { useNavigate } from 'react-router-dom';
import { FaTable, FaProjectDiagram, FaSitemap } from 'react-icons/fa';

const MessagePanel = () => {
  const {
    messages,
    normalizedTables,
    fetchSelectedTableData,
    addMessage,
    erDiagramGenerated,
    fdGenerated,
  } = useStateContext();

  const navigate = useNavigate();
  const [isDropdownOpen, setDropdownOpen] = useState(false);

  const handleTableClick = async (tableName) => {
    try {
      addMessage(`Loading table ${tableName}...`);
      await fetchSelectedTableData(tableName);
      navigate('/table-view');
    } catch (error) {
      console.error('Error fetching table data:', error);
      addMessage(`Error loading table ${tableName}: ${error.response?.data?.error || error.message}`);
    }
  };

  const handleERDiagramClick = () => navigate('/er-diagram');
  const handleFDPageClick = () => navigate('/fd-view');

  // ✨ Error cleaner
  const cleanErrorMessage = (msg) => {
    if (typeof msg !== 'string') return msg;

    // Suppress common HTML/JSON parse error
    if (msg.includes('Unexpected token') && msg.includes('<!DOCTYPE')) {
      return null;
    }

    return msg;
  };

  return (
    <div className="message-panel">
      <div className="messages-list">
        {messages.map((msg, index) => {
          const cleaned = cleanErrorMessage(msg);
          return cleaned ? (
            <div key={index} className="message-item">
              {typeof cleaned === 'string' ? cleaned : JSON.stringify(cleaned)}
            </div>
          ) : null; // Skip rendering suppressed messages
        })}
      </div>

      {normalizedTables.length > 0 && (
        <div className="normalized-tables">
          <div className="dropdown">
            <button
              className="dropdown-toggle"
              onClick={() => setDropdownOpen((prev) => !prev)}
            >
              <FaTable style={{ marginRight: '6px' }} />
              Normalized Tables ▼
            </button>

            {isDropdownOpen && (
              <ul className="dropdown-menu">
                {normalizedTables.map((table, index) => (
                  <li key={index} onClick={() => handleTableClick(table)}>
                    <FaTable style={{ marginRight: '6px' }} />
                    {table}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}

      {erDiagramGenerated && (
        <button onClick={handleERDiagramClick} className="er-diagram-button">
          <FaProjectDiagram style={{ marginRight: '6px' }} />
          Show ER Diagram
        </button>
      )}

      {fdGenerated && (
        <button onClick={handleFDPageClick} className="er-diagram-button">
          <FaSitemap style={{ marginRight: '6px' }} />
          Show Functional Dependencies
        </button>
      )}
    </div>
  );
};

export default MessagePanel;
