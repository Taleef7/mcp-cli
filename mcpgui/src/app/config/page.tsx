import Layout from '@/components/Layout';
import ConfigManager from '@/components/ConfigManager';

export default function ConfigPage() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Configuration</h1>
      <ConfigManager />
    </Layout>
  );
} 