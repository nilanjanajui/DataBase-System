import React, { useRef, useEffect } from "react";

const DraggableButton = ({ id, label, position, onDrag, onClick }) => {
  const btnRef = useRef();

  React.useEffect(() => {
    const btn = btnRef.current;
    const handleMouseDown = (e) => {
      const shiftX = e.clientX - btn.getBoundingClientRect().left;
      const shiftY = e.clientY - btn.getBoundingClientRect().top;

      const onMouseMove = (e) => {
        onDrag(id, { x: e.clientX - shiftX, y: e.clientY - shiftY });
      };

      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener(
        "mouseup",
        () => {
          document.removeEventListener("mousemove", onMouseMove);
        },
        { once: true }
      );
    };

    btn.addEventListener("mousedown", handleMouseDown);

    return () => {
      btn.removeEventListener("mousedown", handleMouseDown);
    };
  }, [id, onDrag]);

  return (
    <div
      ref={btnRef}
      onClick={() => onClick(id)}
      className="draggable-node"
      style={{
        left: position.x,
        top: position.y,
      }}
    >
      {label}
    </div>
  );
};

export default DraggableButton;
