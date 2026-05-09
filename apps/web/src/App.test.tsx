import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { App } from './App';

describe('App', () => {
  it('renders the Wayfinder dashboard shell', () => {
    render(<App />);
    expect(screen.getAllByText('Wayfinder').length).toBeGreaterThan(0);
    expect(screen.getByText('Temporal workflows')).toBeInTheDocument();
    expect(screen.getByText('LangGraph planner')).toBeInTheDocument();
    expect(screen.getByText('LangChain tools')).toBeInTheDocument();
  });
});
