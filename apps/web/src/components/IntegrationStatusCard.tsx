export function IntegrationStatusCard({ name, status }: { name: string; status: string }) {
  return (
    <article className="info-card compact">
      <h2>{name}</h2>
      <span className="badge">{status}</span>
    </article>
  );
}
