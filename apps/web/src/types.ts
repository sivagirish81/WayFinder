export type TripStatus =
  | 'received'
  | 'planning'
  | 'collecting_preferences'
  | 'awaiting_approval'
  | 'completed'
  | 'failed';

export interface TripSummary {
  id: string;
  destination?: string;
  status: TripStatus;
  temporalWorkflowId?: string;
}
