
export interface User {
  id: string;
  email: string;
  fullName: string;
  companyName?: string;
  jobTitle?: string;
  role: string;
}

export interface Agent {
  id: string;
  name: string;
  type: string;
  description: string;
  status: 'idle' | 'running' | 'completed' | 'failed';
  capabilities: string[];
}

export interface WorkflowStatus {
  workflowId: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  currentStep?: string;
  progress?: number;
  agentStatuses?: {
    agentId: string;
    agentName: string;
    status: string;
    progress: number;
  }[];
}

export interface ComplianceResult {
  workflowId: string;
  timestamp: string;
  overallRisk: 'low' | 'medium' | 'high' | 'critical';
  riskScore: number;
  summary: string;
  agentAnalyses: {
    agentId: string;
    agentName: string;
    analysis: string;
    findings: string[];
    recommendations: string[];
  }[];
  recommendations: string[];
}

export interface Workflow {
  id: string;
  workflowId: string;
  status: string;
  query?: string;
  documentPath?: string;
  createdAt: string;
  updatedAt: string;
}
