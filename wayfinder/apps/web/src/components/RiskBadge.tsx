export function RiskBadge({ risk }: { risk: 'low' | 'medium' | 'high' }) {
  return <span className={`badge badge-${risk}`}>{risk}</span>;
}
