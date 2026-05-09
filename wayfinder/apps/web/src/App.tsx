import { Activity, GitBranch, Route, ShieldCheck, Workflow } from 'lucide-react';
import { Layout } from './components/Layout';

const cards = [
  {
    title: 'Temporal workflows',
    body: 'Durable trip coordination with timers, signals, queries, retries, and worker restart recovery.',
    icon: Workflow,
  },
  {
    title: 'LangGraph planner',
    body: 'Inspectable agent state machine for parsing, preferences, conflicts, places, itinerary, and revisions.',
    icon: GitBranch,
  },
  {
    title: 'LangChain tools',
    body: 'Typed integration layer for Slack, Notion, OpenAI, Overpass, budgeting, export, and audit.',
    icon: Route,
  },
  {
    title: 'Audit and traces',
    body: 'Every meaningful workflow, node, and tool event is designed to land in PostgreSQL and Jaeger.',
    icon: Activity,
  },
];

export function App() {
  return (
    <Layout>
      <section className="hero">
        <div>
          <p className="eyebrow">Wayfinder</p>
          <h1>AI group trip coordination that behaves like a durable platform.</h1>
          <p className="lede">
            Slack starts the conversation, Temporal keeps it alive, LangGraph plans with structured
            state, LangChain tools execute integrations, and Notion becomes the living trip document.
          </p>
        </div>
        <div className="status-panel" aria-label="Phase status">
          <ShieldCheck size={20} />
          <div>
            <strong>Phase 1 scaffold</strong>
            <span>API, worker, web shell, compose, CI, and environment hygiene.</span>
          </div>
        </div>
      </section>
      <section className="card-grid">
        {cards.map((card) => (
          <article className="info-card" key={card.title}>
            <card.icon size={22} />
            <h2>{card.title}</h2>
            <p>{card.body}</p>
          </article>
        ))}
      </section>
    </Layout>
  );
}
