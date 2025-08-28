import React, { useEffect } from 'react';
import { useStateContext } from '../context/StateContext';
import { useNavigate } from 'react-router-dom';

const TableView = () => {
  const { selectedTableData } = useStateContext();
  const navigate = useNavigate();

  // Debugging logs
  useEffect(() => {
    console.log("Table data received:", selectedTableData);
  }, [selectedTableData]);

  // Safely get rows or empty array if invalid
  const rows = Array.isArray(selectedTableData?.rows) 
    ? selectedTableData.rows.filter(row => (
        Array.isArray(row) && 
        !row.some(cell => cell === null || cell === undefined || (typeof cell === 'number' && isNaN(cell)))
      ))
    : [];

  if (!selectedTableData || rows.length === 0) {
    return (
      <div style={{ padding: '20px', color: 'red' }}>
        <p>
          {!selectedTableData 
            ? "Error: No data received for table." 
            : "Table exists but contains no valid rows."
          }
        </p>
        <button className="dracula-button" onClick={() => navigate(-1)}>Go Back</button>


      </div>
    );
  }

  return (
    <div style={{ padding: '20px' }}>
      <h2>{selectedTableData.name || 'Untitled Table'}</h2>
      <button onClick={() => navigate(-1)}>Go Back</button>

      {/* Scrollable Wrapper */}
      <div 
        style={{
          overflowX: 'auto',
          overflowY: 'auto',
          maxHeight: '60vh',
          marginTop: '20px',
          border: '1px solid #ccc',
          borderRadius: '5px',
          scrollbarWidth: 'thin'
        }}
      >
        <table style={{ borderCollapse: 'collapse', width: '100%', minWidth: '5px' }}>
          <thead>
            <tr>
              {selectedTableData.headers?.map((header, i) => (
                <th 
                  key={i} 
                  style={{ 
                    border: '1px solid #ddd', 
                    padding: '8px', 
                    backgroundColor: '#ccc5c5ff', 
                    position: 'sticky', 
                    top: 0, 
                    zIndex: 2 
                  }}
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i}>
                {row.map((cell, j) => (
                  <td 
                    key={j} 
                    style={{ 
                      border: '1px solid #767575ff', 
                      padding: '8px',
                    }}
                  >
                    {cell === null || cell === undefined || (typeof cell === 'number' && isNaN(cell)) 
                      ? 'N/A' 
                      : String(cell)
                    }
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TableView;
