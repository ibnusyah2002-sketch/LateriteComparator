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

  status text not null default 'active'
    check (status in ('active', 'inactive', 'review')),

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists comparator_images (
  id uuid primary key default gen_random_uuid(),

  sample_id uuid not null references comparator_samples(id) on delete cascade,
  code text not null,

  image_type text not null default 'raw'
    check (image_type in ('raw', 'scale', 'other')),

  local_path text,
  storage_path text,
  public_url text,

  is_primary boolean not null default false,

  embedding vector(512),
  metadata jsonb not null default '{}'::jsonb,

  created_at timestamptz not null default now()
);

create table if not exists scan_sessions (
  id uuid primary key default gen_random_uuid(),

  input_image_path text,
  input_image_source text
    check (input_image_source in ('camera', 'upload', 'unknown')),

  best_match_sample_id uuid references comparator_samples(id),
  best_match_code text,
  similarity_score numeric,
  confidence_label text,

  result_payload jsonb not null default '{}'::jsonb,

  created_at timestamptz not null default now()
);

create index if not exists comparator_samples_code_idx
on comparator_samples (code);

create index if not exists comparator_samples_zone_idx
on comparator_samples (zone);

create index if not exists comparator_samples_color_idx
on comparator_samples (color);

create index if not exists comparator_samples_status_idx
on comparator_samples (status);

create index if not exists comparator_images_sample_id_idx
on comparator_images (sample_id);

create index if not exists comparator_images_code_idx
on comparator_images (code);

create index if not exists comparator_images_image_type_idx
on comparator_images (image_type);

create index if not exists comparator_images_is_primary_idx
on comparator_images (is_primary);

create index if not exists comparator_images_embedding_idx
on comparator_images
using ivfflat (embedding vector_cosine_ops)
with (lists = 100);

create index if not exists scan_sessions_created_at_idx
on scan_sessions (created_at desc);

create index if not exists scan_sessions_best_match_code_idx
on scan_sessions (best_match_code);

create unique index if not exists comparator_images_storage_path_unique_idx
on comparator_images (storage_path);

create or replace function set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists comparator_samples_set_updated_at on comparator_samples;

create trigger comparator_samples_set_updated_at
before update on comparator_samples
for each row
execute function set_updated_at();