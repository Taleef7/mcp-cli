import Layout from '@/components/Layout';
import ToolsViewer from '@/components/ToolsViewer';

export default function ToolsPage() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Server Tools</h1>
      <ToolsViewer />
    </Layout>
  );
} 