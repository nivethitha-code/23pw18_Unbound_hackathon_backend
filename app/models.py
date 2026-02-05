from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime
from enum import Enum

class ModelType(str, Enum):
    KIMI_K2P5 = "kimi-k2p5"
    KIMI_K2_INSTRUCT = "kimi-k2-instruct-0905"

class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class CompletionCriteria(BaseModel):
    type: str  # "contains", "regex", "llm_judge", "json_valid"
    value: Optional[str] = None
    instruction: Optional[str] = None # For LLM judge

class StepCreate(BaseModel):
    order: int
    prompt_template: str
    model: ModelType
    completion_criteria: CompletionCriteria
    retry_limit: int = 3

class WorkflowCreate(BaseModel):
    name: str
    steps: List[StepCreate]

class Step(StepCreate):
    id: str
    workflow_id: str

class Workflow(WorkflowCreate):
    id: str
    created_at: datetime
    steps: List[Step]

class RunStepResult(BaseModel):
    step_id: str
    status: StepStatus
    input_context: Optional[str]
    output: Optional[str]
    error: Optional[str]
    retries_used: int = 0
    cost: float = 0.0

class WorkflowRun(BaseModel):
    id: str
    workflow_id: str
    status: str # "running", "completed", "failed"
    current_step_index: int
    steps_results: List[RunStepResult]
    created_at: datetime
    updated_at: datetime
