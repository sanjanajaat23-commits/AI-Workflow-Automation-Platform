import { useEffect, useState } from "react";
import { getWorkflows } from "../services/workflowService";

type Workflow = {
  id: number;
  name: string;
  description?: string | null;
  is_active?: boolean;
};

export default function WorkflowList() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    async function loadWorkflows() {
      try {
        const data = await getWorkflows();
        if (mounted) {
          setWorkflows(Array.isArray(data) ? data : []);
        }
      } catch (err) {
        console.error(err);
        if (mounted) {
          setError("Failed to load workflows.");
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    loadWorkflows();

    return () => {
      mounted = false;
    };
  }, []);

  if (loading) {
    return <div>Loading workflows...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (workflows.length === 0) {
    return <div>No workflows found.</div>;
  }

  return (
    <div>
      {workflows.map((workflow) => (
        <div key={workflow.id}>
          <strong>{workflow.name}</strong>
          {workflow.description && <p>{workflow.description}</p>}
        </div>
      ))}
    </div>
  );
}
