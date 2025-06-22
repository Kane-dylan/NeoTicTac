import React from "react";

const Modal = ({ isOpen, onClose, children, closeOnOverlayClick = true }) => {
  if (!isOpen) return null;

  const handleOverlayClick = (e) => {
    if (closeOnOverlayClick && e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      onClick={handleOverlayClick}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-cyber-black/80 backdrop-blur-sm animate-fade-in" />

      {/* Modal Content */}
      <div className="relative z-10 animate-float-up">{children}</div>
    </div>
  );
};

export default Modal;
