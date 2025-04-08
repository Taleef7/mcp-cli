import Layout from '@/components/Layout';
import QueryRunner from '@/components/QueryRunner';

export default function QueryPage() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Run Query</h1>
      <QueryRunner />
    </Layout>
  );
} 