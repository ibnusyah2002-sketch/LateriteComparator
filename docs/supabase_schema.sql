-- LCGC Supabase Schema
-- Laterite Comparator for Grade Control

create extension if not exists "pgcrypto";
create extension if not exists "vector";

create table if not exists comparator_samples (
  id uuid primary key default gen_random_uuid(),

  source_no integer,
  code text not null unique,
  sample_date date,
  sample_code text,
  incr text,

  ni numeric,
  co numeric,
  fe numeric,
  sio2 numeric,
  cao numeric,
  mgo numeric,
  cr2o3 numeric,
  al2o3 numeric,
  cr numeric,
  fe_ni numeric,
  s_m numeric,

  bc text,
  color text,
  zone text,
  size_text text,
  composition text,
  description text,

  documentation_raw text,
  documentation_si_gc text,
  ppt_reference text,
  front_reference text,

  status text not null default 'active',

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists comparator_images (
  id uuid primary key default gen_random_uuid(),

  sample_id uuid not null references comparator_samples(id) on delete cascade,
  code text not null,

  image_type text not null default 'raw',
  storage_path text,
  public_url text,

  embedding vector(512),
  metadata jsonb not null default '{}'::jsonb,

  created_at timestamptz not null default now()
);

create index if not exists comparator_samples_code_idx
on comparator_samples (code);

create index if not exists comparator_samples_zone_idx
on comparator_samples (zone);

create index if not exists comparator_samples_color_idx
on comparator_samples (color);

create index if not exists comparator_images_sample_id_idx
on comparator_images (sample_id);

create index if not exists comparator_images_code_idx
on comparator_images (code);

create index if not exists comparator_images_embedding_idx
on comparator_images
using ivfflat (embedding vector_cosine_ops)
with (lists = 100);

create table if not exists scan_sessions (
  id uuid primary key default gen_random_uuid(),

  input_image_path text,
  input_image_source text,

  best_match_sample_id uuid references comparator_samples(id),
  best_match_code text,
  similarity_score numeric,
  confidence_label text,

  result_payload jsonb not null default '{}'::jsonb,

  created_at timestamptz not null default now()
);

create index if not exists scan_sessions_created_at_idx
on scan_sessions (created_at desc);

create index if not exists scan_sessions_best_match_code_idx
on scan_sessions (best_match_code);