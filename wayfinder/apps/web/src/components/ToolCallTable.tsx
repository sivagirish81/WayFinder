import { RiskBadge } from './RiskBadge';

const calls = ['parse_trip_request', 'normalize_group_preferences', 'discover_destination_pois', 'generate_itinerary'];

export function ToolCallTable() {
  return (
    <table className="table">
      <thead><tr><th>Tool</th><th>Integration</th><th>Risk</th><th>Status</th></tr></thead>
      <tbody>
        {calls.map((call) => (
          <tr key={call}><td>{call}</td><td>Wayfinder</td><td><RiskBadge risk="low" /></td><td>completed</td></tr>
        ))}
      </tbody>
    </table>
  );
}
