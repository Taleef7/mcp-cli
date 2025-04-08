"use client";

import React, { useState, useEffect } from 'react';
import { FiSend } from 'react-icons/fi';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Textarea from '@/components/ui/Textarea';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import mcpClient, { Server } from '@/lib/api-client';

export default function QueryRunner() {
  const [servers, setServers] = useState<Server[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Form state
  const [selectedServer, setSelectedServer] = useState<string>('');
  const [model, setModel] = useState<string>('gpt-3.5-turbo');
  const [query, setQuery] = useState<string>('');
  const [formErrors, setFormErrors] = useState<{
    server?: string;
    model?: string;
    query?: string;
  }>({});

  useEffect(() => {
    const fetchServers = async () => {
      try {
        setLoading(true);
        const response = await mcpClient.getServers();
        setServers(response.servers);
        
        // Set default server if available
        if (response.servers.length > 0) {
          setSelectedServer(response.servers[0].name);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to fetch servers');
      } finally {
        setLoading(false);
      }
    };

    fetchServers();
  }, []);

  const validateForm = () => {
    const errors: {
      server?: string;
      model?: string;
      query?: string;
    } = {};
    
    if (!selectedServer) {
      errors.server = 'Server is required';
    }
    
    if (!query.trim()) {
      errors.query = 'Query is required';
    }
    
    setFormErrors(errors);
    
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    try {
      setIsSubmitting(true);
      setError(null);
      setResult(null);

      const response = await mcpClient.executeQuery(
        selectedServer,
        query,
        model
      );

      setResult(response.result);
    } catch (err: any) {
      setError(err.message || 'Failed to execute query');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Run MCP Query</CardTitle>
      </CardHeader>
      <CardContent>
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-800">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">
              Server
            </label>
            <select
              value={selectedServer}
              onChange={(e) => setSelectedServer(e.target.value)}
              className="w-full h-10 px-3 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-600"
              disabled={loading || servers.length === 0}
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
            {formErrors.server && (
              <p className="mt-1 text-sm text-red-600">{formErrors.server}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Model
            </label>
            <Input
              value={model}
              onChange={(e) => setModel(e.target.value)}
              placeholder="e.g., gpt-3.5-turbo"
              error={formErrors.model}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Query
            </label>
            <Textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your query..."
              rows={5}
              error={formErrors.query}
            />
          </div>

          <div className="flex justify-end">
            <Button
              type="submit"
              disabled={loading || servers.length === 0 || !selectedServer}
              isLoading={isSubmitting}
            >
              <FiSend className="mr-2" />
              Execute Query
            </Button>
          </div>
        </form>

        {result && (
          <div className="mt-6">
            <h3 className="text-lg font-medium mb-2">Result</h3>
            <div className="rounded-md border border-gray-200 bg-gray-50 p-4 whitespace-pre-wrap">
              {result}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
} 