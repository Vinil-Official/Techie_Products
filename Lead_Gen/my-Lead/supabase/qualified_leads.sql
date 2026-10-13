create extension if not exists pgcrypto;

create table if not exists public.qualified_leads (
  id uuid primary key default gen_random_uuid(),
  source_lead_id text,
  owner_id uuid references auth.users(id) on delete cascade,
  name text not null check (length(trim(name)) > 0),
  phone text,
  location text,
  website text,
  qualification_status text not null,
  lead_score integer not null default 0 check (lead_score between 0 and 100),
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.qualified_leads
  drop constraint if exists qualified_leads_qualification_status_check;

alter table public.qualified_leads
  add constraint qualified_leads_qualification_status_check check (
    qualification_status in (
      'Qualified Lead',
      'Partially Qualified Lead',
      'Not Qualified Lead',
      'Meetings',
      'Contacted',
      'Proposals',
      'Deals'
    )
  );

create unique index if not exists qualified_leads_owner_source_unique
  on public.qualified_leads (owner_id, source_lead_id)
  where source_lead_id is not null;

create index if not exists qualified_leads_owner_created_at_idx
  on public.qualified_leads (owner_id, created_at desc);

alter table public.qualified_leads enable row level security;

drop policy if exists "Anyone can read qualified leads" on public.qualified_leads;
create policy "Anyone can read qualified leads"
  on public.qualified_leads for select to public
  using (true);

drop policy if exists "Anyone can insert qualified leads" on public.qualified_leads;
create policy "Anyone can insert qualified leads"
  on public.qualified_leads for insert to public
  with check (true);

drop policy if exists "Anyone can update qualified leads" on public.qualified_leads;
create policy "Anyone can update qualified leads"
  on public.qualified_leads for update to public
  using (true)
  with check (true);

drop policy if exists "Anyone can delete qualified leads" on public.qualified_leads;
create policy "Anyone can delete qualified leads"
  on public.qualified_leads for delete to public
  using (true);

grant select, insert, update, delete on public.qualified_leads to public;