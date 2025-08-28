import React from 'react';
import { useDrag } from '@use-gesture/react';

const DraggableStep = ({ step, position, onPositionChange, onClick, isFirst, displayName }) => {
  const bind = useDrag(({ offset: [x, y] }) => {
    onPositionChange(step, { x, y });
  });

  return (
    <div
      {...bind()}
      onClick={() => onClick(step)}
      className="draggable-node"
      style={{
        left: position.x,
        top: position.y,
      }}
    >
      {/* Show left dot only if NOT the first box */}
      {!isFirst && <div className="connection-dot left-dot" />}

      {/* Step label */}
      <div className="step-label">{displayName || step}</div>

      {/* Always show right dot */}
      <div className="connection-dot right-dot" />
    </div>
  );
};

export default DraggableStep;
