import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';
import { Approvals } from './Approvals';
import { DemoLauncher } from './DemoLauncher';
import { Integrations } from './Integrations';
import { TemporalExplorer } from './TemporalExplorer';
import { ToolCalls } from './ToolCalls';
import { TripDetail } from './TripDetail';

describe('dashboard pages', () => {
  afterEach(() => cleanup());

  it('renders demo launcher participants copy', () => {
    render(<DemoLauncher />);
    expect(screen.getByText(/Alex, Priya, Jordan, and Sam/)).toBeInTheDocument();
  });

  it('renders trip detail panels', () => {
    render(<TripDetail />);
    expect(screen.getByText('Participants')).toBeInTheDocument();
    expect(screen.getByText('Candidate Places')).toBeInTheDocument();
    expect(screen.getByText('LangGraph Nodes')).toBeInTheDocument();
  });

  it('renders approval and integration surfaces', () => {
    render(<Approvals />);
    expect(screen.getByText('Approve')).toBeInTheDocument();
    render(<Integrations />);
    expect(screen.getByText('OpenStreetMap')).toBeInTheDocument();
  });

  it('renders Temporal explorer and tool calls', () => {
    render(<TemporalExplorer />);
    expect(screen.getByText('Temporal State')).toBeInTheDocument();
    render(<ToolCalls />);
    expect(screen.getByText('parse_trip_request')).toBeInTheDocument();
  });
});
