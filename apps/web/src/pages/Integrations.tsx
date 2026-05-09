import { IntegrationStatusCard } from '../components/IntegrationStatusCard';

const integrations = ['OpenAI', 'Slack', 'Notion', 'Temporal', 'PostgreSQL', 'Jaeger', 'OpenStreetMap'];

export function Integrations() {
  return <><h1>Integrations</h1><section className="card-grid">{integrations.map((name) => <IntegrationStatusCard key={name} name={name} status="configured" />)}</section></>;
}
