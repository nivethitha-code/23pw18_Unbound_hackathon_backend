-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Workflows Table
create table workflows (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  definition jsonb not null -- Stores the full steps definition
);

-- Workflow Runs Table (for storing execution state)
create table workflow_runs (
  id uuid default uuid_generate_v4() primary key,
  workflow_id uuid references workflows(id) on delete cascade,
  status text not null default 'pending', -- pending, running, completed, failed
  current_step_index integer default 0,
  steps_results jsonb default '[]'::jsonb, -- Array of results for each step
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Enable Realtime for workflow_runs
alter publication supabase_realtime add table workflow_runs;
