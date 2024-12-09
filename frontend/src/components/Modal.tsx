import React from 'react';

interface ModalProps {
  title: string;
  children: React.ReactNode;
  onClose: () => void;
}

const Modal: React.FC<ModalProps> = ({ title, children, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-lg shadow-lg w-[90%] md:w-[50%] p-6 relative">
        <h2 className="text-lg font-bold mb-4">{title}</h2>
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-600 hover:text-gray-900"
        >
          ✕
        </button>
        <div className="mt-4">{children}</div>
      </div>
    </div>
  );
};

export default Modal;