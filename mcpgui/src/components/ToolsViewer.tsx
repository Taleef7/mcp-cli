"use client";

import React, { useState, useEffect } from 'react';
import { FiChevronDown, FiChevronRight, FiRefreshCw } from 'react-icons/fi';
import Button from '@/components/ui/Button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import mcpClient, { Server, Tool } from '@/lib/api-client';
import { formatJSON } from '@/lib/utils';

export default function ToolsViewer() {
  const [servers, setServers] = useState<Server[]>([]);
  const [selectedServer, setSelectedServer] = useState<string>('');
  const [tools, setTools] = useState<Tool[]>([]);
  const [expandedTool, setExpandedTool] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [model, setModel] = useState('gpt-3.5-turbo');
  const [debugInfo, setDebugInfo] = useState<string | null>(null);

  useEffect(() => {
    const fetchServers = async () => {
      try {
        setError(null);
        const response = await mcpClient.getServers();
        if (!response || !response.servers) {
          setError('Invalid server response');
          return;
        }
        setServers(response.servers);
        if (response.servers.length > 0) {
          setSelectedServer(response.servers[0].name);
        }
      } catch (err: any) {
        setError(`Failed to fetch servers: ${err.message || err}`);
      }
    };

    fetchServers();
  }, []);

  const fetchTools = async () => {
    if (!selectedServer) return;

    try {
      setLoading(true);
      setError(null);
      setDebugInfo(null);
      setTools([]);

      console.log(`Fetching tools for server: ${selectedServer}, model: ${model}`);
      const response = await mcpClient.getTools(selectedServer, model);
      
      console.log('Tools API response:', response);
      setDebugInfo(`API Response: ${JSON.stringify(response, null, 2)}`);

      if (!response) {
        setError('Empty response from server');
        return;
      }

      if (response.error) {
        setError(`API error: ${response.error}`);
        return;
      }

      // Handle tools response
      if (response.tools) {
        if (Array.isArray(response.tools)) {
          setTools(response.tools);
          console.log(`Received ${response.tools.length} tools`);
        } else {
          setError(`Invalid tools data: ${typeof response.tools}`);
          console.error('Invalid tools data:', response.tools);
        }
      } else {
        setError('No tools data in response');
      }
    } catch (err: any) {
      setError(`Failed to fetch tools: ${err.message || err}`);
      console.error('Error fetching tools:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedServer) {
      fetchTools();
    }
  }, [selectedServer, model]);

  const toggleTool = (name: string) => {
    if (expandedTool === name) {
      setExpandedTool(null);
    } else {
      setExpandedTool(name);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Server Tools</CardTitle>
      </CardHeader>
      <CardContent>
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-800">
            {error}
          </div>
        )}

        <div className="flex flex-col space-y-4">
          <div className="flex space-x-4">
            <div className="w-2/3">
              <label className="block text-sm font-medium mb-1">
                Server
              </label>
              <select
                value={selectedServer}
                onChange={(e) => setSelectedServer(e.target.value)}
                className="w-full h-10 px-3 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-600"
                disabled={servers.length === 0 || loading}
              >
                {servers.length === 0 ? (
                  <option value="">No servers available</option>
                ) : (
                  servers.map((server) => (
                    <option key={server.name} value={server.name}>
                      {server.name}
                    </option>
                  ))
                )}
              </select>
            </div>
            <div className="w-1/3">
              <label className="block text-sm font-medium mb-1">
                Model
              </label>
              <input
                type="text"
                value={model}
                onChange={(e) => setModel(e.target.value)}
                className="w-full h-10 px-3 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-600"
                placeholder="gpt-3.5-turbo"
                disabled={loading}
              />
            </div>
          </div>

          <div>
            <Button 
              onClick={fetchTools} 
              disabled={!selectedServer || loading}
              className="flex items-center"
            >
              <FiRefreshCw className={`mr-2 ${loading ? 'animate-spin' : ''}`} />
              Refresh Tools
            </Button>
          </div>

          {loading ? (
            <div className="flex justify-center py-8">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
            </div>
          ) : (!tools || tools.length === 0) ? (
            <div className="py-4 text-center text-gray-500">
              {selectedServer
                ? `No tools available for server "${selectedServer}"`
                : 'Select a server to view available tools'}
            </div>
          ) : (
            <div className="mt-4 space-y-2">
              <h3 className="font-medium text-lg mb-2">Available Tools ({tools.length})</h3>
              {tools.map((tool) => (
                <div key={tool.name} className="border rounded-md overflow-hidden">
                  <div
                    className="flex justify-between items-center p-3 bg-gray-50 cursor-pointer"
                    onClick={() => toggleTool(tool.name)}
                  >
                    <div className="font-medium">{tool.name}</div>
                    <Button variant="ghost" size="sm">
                      {expandedTool === tool.name ? (
                        <FiChevronDown className="h-5 w-5" />
                      ) : (
                        <FiChevronRight className="h-5 w-5" />
                      )}
                    </Button>
                  </div>
                  {expandedTool === tool.name && (
                    <div className="p-3 border-t">
                      <p className="text-gray-600 mb-2">{tool.description}</p>
                      <div>
                        <h4 className="font-medium mb-1">Parameters:</h4>
                        <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto">
                          {formatJSON(tool.parameters)}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {debugInfo && (
            <div className="mt-6 border-t pt-4">
              <h3 className="text-sm font-medium mb-2">Debug Information</h3>
              <pre className="bg-gray-100 p-3 rounded text-xs overflow-auto max-h-60">
                {debugInfo}
              </pre>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
} 