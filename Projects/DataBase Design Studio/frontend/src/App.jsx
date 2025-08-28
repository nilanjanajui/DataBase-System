import React, { useEffect, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; //	Navigation between different pages/views without reloading
import { StateProvider } from './context/StateContext';
import { Helmet } from 'react-helmet';
import {
  FaDatabase,
  FaTable,
  FaProjectDiagram,
  FaCode,
  FaCommentAlt,
  FaStream
} from 'react-icons/fa'; // FontAwesome icons inside React components

import ActionPanel from './components/ActionPanel';
import OutputPanel from './components/OutputPanel';
import CodePanel from './components/CodePanel';
import MessagePanel from './components/messagePanel';
import NormalizedTableView from './components/TableView';
import ERDiagramPage from './components/ERDiagramPage';
import FDPage from './components/FDPage';

import './style.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

// Move STORAGE_KEYS outside component to avoid eslint dependency warnings
const STORAGE_KEYS = {
  leftWidth: 'dbstudio-leftWidth',
  centerWidth: 'dbstudio-centerWidth',
  rightWidth: 'dbstudio-rightWidth',
  messagesHeight: 'dbstudio-messagesHeight',
  codeHeight: 'dbstudio-codeHeight',
};

const PanelContainer = ({ children, title, icon }) => (
  <div className="panel-base">
    <div className="panel-header">
      <h3 className="panel-title">
        {icon && React.cloneElement(icon, { className: 'panel-icon' })}
        {title}
      </h3>
    </div>
    <div className="panel-content">{children}</div>
  </div>
);

const MainLayout = () => {
  // Refs for horizontal resizing
  const leftRef = useRef(null);
  const centerRef = useRef(null);
  const rightRef = useRef(null);

  // Refs for vertical resizing inside right panel
  const messagesRef = useRef(null);
  const codeRef = useRef(null);

  // Restore saved sizes on mount
  useEffect(() => {
    const leftWidth = localStorage.getItem(STORAGE_KEYS.leftWidth);
    const centerWidth = localStorage.getItem(STORAGE_KEYS.centerWidth);
    const rightWidth = localStorage.getItem(STORAGE_KEYS.rightWidth);
    const messagesHeight = localStorage.getItem(STORAGE_KEYS.messagesHeight);
    const codeHeight = localStorage.getItem(STORAGE_KEYS.codeHeight);

    if (leftWidth && leftRef.current) {
      leftRef.current.style.flex = `0 0 ${leftWidth}px`;
    }
    if (centerWidth && centerRef.current) {
      centerRef.current.style.flex = `0 0 ${centerWidth}px`;
    }
    if (rightWidth && rightRef.current) {
      rightRef.current.style.flex = `0 0 ${rightWidth}px`;
    }
    if (messagesHeight && messagesRef.current) {
      messagesRef.current.style.flex = `0 0 ${messagesHeight}px`;
    }
    if (codeHeight && codeRef.current) {
      codeRef.current.style.flex = `0 0 ${codeHeight}px`;
    }
  }, []);

  useEffect(() => {
    // ----- Horizontal resizing (left <-> center and center <-> right) -----
    const leftCenterHandle = document.querySelector('.resize-handle-x.left-center');  // for handleing resizeable panels
    const centerRightHandle = document.querySelector('.resize-handle-x.center-right');

    const minLeftWidth = 150;
    const minCenterWidth = 200;
    const minRightWidth = 200;

    function setupHorizontalResize(handle, leftEl, rightEl, minLeft, minRight, leftKey, rightKey) {
      let startX = 0;
      let startLeftWidth = 0;
      let startRightWidth = 0;

      function onMouseMove(e) {
        let dx = e.clientX - startX;
        let newLeftWidth = startLeftWidth + dx;
        let newRightWidth = startRightWidth - dx;

        // Clamp widths
        if (newLeftWidth < minLeft) {
          newLeftWidth = minLeft;
          newRightWidth = startLeftWidth + startRightWidth - minLeft;
        } else if (newRightWidth < minRight) {
          newRightWidth = minRight;
          newLeftWidth = startLeftWidth + startRightWidth - minRight;
        }

        leftEl.style.flex = `0 0 ${newLeftWidth}px`;
        rightEl.style.flex = `0 0 ${newRightWidth}px`;
      }

      function onMouseUp() {
        // Save widths in localStorage
        localStorage.setItem(leftKey, leftEl.getBoundingClientRect().width);
        localStorage.setItem(rightKey, rightEl.getBoundingClientRect().width);

        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
      }

      function onMouseDown(e) {
        e.preventDefault();
        startX = e.clientX;
        startLeftWidth = leftEl.getBoundingClientRect().width;
        startRightWidth = rightEl.getBoundingClientRect().width;

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
      }

      handle.addEventListener('mousedown', onMouseDown);

      return () => {
        handle.removeEventListener('mousedown', onMouseDown);
      };
    }

    // ----- Vertical resizing inside right panel (messages <-> code) -----
    const verticalHandle = document.querySelector('.resize-handle-y.messages-code');

    const minMessagesHeight = 80;
    const minCodeHeight = 80;

    function setupVerticalResize(handle, topEl, bottomEl, minTop, minBottom, topKey, bottomKey) {
      let startY = 0;
      let startTopHeight = 0;
      let startBottomHeight = 0;

      function onMouseMove(e) {
        let dy = e.clientY - startY;
        let newTopHeight = startTopHeight + dy;
        let newBottomHeight = startBottomHeight - dy;

        // Clamp heights
        if (newTopHeight < minTop) {
          newTopHeight = minTop;
          newBottomHeight = startTopHeight + startBottomHeight - minTop;
        } else if (newBottomHeight < minBottom) {
          newBottomHeight = minBottom;
          newTopHeight = startTopHeight + startBottomHeight - minBottom;
        }

        topEl.style.flex = `0 0 ${newTopHeight}px`;
        bottomEl.style.flex = `0 0 ${newBottomHeight}px`;
      }

      function onMouseUp() {
        // Save heights in localStorage
        localStorage.setItem(topKey, topEl.getBoundingClientRect().height);
        localStorage.setItem(bottomKey, bottomEl.getBoundingClientRect().height);

        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
      }

      function onMouseDown(e) {
        e.preventDefault();
        startY = e.clientY;
        startTopHeight = topEl.getBoundingClientRect().height;
        startBottomHeight = bottomEl.getBoundingClientRect().height;

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
      }

      handle.addEventListener('mousedown', onMouseDown);

      return () => {
        handle.removeEventListener('mousedown', onMouseDown);
      };
    }

    const cleanups = [];
    if (leftCenterHandle && leftRef.current && centerRef.current) {
      cleanups.push(
        setupHorizontalResize(
          leftCenterHandle,
          leftRef.current,
          centerRef.current,
          minLeftWidth,
          minCenterWidth,
          STORAGE_KEYS.leftWidth,
          STORAGE_KEYS.centerWidth
        )
      );
    }
    if (centerRightHandle && centerRef.current && rightRef.current) {
      cleanups.push(
        setupHorizontalResize(
          centerRightHandle,
          centerRef.current,
          rightRef.current,
          minCenterWidth,
          minRightWidth,
          STORAGE_KEYS.centerWidth,
          STORAGE_KEYS.rightWidth
        )
      );
    }
    if (verticalHandle && messagesRef.current && codeRef.current) {
      cleanups.push(
        setupVerticalResize(
          verticalHandle,
          messagesRef.current,
          codeRef.current,
          minMessagesHeight,
          minCodeHeight,
          STORAGE_KEYS.messagesHeight,
          STORAGE_KEYS.codeHeight
        )
      );
    }

    return () => {
      cleanups.forEach((cleanup) => cleanup && cleanup());
    };
  }, []);

  return (
    <div className="app-container">
      {/* Left panel */}
      <div className="left-panel" ref={leftRef} style={{ flex: '0 0 240px' }}>
        <PanelContainer title="DataBase Tools" icon={<FaDatabase />}>
          <ActionPanel />
        </PanelContainer>
      </div>

      {/* Horizontal resize handle between left and center */}
      <div className="resize-handle-x left-center" />

      {/* Center panel */}
      <div className="center-panel" ref={centerRef} style={{ flex: '1 1 auto' }}>
        <PanelContainer title="DataBase Workflow" icon={<FaTable />}>
          <OutputPanel />
        </PanelContainer>
      </div>

      {/* Horizontal resize handle between center and right */}
      <div className="resize-handle-x center-right" />

      {/* Right panel */}
      <div
        className="right-panel"
        ref={rightRef}
        style={{ flex: '0 0 240px', display: 'flex', flexDirection: 'column' }}
      >
        {/* Messages panel with vertical resize */}
        <div
          ref={messagesRef}
          style={{ flex: '0 0 150px', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}
        >
          <PanelContainer title="Messages" icon={<FaCommentAlt />}>
            <MessagePanel />
          </PanelContainer>
        </div>

        {/* Vertical resize handle between messages and code */}
        <div className="resize-handle-y messages-code" />

        {/* Code panel */}
        <div
          ref={codeRef}
          style={{ flex: '1 1 auto', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}
        >
          <PanelContainer title="Generated Code" icon={<FaCode />}>
            <CodePanel />
          </PanelContainer>
        </div>
      </div>
    </div>
  );
};

const App = () => {
  return (
    <StateProvider>
      <Helmet>
        <title>Database Design Studio</title>
        <meta
          name="description"
          content="Tool for creating database designs and ER diagrams"
        />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </Helmet>

      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />} />
          <Route
            path="/table-view"
            element={
              <PanelContainer title="Normalized Tables" icon={<FaTable />}>
                <NormalizedTableView />
              </PanelContainer>
            }
          />
          <Route
            path="/er-diagram"
            element={
              <PanelContainer title="ER Diagram" icon={<FaProjectDiagram />}>
                <ERDiagramPage />
              </PanelContainer>
            }
          />
          <Route
            path="/fd-view"
            element={
              <PanelContainer title="Detected Functional Dependencies" icon={<FaStream />}>
                <FDPage />
              </PanelContainer>
            }
          />
        </Routes>
      </Router>

      {/* SVG Arrowhead Definitions */}
      <svg className="svg-defs" style={{ display: 'none' }}>
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill="#1a73e8" />
          </marker>
        </defs>
      </svg>
    </StateProvider>
  );
};

export default App;
