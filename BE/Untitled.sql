CREATE TYPE "status" AS ENUM (
  'active',
  'disabled',
  'in_progress',
  'arrived',
  'under_maintenance',
  'delayed'
);

CREATE TABLE "students" (
  "id" UUID PRIMARY KEY,
  "student_id" text UNIQUE,
  "name" text,
  "email" text UNIQUE,
  "password" text,
  "major" text,
  "is_deleted" bool,
  "is_active" bool,
  "created_at" timestamp,
  "updated_at" timestamp,
  "deleted_at" timestamp
);

CREATE TABLE "admin" (
  "id" UUID PRIMARY KEY,
  "name" text,
  "email" text UNIQUE,
  "password" text,
  "is_deleted" bool,
  "is_active" bool,
  "created_at" timestamp,
  "updated_at" timestamp,
  "deleted_at" timestamp
);

CREATE TABLE "driver" (
  "id" UUID PRIMARY KEY,
  "admin_id" text,
  "name" text,
  "email" text UNIQUE,
  "password" text,
  "bus_number" int,
  "phone" int,
  "is_deleted" bool,
  "is_active" bool,
  "created_at" timestamp,
  "updated_at" timestamp,
  "deleted_at" timestamp
);

CREATE TABLE "routes" (
  "id" uuid PRIMARY KEY,
  "name" text,
  "description" text,
  "status" status,
  "created_at" timestamp,
  "updated_at" timestamp,
  "deleted_at" timestamp
);

CREATE TABLE "stops" (
  "id" uuid PRIMARY KEY,
  "route_id" text,
  "name" text,
  "latitude" double,
  "longitude" double,
  "status" status,
  "created_at" timestamp,
  "updated_at" timestamp,
  "deleted_at" timestamp
);

CREATE TABLE "trips" (
  "id" uuid PRIMARY KEY,
  "route_id" text,
  "driver_id" text,
  "bus_id" text,
  "latitude" double,
  "longitude" double,
  "status" status,
  "current_time" timestamp,
  "created_at" timestamp,
  "updated_at" timestamp,
  "deleted_at" timestamp
);

CREATE TABLE "buses" (
  "id" uuid PRIMARY KEY,
  "bus_number" int,
  "start_time" timestamp,
  "end_time" timestamp,
  "status" status,
  "created_at" timestamp,
  "updated_at" timestamp,
  "deleted_at" timestamp
);

CREATE TABLE "bus_location" (
  "id" uuid PRIMARY KEY,
  "bus_id" text,
  "trip_id" text,
  "capacity" text,
  "status" status,
  "created_at" timestamp,
  "updated_at" timestamp,
  "deleted_at" timestamp
);

ALTER TABLE "driver" ADD FOREIGN KEY ("admin_id") REFERENCES "admin" ("id");

ALTER TABLE "driver" ADD FOREIGN KEY ("bus_number") REFERENCES "buses" ("bus_number");

ALTER TABLE "stops" ADD FOREIGN KEY ("route_id") REFERENCES "routes" ("id");

ALTER TABLE "trips" ADD FOREIGN KEY ("route_id") REFERENCES "routes" ("id");

ALTER TABLE "trips" ADD FOREIGN KEY ("driver_id") REFERENCES "driver" ("id");

ALTER TABLE "trips" ADD FOREIGN KEY ("bus_id") REFERENCES "buses" ("id");

ALTER TABLE "bus_location" ADD FOREIGN KEY ("bus_id") REFERENCES "buses" ("id");

ALTER TABLE "bus_location" ADD FOREIGN KEY ("trip_id") REFERENCES "trips" ("id");