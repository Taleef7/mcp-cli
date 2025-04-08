import Layout from '@/components/Layout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { FiServer, FiSend, FiTool, FiSettings } from 'react-icons/fi';
import Link from 'next/link';

export default function Home() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Servers Card */}
        <Link href="/servers" className="block">
          <Card className="h-full transition-transform hover:scale-[1.02] hover:shadow-md">
            <CardContent className="p-6 flex items-center space-x-4">
              <div className="bg-blue-100 p-3 rounded-full">
                <FiServer className="h-6 w-6 text-blue-700" />
              </div>
              <div>
                <h2 className="text-xl font-semibold">Server Management</h2>
                <p className="text-gray-600 mt-1">Add, edit, and remove MCP servers</p>
              </div>
            </CardContent>
          </Card>
        </Link>

        {/* Query Card */}
        <Link href="/query" className="block">
          <Card className="h-full transition-transform hover:scale-[1.02] hover:shadow-md">
            <CardContent className="p-6 flex items-center space-x-4">
              <div className="bg-green-100 p-3 rounded-full">
                <FiSend className="h-6 w-6 text-green-700" />
              </div>
              <div>
                <h2 className="text-xl font-semibold">Run Query</h2>
                <p className="text-gray-600 mt-1">Execute queries on MCP servers</p>
              </div>
            </CardContent>
          </Card>
        </Link>

        {/* Tools Card */}
        <Link href="/tools" className="block">
          <Card className="h-full transition-transform hover:scale-[1.02] hover:shadow-md">
            <CardContent className="p-6 flex items-center space-x-4">
              <div className="bg-purple-100 p-3 rounded-full">
                <FiTool className="h-6 w-6 text-purple-700" />
              </div>
              <div>
                <h2 className="text-xl font-semibold">Tools</h2>
                <p className="text-gray-600 mt-1">Explore available tools on each server</p>
              </div>
            </CardContent>
          </Card>
        </Link>

        {/* Config Card */}
        <Link href="/config" className="block">
          <Card className="h-full transition-transform hover:scale-[1.02] hover:shadow-md">
            <CardContent className="p-6 flex items-center space-x-4">
              <div className="bg-amber-100 p-3 rounded-full">
                <FiSettings className="h-6 w-6 text-amber-700" />
              </div>
              <div>
                <h2 className="text-xl font-semibold">Configuration</h2>
                <p className="text-gray-600 mt-1">Import and export MCP configuration</p>
              </div>
            </CardContent>
          </Card>
        </Link>
      </div>

      <div className="mt-6">
        <Card>
          <CardHeader>
            <CardTitle>About MCP CLI</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">
              MCP CLI (Model Context Protocol Command Line Interface) is a tool for interacting with various context providers 
              through a unified interface. This web UI provides a simple way to manage MCP servers, execute queries, and 
              explore available tools.
            </p>
            <div className="mt-4">
              <h3 className="font-medium mb-2">Quick Start:</h3>
              <ol className="list-decimal pl-6 space-y-2 text-gray-600">
                <li>Add a new MCP server in the <Link href="/servers" className="text-blue-600 hover:underline">Servers</Link> section</li>
                <li>Run a query on the server from the <Link href="/query" className="text-blue-600 hover:underline">Query</Link> page</li>
                <li>Explore available tools on the <Link href="/tools" className="text-blue-600 hover:underline">Tools</Link> page</li>
                <li>Backup your configuration on the <Link href="/config" className="text-blue-600 hover:underline">Configuration</Link> page</li>
              </ol>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
