import React, { createContext, useContext, useState, useCallback } from 'react'; //	A wrapper component that holds the global state and passes it to all children via <StateContext.Provider>.
import axios from 'axios';   //A library for making HTTP requests (GET, POST, etc.) to your backend API.

const StateContext = createContext();

export const StateProvider = ({ children }) => {
  const [workflowSteps, setWorkflowSteps] = useState([]);
  const [currentCode, setCurrentCodeState] = useState('');
  const [messages, setMessages] = useState([]);
  const [normalizedTables, setNormalizedTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');

  const [originalFDs, setOriginalFDs] = useState([]);
  const [decomposedSchemas, setDecomposedSchemas] = useState([]);
  const [erDiagramGenerated, setErDiagramGenerated] = useState(false);
  const [fdGenerated, setFDGenerated] = useState(false);
  // In your StateContext.jsx, update the initial state:
  const [selectedTableData, setSelectedTableData] = useState({
    name: '',
    headers: [],
    rows: []
  });


  const addWorkflowStep = useCallback((stepName) => {
    setWorkflowSteps((prev) => (prev.includes(stepName) ? prev : [...prev, stepName]));
  }, []);

  const fetchCode = useCallback(async (stepName) => {
    try {
      const response = await axios.get(`/api/code/${stepName}`);
      return response.data.code;
    } catch {
      return 'Error fetching code.';
    }
  }, []);

  const setCurrentCode = useCallback((code) => {
    setCurrentCodeState(code);
  }, []);

  const addMessage = useCallback((msg) => {
    setMessages((prev) => [...prev, msg]);
  }, []);



  const fetchNormalizedTables = useCallback(async () => {
    try {
      const response = await axios.get('/api/normalized_tables');
      setNormalizedTables(response.data.tables || []);
    } catch (error) {
      console.error('Failed to fetch normalized tables', error);
    }
  }, []);

  // In your fetchSelectedTableData function:
  // In StateContext.jsx
  const fetchSelectedTableData = useCallback(async (tableName) => {
    try {
      const response = await axios.get(`/api/get_normalized_table/${tableName}`);
    
      // Normalize the response data
      const data = response.data || {};
      const normalizedData = {
        name: data.name || tableName,
        headers: data.headers || data.header || [],
        rows: data.rows || data.rank || []
      };
    
      console.log('Normalized table data:', normalizedData);
      setSelectedTableData(normalizedData);
      return normalizedData;
    } catch (error) {
      console.error('Failed to fetch table data', error);
      setSelectedTableData({
        name: tableName,
        headers: [],
        rows: []
      });
      throw error;
    }
  }, []);

  const fetchOriginalFDs = useCallback(async () => {
    try {
      const response = await axios.get('/api/detected_fds');
      setOriginalFDs(response.data.fds || []);
    } catch (error) {
      console.error('Failed to fetch Functional Dependencies', error);
      setOriginalFDs([]);
    }
  }, []);

  const fetchDecomposedSchemas = useCallback(async () => {
    try {
      const response = await axios.get('/api/decomposed_schemas');
      setDecomposedSchemas(response.data.schemas || []);
    } catch (error) {
      console.error('Failed to fetch Decomposed Schemas', error);
      setDecomposedSchemas([]);
    }
  }, []);

  const checkDependencyPreservation = useCallback(async (fds, schemas) => {
    try {
      const response = await axios.post(
        '/api/dependency_preservation',
        { originalFDs: fds, decomposedSchemas: schemas },
        { headers: { 'Content-Type': 'application/json' } }
      );
      const message = response.data.message || 'Dependency preservation checked.';
      addMessage(message);
      addWorkflowStep('DependencyPreservation');
      return message;
    } catch (error) {
      const errMsg = error.response?.data?.message || 'Dependency preservation check failed.';
      addMessage(errMsg);
      throw new Error(errMsg);
    }
  }, [addMessage, addWorkflowStep]);

  return (
    <StateContext.Provider
      value={{
        workflowSteps,
        addWorkflowStep,
        fetchCode,
        currentCode,
        setCurrentCode,
        messages,
        addMessage,
        normalizedTables,
        fetchNormalizedTables,
        fdGenerated,
        setFDGenerated,
        selectedTable,
        setSelectedTable,
        selectedTableData,
        fetchSelectedTableData,
        originalFDs,
        fetchOriginalFDs,
        decomposedSchemas,
        fetchDecomposedSchemas,
        checkDependencyPreservation,
        erDiagramGenerated,
        setErDiagramGenerated,

      }}
    >
      {children}
    </StateContext.Provider>
  );
};

export const useStateContext = () => useContext(StateContext);
