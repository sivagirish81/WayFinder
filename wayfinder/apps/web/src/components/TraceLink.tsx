export function TraceLink({ traceUrl }: { traceUrl?: string }) {
  return <a className="link-button" href={traceUrl ?? 'http://localhost:16686'}>Trace</a>;
}
