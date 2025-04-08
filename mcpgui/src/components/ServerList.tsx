"use client";

import React, { useState, useEffect } from 'react';
import { FiEdit, FiTrash2, FiPlus } from 'react-icons/fi';
import Button from '@/components/ui/Button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Server } from '@/lib/api-client';
import mcpClient from '@/lib/api-client';
import AddServerModal from '@/components/AddServerModal';
import EditServerModal from '@/components/EditServerModal';
import { formatJSON } from '@/lib/utils';

export default function ServerList() {
  const [servers, setServers] = useState<Server[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedServer, setSelectedServer] = useState<Server | null>(null);
  const [expandedServer, setExpandedServer] = useState<string | null>(null);

  const fetchServers = async () => {
    try {
      setLoading(true);
      const response = await mcpClient.getServers();
      setServers(response.servers);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch servers');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServers();
  }, []);

  const handleDeleteServer = async (name: string) => {
    if (!confirm(`Are you sure you want to delete server "${name}"?`)) {
      return;
    }

    try {
      await mcpClient.removeServer(name);
      setServers(servers.filter(server => server.name !== name));
    } catch (err: any) {
      setError(err.message || `Failed to delete server "${name}"`);
    }
  };

  const handleEditServer = (server: Server) => {
    setSelectedServer(server);
    setIsEditModalOpen(true);
  };

  const handleServerAdded = () => {
    fetchServers();
    setIsAddModalOpen(false);
  };

  const handleServerUpdated = () => {
    fetchServers();
    setIsEditModalOpen(false);
    setSelectedServer(null);
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="py-6">
          <div className="flex justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>MCP Servers</CardTitle>
          <Button onClick={() => setIsAddModalOpen(true)} size="sm">
            <FiPlus className="mr-1" /> Add Server
          </Button>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-800">
              {error}
            </div>
          )}

          {servers.length === 0 ? (
            <div className="py-4 text-center text-gray-500">
              No servers configured. Click "Add Server" to add a new MCP server.
            </div>
          ) : (
            <div className="space-y-4">
              {servers.map((server) => (
                <div
                  key={server.name}
                  className="rounded-md border border-gray-200 overflow-hidden"
                >
                  <div 
                    className="flex items-center justify-between bg-gray-50 p-4 cursor-pointer"
                    onClick={() => setExpandedServer(expandedServer === server.name ? null : server.name)}
                  >
                    <div className="font-medium">{server.name}</div>
                    <div className="flex space-x-2">
                      <Button 
                        variant="ghost" 
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditServer(server);
                        }}
                      >
                        <FiEdit className="h-4 w-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteServer(server.name);
                        }}
                      >
                        <FiTrash2 className="h-4 w-4 text-red-600" />
                      </Button>
                    </div>
                  </div>
                  
                  {expandedServer === server.name && (
                    <div className="p-4 bg-gray-50 border-t border-gray-200">
                      <div className="mb-2">
                        <span className="font-semibold">Command: </span>
                        {server.command} {server.args.join(' ')}
                      </div>
                      {Object.keys(server.env || {}).length > 0 && (
                        <div>
                          <span className="font-semibold">Environment: </span>
                          <pre className="mt-1 rounded bg-gray-100 p-2 text-xs overflow-auto">
                            {formatJSON(server.env)}
                          </pre>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <AddServerModal 
        isOpen={isAddModalOpen} 
        onClose={() => setIsAddModalOpen(false)} 
        onServerAdded={handleServerAdded}
      />

      <EditServerModal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setSelectedServer(null);
        }}
        onServerUpdated={handleServerUpdated}
        server={selectedServer}
      />
    </>
  );
} 