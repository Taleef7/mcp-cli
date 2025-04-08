"use client";

import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { FiUpload, FiDownload } from 'react-icons/fi';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import mcpClient from '@/lib/api-client';

const importSchema = z.object({
  importPath: z.string().min(1, 'Import path is required'),
});

const exportSchema = z.object({
  exportPath: z.string().min(1, 'Export path is required'),
});

type ImportFormData = z.infer<typeof importSchema>;
type ExportFormData = z.infer<typeof exportSchema>;

export default function ConfigManager() {
  const [importError, setImportError] = useState<string | null>(null);
  const [exportError, setExportError] = useState<string | null>(null);
  const [importSuccess, setImportSuccess] = useState<string | null>(null);
  const [exportSuccess, setExportSuccess] = useState<string | null>(null);
  const [isImporting, setIsImporting] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  const importForm = useForm<ImportFormData>({
    resolver: zodResolver(importSchema),
    defaultValues: {
      importPath: '',
    },
  });

  const exportForm = useForm<ExportFormData>({
    resolver: zodResolver(exportSchema),
    defaultValues: {
      exportPath: '',
    },
  });

  const onImport: SubmitHandler<ImportFormData> = async (data) => {
    try {
      setIsImporting(true);
      setImportError(null);
      setImportSuccess(null);

      const response = await mcpClient.importConfig(data.importPath);
      setImportSuccess(`Configuration imported successfully from ${data.importPath}`);
      importForm.reset();
    } catch (err: any) {
      setImportError(err.message || 'Failed to import configuration');
    } finally {
      setIsImporting(false);
    }
  };

  const onExport: SubmitHandler<ExportFormData> = async (data) => {
    try {
      setIsExporting(true);
      setExportError(null);
      setExportSuccess(null);

      const response = await mcpClient.exportConfig(data.exportPath);
      setExportSuccess(`Configuration exported successfully to ${data.exportPath}`);
      exportForm.reset();
    } catch (err: any) {
      setExportError(err.message || 'Failed to export configuration');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Configuration</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-6 md:grid-cols-2">
          {/* Import Config */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Import Configuration</h3>
            
            {importError && (
              <div className="rounded-md bg-red-50 p-3 text-sm text-red-800">
                {importError}
              </div>
            )}
            
            {importSuccess && (
              <div className="rounded-md bg-green-50 p-3 text-sm text-green-800">
                {importSuccess}
              </div>
            )}
            
            <form onSubmit={importForm.handleSubmit(onImport)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  File Path
                </label>
                <Input
                  {...importForm.register('importPath')}
                  placeholder="/path/to/config.json"
                  error={importForm.formState.errors.importPath?.message}
                />
              </div>
              
              <Button
                type="submit"
                isLoading={isImporting}
              >
                <FiUpload className="mr-2" />
                Import
              </Button>
            </form>
          </div>
          
          {/* Export Config */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Export Configuration</h3>
            
            {exportError && (
              <div className="rounded-md bg-red-50 p-3 text-sm text-red-800">
                {exportError}
              </div>
            )}
            
            {exportSuccess && (
              <div className="rounded-md bg-green-50 p-3 text-sm text-green-800">
                {exportSuccess}
              </div>
            )}
            
            <form onSubmit={exportForm.handleSubmit(onExport)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  File Path
                </label>
                <Input
                  {...exportForm.register('exportPath')}
                  placeholder="/path/to/save/config.json"
                  error={exportForm.formState.errors.exportPath?.message}
                />
              </div>
              
              <Button
                type="submit"
                isLoading={isExporting}
              >
                <FiDownload className="mr-2" />
                Export
              </Button>
            </form>
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 