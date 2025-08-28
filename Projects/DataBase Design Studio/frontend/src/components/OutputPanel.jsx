import React, { useEffect, useState, useRef } from 'react';
import { useStateContext } from '../context/StateContext';
import DraggableStep from './DraggableStep';
import axios from 'axios';

const STORAGE_KEY = 'workflowStepPositions';

const OutputPanel = () => {
  const { workflowSteps, setCurrentCode } = useStateContext();
  const [positions, setPositions] = useState({});
  const [boxWidths, setBoxWidths] = useState({});
  const [scale, setScale] = useState(1);
  const containerRef = useRef(null);

  const [controlPoints, setControlPoints] = useState({});
  const positionsInitialized = useRef(false);

  // Undo / Redo stacks
  const [undoStack, setUndoStack] = useState([]);
  const [redoStack, setRedoStack] = useState([]);

  // Current focused step index for step-by-step navigation
  const [currentStepIndex, setCurrentStepIndex] = useState(null);

  // Manage visible and removed steps separately for reverse/forward buttons
  const [visibleSteps, setVisibleSteps] = useState([]);
  const [removedSteps, setRemovedSteps] = useState([]);

  const boxHeight = 44;
  const horizontalSpacing = 60;
  const verticalSpacing = 60;

  // Map internal step IDs to user-friendly display names
  const stepDisplayNames = {
    Upload: 'Upload',
    CleanModify: 'Noise Clean',
    FDModified: 'FD Detection',
    NormalizeTable: 'Normalization',
    LosslessCheck: 'Lossless Decomposition',
    ERDiagram: 'ER Diagram',
    ConvertToCSV: 'CSV Converter',
    KeyDetection: 'Key Detector',
    DependencyPreservation: 'Check Dependency Preservation',
  };

  // Load saved positions on mount
  useEffect(() => {
    const savedPositions = localStorage.getItem(STORAGE_KEY);
    if (savedPositions) {
      try {
        const parsedPositions = JSON.parse(savedPositions);
        setPositions(parsedPositions);
        positionsInitialized.current = true;
      } catch {
        console.warn('Failed to parse saved positions');
      }
    }
  }, []);

  // Initialize visibleSteps and removedSteps when workflowSteps changes
  useEffect(() => {
    setVisibleSteps(workflowSteps);
    setRemovedSteps([]);
  }, [workflowSteps]);

  // Initialize default positions if none saved, after we know box widths
  useEffect(() => {
    if (positionsInitialized.current) return;
    if (!containerRef.current) return;
    if (workflowSteps.length === 0) return;

    // Wait until all box widths are measured for all workflowSteps
    if (workflowSteps.some((step) => !boxWidths[step])) return;

    const containerWidth = containerRef.current.clientWidth;
    const initialPositions = {};

    let x = 50;
    let y = 60;

    workflowSteps.forEach((step) => {
      const width = boxWidths[step] || 140;

      if (x + width > containerWidth - 20) {
        x = 50;
        y += boxHeight + verticalSpacing;
      }
      initialPositions[step] = { x, y };
      x += width + horizontalSpacing;
    });

    setPositions((prev) => ({ ...prev, ...initialPositions }));
    positionsInitialized.current = true;
  }, [workflowSteps, boxWidths]);

  // Save positions to localStorage when changed
  useEffect(() => {
    if (positionsInitialized.current) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(positions));
    }
  }, [positions]);

  // Ensure currentStepIndex stays valid when workflowSteps or visibleSteps change
  useEffect(() => {
    if (currentStepIndex == null) return;
    if (currentStepIndex >= visibleSteps.length) {
      setCurrentStepIndex(visibleSteps.length - 1);
    }
  }, [visibleSteps, currentStepIndex]);

  // Handle drag of step boxes with undo stack update
  const handlePositionChange = (step, pos) => {
    setPositions((prev) => {
      setUndoStack((undoPrev) => [...undoPrev, prev]);
      setRedoStack([]);
      return { ...prev, [step]: pos };
    });
  };

  const handleClickStep = async (step) => {
    try {
      const response = await axios.get(`/api/code/${step}`);
      setCurrentCode(response.data.code || '');
    } catch {
      setCurrentCode('Failed to load code');
    }

    const idx = visibleSteps.indexOf(step);
    if (idx !== -1) setCurrentStepIndex(idx);
  };

  // Undo handler: undo 2 steps at once
  const handleUndo = () => {
    if (undoStack.length === 0) return;

    setPositions((currentPositions) => {
      let newUndoStack = [...undoStack];
      let newRedoStack = [...redoStack, currentPositions];

      let previousPositions;
      for (let i = 0; i < 2; i++) {
        if (newUndoStack.length === 0) break;
        previousPositions = newUndoStack.pop();
        newRedoStack.push(previousPositions);
      }

      setUndoStack(newUndoStack);
      setRedoStack(newRedoStack);

      return previousPositions || currentPositions;
    });
  };

  // Redo handler: redo 2 steps at once
  const handleRedo = () => {
    if (redoStack.length === 0) return;

    setPositions((currentPositions) => {
      let newRedoStack = [...redoStack];
      let newUndoStack = [...undoStack, currentPositions];

      let nextPositions;
      for (let i = 0; i < 2; i++) {
        if (newRedoStack.length === 0) break;
        nextPositions = newRedoStack.pop();
        newUndoStack.push(nextPositions);
      }

      setRedoStack(newRedoStack);
      setUndoStack(newUndoStack);

      return nextPositions || currentPositions;
    });
  };

  // Helper cubic Bézier function for point at parameter t
  function cubicBezierPoint(t, P0, P1, P2, P3) {
    const u = 1 - t;
    const tt = t * t;
    const uu = u * u;
    const uuu = uu * u;
    const ttt = tt * t;

    const x =
      uuu * P0.x +
      3 * uu * t * P1.x +
      3 * u * tt * P2.x +
      ttt * P3.x;
    const y =
      uuu * P0.y +
      3 * uu * t * P1.y +
      3 * u * tt * P2.y +
      ttt * P3.y;

    return { x, y };
  }

  const renderLines = () => {
    const dotRadius = 4.5;
    const lines = [];

    const t1 = 0.25; // parameter for first dot on curve
    const t2 = 0.75; // parameter for second dot on curve

    for (let i = 0; i < visibleSteps.length - 1; i++) {
      const from = positions[visibleSteps[i]];
      const to = positions[visibleSteps[i + 1]];

      if (from && to) {
        const fromWidth = boxWidths[visibleSteps[i]] || 140;

        const padding = 6; // padding so lines don't overlap box edges

        // Start point at right edge center of "from" box
        const P0 = {
          x: from.x + fromWidth + padding,
          y: from.y + boxHeight / 2,
        };

        // End point at left edge center of "to" box
        const P3 = {
          x: to.x - padding,
          y: to.y + boxHeight / 2,
        };

        const cp = controlPoints[i] || {};

        let P1, P2;

        if (cp.c1 && cp.c2) {
          P1 = cp.c1;
          P2 = cp.c2;
        } else {
          if (Math.abs(P3.x - P0.x) > Math.abs(P3.y - P0.y)) {
            P1 = { x: P0.x + (P3.x - P0.x) / 2, y: P0.y };
            P2 = { x: P0.x + (P3.x - P0.x) / 2, y: P3.y };
          } else {
            P1 = { x: P0.x, y: P0.y + (P3.y - P0.y) / 2 };
            P2 = { x: P3.x, y: P0.y + (P3.y - P0.y) / 2 };
          }
        }

        // Compute dot positions on the curve
        const dot1Pos = cubicBezierPoint(t1, P0, P1, P2, P3);
        const dot2Pos = cubicBezierPoint(t2, P0, P1, P2, P3);

        // Build path string
        const d = `M${P0.x},${P0.y} C${P1.x},${P1.y} ${P2.x},${P2.y} ${P3.x},${P3.y}`;

        lines.push(
          <path
            key={`line-${i}`}
            d={d}
            fill="none"
            stroke="rgba(184, 212, 249, 0.9)"
            strokeWidth="1.5"
            markerEnd="url(#arrowhead)"
          />
        );

        // Draggable dots placed on curve at dot1Pos and dot2Pos
        lines.push(
          <circle
            key={`dot1-${i}`}
            cx={dot1Pos.x}
            cy={dot1Pos.y}
            r={dotRadius}
            fill="rgba(70, 130, 180, 0.9)"
            stroke="#333"
            strokeWidth="1.5"
            style={{ cursor: 'grab' }}
            pointerEvents="all"
            onMouseDown={(e) => onMouseDownControlPoint(i, 'c1', e)}
          />,
          <circle
            key={`dot2-${i}`}
            cx={dot2Pos.x}
            cy={dot2Pos.y}
            r={dotRadius}
            fill="rgba(70, 130, 180, 0.9)"
            stroke="#333"
            strokeWidth="1.5"
            style={{ cursor: 'grab' }}
            pointerEvents="all"
            onMouseDown={(e) => onMouseDownControlPoint(i, 'c2', e)}
          />
        );
      }
    }
    return lines;
  };

  const zoomIn = () => setScale((s) => Math.min(2, +(s + 0.1).toFixed(2)));
  const zoomOut = () => setScale((s) => Math.max(0.5, +(s - 0.1).toFixed(2)));

  // Drag handlers for control points
  const draggingRef = useRef(null);

  const onMouseDownControlPoint = (lineIndex, pointKey, e) => {
    e.preventDefault();
    e.stopPropagation();
    draggingRef.current = { lineIndex, pointKey };

    window.addEventListener('mousemove', onMouseMoveControlPoint);
    window.addEventListener('mouseup', onMouseUpControlPoint);
  };

  const onMouseMoveControlPoint = (e) => {
    if (!draggingRef.current) return;

    const { lineIndex, pointKey } = draggingRef.current;
    const containerRect = containerRef.current.getBoundingClientRect();
    const mouseX = (e.clientX - containerRect.left) / scale;
    const mouseY = (e.clientY - containerRect.top) / scale;

    setControlPoints((prev) => ({
      ...prev,
      [lineIndex]: {
        ...prev[lineIndex],
        [pointKey]: { x: mouseX, y: mouseY },
      },
    }));
  };

  const onMouseUpControlPoint = () => {
    draggingRef.current = null;
    window.removeEventListener('mousemove', onMouseMoveControlPoint);
    window.removeEventListener('mouseup', onMouseUpControlPoint);
  };

  // Handle width updates from DraggableStep
  const handleSizeChange = (step, width) => {
    setBoxWidths((prev) => {
      if (prev[step] === width) return prev;
      return { ...prev, [step]: width };
    });
  };

  // CENTER / NAVIGATION helpers: go to a specific step index (centers it + optionally loads code)
  const goToIndex = (idx) => {
    if (!containerRef.current) return;
    if (!positionsInitialized.current) return;
    if (idx == null || idx < 0 || idx >= visibleSteps.length) return;

    const step = visibleSteps[idx];
    const pos = positions[step];
    if (!pos) return;

    const boxW = boxWidths[step] || 140;
    const container = containerRef.current;
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    // positions are in unscaled coords; canvas is scaled, so multiply by scale to compute scroll target
    const targetLeft = Math.round(pos.x * scale - containerWidth / 2 + (boxW * scale) / 2);
    const targetTop = Math.round(pos.y * scale - containerHeight / 2 + (boxHeight * scale) / 2);

    container.scrollTo({
      left: Math.max(0, targetLeft),
      top: Math.max(0, targetTop),
      behavior: 'smooth',
    });

    setCurrentStepIndex(idx);

    // optionally load code for that step (keeps UI consistent with clicking a step)
    handleClickStep(step);
  };

  // Step backward (reverse) one step at a time by removing the last visible step
  const prevStep = () => {
    if (visibleSteps.length === 0) return;

    setVisibleSteps((prevVisible) => {
      if (prevVisible.length === 0) return prevVisible;

      const newVisible = prevVisible.slice(0, -1);
      const removed = prevVisible[prevVisible.length - 1];

      setRemovedSteps((prevRemoved) => [removed, ...prevRemoved]);

      // After removing, go to new last visible step if exists
      if (newVisible.length > 0) {
        goToIndex(newVisible.length - 1);
      } else {
        // No visible steps left
        setCurrentStepIndex(null);
        setCurrentCode('');
      }

      return newVisible;
    });
  };

  // Step forward one step at a time by restoring the first removed step
  const nextStep = () => {
    if (removedSteps.length === 0) return;

    setRemovedSteps((prevRemoved) => {
      const [restored, ...rest] = prevRemoved;

      setVisibleSteps((prevVisible) => {
        const newVisible = [...prevVisible, restored];
        goToIndex(newVisible.length - 1);
        return newVisible;
      });

      return rest;
    });
  };

  return (
    <div
      className="output-panel"
      style={{
        width: '100%',
        height: '100%',
        position: 'relative',
        overflow: 'auto',
        padding: 20,
      }}
      ref={containerRef}
    >
      {/* Zoom controls + Undo/Redo + Step navigation */}
      <div
        className="zoom-controls"
        style={{
          position: 'absolute',
          top: 5,
          right: 5,
          zIndex: 5,
          display: 'flex',
          gap: 6,
          alignItems: 'center',
        }}
      >
        <button
          className="zoom-btn"
          onClick={zoomIn}
          title="Zoom in"
          style={{ textAlign: 'center' }}
        >
          +
        </button>
        <button
          className="zoom-btn"
          onClick={zoomOut}
          title="Zoom out"
          style={{ textAlign: 'center' }}
        >
          −
        </button>

        <button
          className="undo-btn"
          onClick={handleUndo}
          disabled={undoStack.length === 0}
          title="Undo (2 steps)"
          style={{ cursor: undoStack.length === 0 ? 'not-allowed' : 'pointer' }}
        >
          ↺
        </button>
        <button
          className="redo-btn"
          onClick={handleRedo}
          disabled={redoStack.length === 0}
          title="Redo (2 steps)"
          style={{ cursor: redoStack.length === 0 ? 'not-allowed' : 'pointer' }}
        >
          ↻
        </button>

        {/* Step backward / forward controls */}
        <button
          className="step-back-btn"
          onClick={prevStep}
          title="Step backward (remove last workflow box)"
          disabled={visibleSteps.length === 0}
          style={{
            cursor: visibleSteps.length === 0 ? 'not-allowed' : 'pointer',
          }}
        >
          ◀
        </button>

        <button
          className="step-forward-btn"
          onClick={nextStep}
          title="Step forward (restore workflow box)"
          disabled={removedSteps.length === 0}
          style={{
            cursor: removedSteps.length === 0 ? 'not-allowed' : 'pointer',
          }}
        >
          ▶
        </button>
      </div>

      {/* Canvas wrapper */}
      <div
        className="canvas-wrapper"
        style={{
          transform: `scale(${scale})`,
          transformOrigin: '0 0',
          position: 'relative',
          minHeight: '100%',
          width: '100%',
        }}
      >
        {/* SVG lines and draggable dots */}
        <svg
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
            overflow: 'visible',
            top: 0,
            left: 0,
          }}
        >
          <defs>
            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="7"
              refX="10"
              refY="3.5"
              orient="auto"
              fill="rgba(103, 121, 136, 0.9)"
            >
              <polygon points="0 0, 10 3.5, 0 7" />
            </marker>
          </defs>
          {renderLines()}
        </svg>

        {/* Draggable steps from visibleSteps */}
        {visibleSteps.map((step, index) => (
          <DraggableStep
            key={step}
            step={step}
            displayName={stepDisplayNames[step] || step} // Pass friendly name here
            position={positions[step] || { x: 0, y: 0 }}
            onPositionChange={handlePositionChange}
            onClick={handleClickStep}
            isFirst={index === 0}
            onSizeChange={handleSizeChange}
            isActive={index === currentStepIndex} // highlight if active — requires DraggableStep to use this prop
          />
        ))}
      </div>
    </div>
  );
};

export default OutputPanel;
