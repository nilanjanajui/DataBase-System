import React, { useEffect, useRef } from "react";
import { useStateContext } from "../context/StateContext";
import Prism from "prismjs";
// Import Prism CSS for styling (choose a theme or create your own)
import "prismjs/themes/prism-tomorrow.css"; 
// Import languages you want to support, e.g., JavaScript
import "prismjs/components/prism-jsx.min.js"; 

const CodePanel = () => {
  const { currentCode } = useStateContext();
  const codeRef = useRef(null);

  // Re-highlight whenever currentCode changes
  useEffect(() => {
    if (codeRef.current) {
      Prism.highlightElement(codeRef.current);
    }
  }, [currentCode]);

  const styles = {
    container: {
      overflowY: "auto",
      height: "100%",
      padding: 1,
      backgroundColor: "#60606073",
      color: "#8f8e8eff",
      fontFamily: "'Source Code Pro', monospace",
      fontSize: 14,
      borderRadius: 4,
      boxSizing: "border-box",
      userSelect: "text",
      whiteSpace: "pre-wrap",
      wordBreak: "break-word",
      outline: "none",
    },
  };

  return (
    <section
      className="code-panel"
      style={styles.container}
      aria-label="Code display panel"
      tabIndex={0}
    >
      <pre>
        <code ref={codeRef} className="language-jsx">
          {currentCode || "Click a button in Output Panel to see code here."}
        </code>
      </pre>
    </section>
  );
};

export default CodePanel;
