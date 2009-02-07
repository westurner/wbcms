BEGIN;
CREATE TABLE "tiger_company" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(128) NOT NULL
)
;
CREATE TABLE "tiger_contact" (
    "id" integer NOT NULL PRIMARY KEY,
    "first_name" varchar(42) NOT NULL,
    "middle_name" varchar(42) NOT NULL,
    "last_name" varchar(42) NOT NULL,
    "company_id" integer NOT NULL REFERENCES "tiger_company" ("id"),
    "addr_1" varchar(42) NOT NULL,
    "addr_2" varchar(42) NOT NULL,
    "city" varchar(42) NOT NULL,
    "state" varchar(2) NOT NULL,
    "zip_code" varchar(10) NOT NULL,
    "phone_number" varchar(20) NOT NULL,
    "email" varchar(75) NOT NULL
)
;
CREATE TABLE "tiger_instructor" (
    "contact_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "tiger_contact" ("id")
)
;
CREATE TABLE "tiger_instructoravailability" (
    "id" integer NOT NULL PRIMARY KEY,
    "starting" datetime NOT NULL,
    "ending" datetime NOT NULL,
    "open" bool NOT NULL,
    "instructor_id" integer NOT NULL REFERENCES "tiger_instructor" ("contact_ptr_id")
)
;
CREATE TABLE "tiger_clientavailability" (
    "id" integer NOT NULL PRIMARY KEY,
    "starting" datetime NOT NULL,
    "ending" datetime NOT NULL,
    "open" bool NOT NULL,
    "client_id" integer NOT NULL REFERENCES "tiger_contact" ("id"),
    "course_request_id" integer NOT NULL
)
;
CREATE TABLE "tiger_course" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(256) NOT NULL,
    "subject" varchar(128) NOT NULL,
    "description" text NOT NULL,
    "cost" decimal NULL
)
;
CREATE TABLE "tiger_courserequest" (
    "id" integer NOT NULL PRIMARY KEY,
    "client_id" integer NOT NULL REFERENCES "tiger_contact" ("id"),
    "course_id" integer NOT NULL REFERENCES "tiger_course" ("id"),
    "number_of_students" integer NOT NULL,
    "status" integer NOT NULL,
    "schedule_id" integer NULL
)
;
CREATE TABLE "tiger_coursesession" (
    "id" integer NOT NULL PRIMARY KEY,
    "starting" datetime NOT NULL,
    "ending" datetime NOT NULL,
    "open" bool NOT NULL,
    "location" text NOT NULL,
    "description" text NOT NULL,
    "notes" text NOT NULL,
    "schedule_id" integer NOT NULL
)
;
CREATE TABLE "tiger_courseschedule" (
    "id" integer NOT NULL PRIMARY KEY,
    "course_id" integer NOT NULL REFERENCES "tiger_course" ("id"),
    "instructor_id" integer NOT NULL REFERENCES "tiger_instructor" ("contact_ptr_id")
)
;
CREATE TABLE "tiger_instructor_courses" (
    "id" integer NOT NULL PRIMARY KEY,
    "instructor_id" integer NOT NULL REFERENCES "tiger_instructor" ("contact_ptr_id"),
    "course_id" integer NOT NULL REFERENCES "tiger_course" ("id"),
    UNIQUE ("instructor_id", "course_id")
)
;
CREATE TABLE "tiger_courseschedule_students" (
    "id" integer NOT NULL PRIMARY KEY,
    "courseschedule_id" integer NOT NULL REFERENCES "tiger_courseschedule" ("id"),
    "contact_id" integer NOT NULL REFERENCES "tiger_contact" ("id"),
    UNIQUE ("courseschedule_id", "contact_id")
)
;
CREATE INDEX "tiger_contact_company_id" ON "tiger_contact" ("company_id");
CREATE INDEX "tiger_instructoravailability_instructor_id" ON "tiger_instructoravailability" ("instructor_id");
CREATE INDEX "tiger_clientavailability_client_id" ON "tiger_clientavailability" ("client_id");
CREATE INDEX "tiger_clientavailability_course_request_id" ON "tiger_clientavailability" ("course_request_id");
CREATE INDEX "tiger_courserequest_client_id" ON "tiger_courserequest" ("client_id");
CREATE INDEX "tiger_courserequest_course_id" ON "tiger_courserequest" ("course_id");
CREATE INDEX "tiger_courserequest_schedule_id" ON "tiger_courserequest" ("schedule_id");
CREATE INDEX "tiger_coursesession_schedule_id" ON "tiger_coursesession" ("schedule_id");
CREATE INDEX "tiger_courseschedule_course_id" ON "tiger_courseschedule" ("course_id");
CREATE INDEX "tiger_courseschedule_instructor_id" ON "tiger_courseschedule" ("instructor_id");
COMMIT;
