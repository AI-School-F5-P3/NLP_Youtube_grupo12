import React from 'react';
import Header from './Header';
import Footer from './Footer';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="relative bg-gray-100 min-h-screen">
      <Sidebar />
      {/* La clase pl-16 empuja todo el contenido principal a la derecha del sidebar */}
      <div className="pl-16 flex flex-col min-h-screen">
        <Header />
        <main className="flex-1 p-6">
          {children}
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default Layout;
