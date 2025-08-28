import axios from 'axios';

// Set base URL for backend API (adjust if needed)
axios.defaults.baseURL = 'http://localhost:5000';  // Change if deploying to a server

// ---------------------- File Upload ---------------------- //
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const response = await axios.post('/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    // Always check for expected response structure to avoid parsing errors
    if (response.status === 200 && response.data?.message) {
      return response.data.message;
    } else {
      throw new Error('Unexpected response from upload API');
    }
  } catch (error) {
    // Improve error handling: check if error.response exists to avoid undefined
    throw new Error(error.response?.data?.message || 'File upload failed');
  }
};

// ---------------------- Backend Actions ---------------------- //
export const triggerBackendStep = async (stepName) => {
  const endpointMap = {
    ConvertToCSV: '/api/convert_to_csv',
    CleanModify: '/api/clean_modify',
    FDModified: '/api/fd_modified',
    KeyDetection: '/api/key_detection',
    NormalizeTable: '/api/normalize_table',
    DependencyPreservation: '/api/dependency_preservation',
    LosslessCheck: '/api/lossless_check',
    ERDiagram: '/api/generate_er_diagram',
  };

  const endpoint = endpointMap[stepName];
  if (!endpoint) {
    throw new Error('Invalid step name');
  }

  try {
    const response = await axios.post(endpoint);

    // Check for HTTP 2xx status to avoid parsing error
    if (response.status < 200 || response.status >= 300) {
      // Response is not OK, handle as error
      throw new Error(`Server returned status ${response.status}`);
    }

    if (stepName === 'LosslessCheck') {
      // Custom handling for LosslessCheck:
      if (response.data && typeof response.data.message === 'string') {
        return response.data.message;
      }
      if (response.data) {
        return JSON.stringify(response.data);
      }
      return 'Unexpected response from lossless check API';
    }

    // Default handling for other steps
    if (response.data && typeof response.data.message === 'string') {
      return response.data.message;
    }

    throw new Error(`Invalid response from server on ${stepName}`);
  } catch (error) {
    // Always check error.response before accessing its data
    throw new Error(error.response?.data?.message || `Failed to trigger ${stepName}`);
  }
};

// ---------------------- Fetch Backend Code ---------------------- //
export const fetchCodeForStep = async (stepName) => {
  try {
    const response = await axios.get(`/api/code/${stepName}`);

    // Defensive check for response data
    if (response.status === 200 && response.data?.code) {
      return response.data.code;
    } else {
      throw new Error('Invalid response when fetching code');
    }
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to fetch code');
  }
};

// Update the fetchNormalizedTables function in api.js
export const fetchNormalizedTables = async () => {
  try {
    const response = await axios.get('/api/normalized_tables');
    if (response.status === 200 && Array.isArray(response.data.tables)) {
      return response.data.tables;
    }
    console.warn('Unexpected response shape for normalized tables:', response.data);
    return [];
  } catch (error) {
    console.error('Error fetching normalized tables:', error);
    return [];
  }
};

// Add this new function
export const fetchTableData = async (tableName) => {
  try {
    const response = await axios.get(`/api/get_normalized_table/${tableName}`);
    if (response.status === 200 && response.data) {
      return response.data;
    }
    throw new Error('Invalid response fetching table data');
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch table data');
  }
};

// ---------------------- Dependency Preservation API Call ---------------------- //
export const checkDependencyPreservation = async (originalFDs, decomposedSchemas) => {
  try {
    const response = await axios.post(
      '/api/dependency_preservation',
      { originalFDs, decomposedSchemas },
      { headers: { 'Content-Type': 'application/json' } }
    );

    if (response.status === 200 && typeof response.data.message === 'string') {
      return response.data.message;
    }
    throw new Error('Invalid response from dependency preservation API');
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Dependency preservation check failed';
    console.error('Dependency preservation check failed:', errorMsg);
    throw new Error(errorMsg);
  }
};

// ---------------------- Lossless Check API Call ---------------------- //
export const triggerLosslessCheck = async () => {
  try {
    const response = await axios.post('/api/lossless_check');

    if (response.status === 200 && typeof response.data.message === 'string') {
      return response.data.message;
    }

    if (response.data) {
      return JSON.stringify(response.data);
    }
    return 'Unexpected response from lossless check API';
  } catch (error) {
    const msg = error.response?.data?.message || error.message || 'Lossless check failed';
    console.error('Lossless check API error:', msg);
    throw new Error(msg);
  }
};
