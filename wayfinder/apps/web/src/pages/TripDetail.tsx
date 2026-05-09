import { AuditTimeline } from '../components/AuditTimeline';
import { CandidatePlacesPanel } from '../components/CandidatePlacesPanel';
import { LangGraphNodeTimeline } from '../components/LangGraphNodeTimeline';
import { ParticipantsPanel } from '../components/ParticipantsPanel';
import { PreferenceSummaryPanel } from '../components/PreferenceSummaryPanel';
import { RankedPlacesPanel } from '../components/RankedPlacesPanel';
import { TemporalStatePanel } from '../components/TemporalStatePanel';
import { ToolCallTable } from '../components/ToolCallTable';
import { TripStatePanel } from '../components/TripStatePanel';

export function TripDetail() {
  return (
    <>
      <h1>Trip Detail</h1>
      <div className="panel-grid">
        <TripStatePanel />
        <ParticipantsPanel />
        <PreferenceSummaryPanel />
        <CandidatePlacesPanel />
        <RankedPlacesPanel />
        <TemporalStatePanel />
        <LangGraphNodeTimeline />
        <AuditTimeline />
      </div>
      <ToolCallTable />
    </>
  );
}
