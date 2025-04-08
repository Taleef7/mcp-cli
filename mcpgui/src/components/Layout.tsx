"use client";

import React, { ReactNode, useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FiHome, FiServer, FiSend, FiTool, FiSettings } from 'react-icons/fi';
import mcpClient from '@/lib/api-client';

interface LayoutProps {
  children: ReactNode;
}

interface NavItemProps {
  href: string;
  icon: React.ReactNode;
  text: string;
  isActive: boolean;
}

const NavItem = ({ href, icon, text, isActive }: NavItemProps) => (
  <Link
    href={href}
    className={`flex items-center px-4 py-2 rounded-md transition-colors ${
      isActive
        ? 'bg-blue-100 text-blue-900'
        : 'text-gray-700 hover:bg-gray-100'
    }`}
  >
    <div className="mr-3">{icon}</div>
    <span>{text}</span>
  </Link>
);

export default function Layout({ children }: LayoutProps) {
  const pathname = usePathname();
  const [apiStatus, setApiStatus] = useState<string>('Checking...');
  const [statusColor, setStatusColor] = useState<string>('text-yellow-500');

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const status = await mcpClient.getStatus();
        setApiStatus(`Connected (v${status.version})`);
        setStatusColor('text-green-600');
      } catch (error) {
        setApiStatus('Disconnected');
        setStatusColor('text-red-600');
      }
    };

    checkApiStatus();
    const interval = setInterval(checkApiStatus, 10000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">MCP CLI GUI</h1>
            <div className={`ml-4 text-sm ${statusColor}`}>
              API: {apiStatus}
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row gap-6">
          {/* Sidebar */}
          <aside className="md:w-64 flex-shrink-0">
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <nav className="space-y-2">
                <NavItem
                  href="/"
                  icon={<FiHome className="h-5 w-5" />}
                  text="Dashboard"
                  isActive={pathname === '/'}
                />
                <NavItem
                  href="/servers"
                  icon={<FiServer className="h-5 w-5" />}
                  text="Servers"
                  isActive={pathname === '/servers'}
                />
                <NavItem
                  href="/query"
                  icon={<FiSend className="h-5 w-5" />}
                  text="Run Query"
                  isActive={pathname === '/query'}
                />
                <NavItem
                  href="/tools"
                  icon={<FiTool className="h-5 w-5" />}
                  text="Tools"
                  isActive={pathname === '/tools'}
                />
                <NavItem
                  href="/config"
                  icon={<FiSettings className="h-5 w-5" />}
                  text="Configuration"
                  isActive={pathname === '/config'}
                />
              </nav>
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
} 