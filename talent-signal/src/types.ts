export type NodeType = "dataSource" | "vectorSearch" | "filter" | "llmAgent" | "output";

export interface NodeConfig {
  collection?: string;
  index?: string;
  field?: string;
  path?: string;
  limit?: number;
  op?: string;
  value?: any;
  provider?: string;
  model?: string;
  promptTemplate?: string;
  outputField?: string;
  [key: string]: any;
}

export interface WorkflowNode {
  id: string;
  type: NodeType;
  position: { x: number; y: number };
  config: NodeConfig;
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
}

export interface WorkflowGraph {
  id: string;
  name: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
}

export interface CompiledStage {
  stageType: string;
  stageName: string;
  mongoStage?: Record<string, any>;
  llmConfig?: {
    provider: string;
    model: string;
    promptTemplate: string;
    outputField: string;
  };
  details: Record<string, any>;
}

export interface CompiledPlan {
  workflowId: string;
  workflowName: string;
  pipeline: Record<string, any>[];
  llmStages: CompiledStage[];
  executionOrder: string[];
}
