import React, { useRef } from 'react';
import {
  Upload,
  FileSpreadsheet,
  Trash2,
  Search,
  Key,
  Database,
  Shield,
  CheckCircle,
  GitBranch,
  RotateCcw,
} from 'lucide-react';

import {
  uploadFile,
  triggerBackendStep,
  triggerLosslessCheck,
} from '../api';
import { useStateContext } from '../context/StateContext';

const leftColumnActions = [
  { id: 'upload-file', label: 'Dataset Upload', icon: Upload, color: 'bg-blue-500' },
  { id: 'clean', label: 'Noise Clean', icon: Trash2, color: 'bg-yellow-500' },
  { id: 'key-detection', label: 'Key Detector', icon: Key, color: 'bg-indigo-500' },
  { id: 'dependency-preservation', label: 'Check Dependency Preservation', icon: Shield, color: 'bg-orange-500' },
  { id: 'er-diagram', label: 'Generate ER Diagram', icon: GitBranch, color: 'bg-pink-500' },
];

const rightColumnActions = [
  { id: 'convert-csv', label: 'CSV Data Loader', icon: FileSpreadsheet, color: 'bg-green-500' },
  { id: 'fd-detection', label: 'FD Detector', icon: Search, color: 'bg-purple-500' },
  { id: 'normalized-tables', label: 'Normalization', icon: Database, color: 'bg-teal-500' },
  { id: 'lossless-check', label: 'Check Lossless Decomposition', icon: CheckCircle, color: 'bg-emerald-500' },
  { id: 'refresh-workflow', label: 'Refresh Workflow', icon: RotateCcw, color: 'bg-red-500' },
];

const ActionPanel = () => {
  const {
    addMessage,
    addWorkflowStep,
    fetchNormalizedTables,
    originalFDs,
    decomposedSchemas,
    fetchOriginalFDs,
    fetchDecomposedSchemas,
    checkDependencyPreservation,
    setErDiagramGenerated,
    setFDGenerated,
  } = useStateContext();

  const fileInputRef = useRef(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const message = await uploadFile(file);
      addMessage(message);
      addWorkflowStep('Upload');
    } catch (error) {
      addMessage(error.message);
    }
  };

  const handleBackendAction = async (stepName) => {
    try {
      const message = await triggerBackendStep(stepName);
      addMessage(message);
      addWorkflowStep(stepName);

      if (stepName === 'FDModified') {
        await fetchOriginalFDs();
        setFDGenerated(true);

        await fetch('/api/detected_fds')
          .then((res) => res.json())
          .then((data) => {
            fetchOriginalFDs(data.fds || []);
            setFDGenerated(true);
          });
      }

      if (stepName === 'NormalizeTable') {
        await fetchDecomposedSchemas();
        await fetchNormalizedTables();
        addMessage('Tables normalized successfully');
      }

      if (stepName === 'ERDiagram') {
        setErDiagramGenerated(true);
      }

    } catch (error) {
      addMessage(error.message);
    }
  };

  const handleDependencyPreservation = async () => {
    try {
      await fetchOriginalFDs();
      await fetchDecomposedSchemas();

      if (!originalFDs || originalFDs.length === 0) {
        addMessage('Error: Functional Dependencies are missing or invalid.');
        return;
      }

      if (!decomposedSchemas || decomposedSchemas.length === 0) {
        addMessage('Error: Decomposed Schemas are missing or invalid.');
        return;
      }

      const message = await checkDependencyPreservation(originalFDs, decomposedSchemas);
      addMessage(message);
    } catch (error) {
      addMessage(error.message || 'Unknown error occurred during dependency preservation check.');
    }
  };

  const handleLosslessCheck = async () => {
    try {
      const message = await triggerLosslessCheck();
      addMessage(message);
      addWorkflowStep('LosslessCheck');
    } catch (error) {
      addMessage(error.message || 'Unknown error during Lossless Check');
    }
  };

  const handleActionClick = (id) => {
    switch (id) {
      case 'upload-file':
        fileInputRef.current.click();
        break;
      case 'convert-csv':
        handleBackendAction('ConvertToCSV');
        break;
      case 'clean':
        handleBackendAction('CleanModify');
        break;
      case 'fd-detection':
        handleBackendAction('FDModified');
        break;
      case 'key-detection':
        handleBackendAction('KeyDetection');
        break;
      case 'normalized-tables':
        handleBackendAction('NormalizeTable');
        break;
      case 'dependency-preservation':
        handleDependencyPreservation();
        break;
      case 'lossless-check':
        handleLosslessCheck();
        break;
      case 'er-diagram':
        handleBackendAction('ERDiagram');
        break;
      case 'refresh-workflow':
        window.location.reload();
        break;
      default:
        break;
    }
  };

  return (
    <div className="action-panel">
      <div className="action-panel-header">
      </div>

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        className="action-file-input"
      />

      <div className="action-grid">
        {/* Left Column */}
        <div className="action-column">
          {leftColumnActions.map((action) => (
            <button
              key={action.id}
              onClick={() => handleActionClick(action.id)}
              className="action-button"
              data-color={action.color.replace('bg-', '').replace('-500', '')}
            >
              <div className="action-icon">
                <action.icon size={28} />
              </div>
              <span className="action-label">{action.label}</span>
            </button>
          ))}
        </div>

        {/* Right Column */}
        <div className="action-column">
          {rightColumnActions.map((action) => (
            <button
              key={action.id}
              onClick={() => handleActionClick(action.id)}
              className="action-button"
              data-color={action.color.replace('bg-', '').replace('-500', '')}
            >
              <div className="action-icon">
                <action.icon size={28} />
              </div>
              <span className="action-label">{action.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* CSS directly in component for quick effect */}
    </div>
  );
};

export default ActionPanel;
