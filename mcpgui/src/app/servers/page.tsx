import Layout from '@/components/Layout';
import ServerList from '@/components/ServerList';

export default function ServersPage() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Server Management</h1>
      <ServerList />
    </Layout>
  );
} 