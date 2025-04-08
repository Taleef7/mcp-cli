"use client";

import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Textarea from '@/components/ui/Textarea';
import mcpClient from '@/lib/api-client';
import { parseEnvString } from '@/lib/utils';

interface AddServerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onServerAdded: () => void;
}

const formSchema = z.object({
  name: z.string().min(1, 'Server name is required'),
  command: z.string().min(1, 'Command is required'),
  args: z.string().optional(),
  env: z.string().optional(),
});

type FormData = z.infer<typeof formSchema>;

export default function AddServerModal({ isOpen, onClose, onServerAdded }: AddServerModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      command: '',
      args: '',
      env: '',
    },
  });

  const onSubmit: SubmitHandler<FormData> = async (data) => {
    try {
      setIsSubmitting(true);
      setError(null);

      // Parse args string into array
      const args = data.args ? data.args.split(' ').filter(Boolean) : [];
      
      // Parse env string into object
      const env = parseEnvString(data.env || '');

      await mcpClient.addServer(data.name, data.command, args, env);
      reset();
      onServerAdded();
    } catch (err: any) {
      setError(err.message || 'Failed to add server');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    reset();
    setError(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-lg">
        <div className="p-6">
          <h2 className="text-xl font-semibold mb-4">Add MCP Server</h2>
          
          {error && (
            <div className="mb-4 p-3 bg-red-50 text-red-800 rounded-md text-sm">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit(onSubmit)}>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Server Name
                </label>
                <Input
                  {...register('name')}
                  placeholder="e.g., playwright, airbnb"
                  error={errors.name?.message}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">
                  Command
                </label>
                <Input
                  {...register('command')}
                  placeholder="e.g., npx"
                  error={errors.command?.message}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">
                  Arguments (space separated)
                </label>
                <Input
                  {...register('args')}
                  placeholder="e.g., @playwright/mcp@latest"
                  error={errors.args?.message}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">
                  Environment Variables (KEY=VALUE, one per line)
                </label>
                <Textarea
                  {...register('env')}
                  placeholder="e.g., DISPLAY=:1"
                  error={errors.env?.message}
                  rows={4}
                />
              </div>
            </div>
            
            <div className="mt-6 flex justify-end space-x-3">
              <Button
                type="button"
                variant="outline"
                onClick={handleClose}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                isLoading={isSubmitting}
              >
                Add Server
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
} 