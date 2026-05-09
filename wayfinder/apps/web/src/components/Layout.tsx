import type { PropsWithChildren } from 'react';

export function Layout({ children }: PropsWithChildren) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Wayfinder</div>
        <nav>
          <a href="#">Dashboard</a>
          <a href="#">Demo Launcher</a>
          <a href="#">Temporal</a>
          <a href="#">LangGraph</a>
          <a href="#">Tool Calls</a>
          <a href="#">Audit</a>
        </nav>
      </aside>
      <main>{children}</main>
    </div>
  );
}
