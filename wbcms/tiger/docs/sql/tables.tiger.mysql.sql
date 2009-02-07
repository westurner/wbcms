BEGIN;
CREATE TABLE `tiger_company` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(128) NOT NULL
)
;
CREATE TABLE `tiger_contact` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `first_name` varchar(42) NOT NULL,
    `middle_name` varchar(42) NOT NULL,
    `last_name` varchar(42) NOT NULL,
    `company_id` integer NOT NULL,
    `addr_1` varchar(42) NOT NULL,
    `addr_2` varchar(42) NOT NULL,
    `city` varchar(42) NOT NULL,
    `state` varchar(2) NOT NULL,
    `zip_code` varchar(10) NOT NULL,
    `phone_number` varchar(20) NOT NULL,
    `email` varchar(75) NOT NULL
)
;
ALTER TABLE `tiger_contact` ADD CONSTRAINT company_id_refs_id_1d21cfd2 FOREIGN KEY (`company_id`) REFERENCES `tiger_company` (`id`);
CREATE TABLE `tiger_instructor` (
    `contact_ptr_id` integer NOT NULL PRIMARY KEY
)
;
ALTER TABLE `tiger_instructor` ADD CONSTRAINT contact_ptr_id_refs_id_1ec33305 FOREIGN KEY (`contact_ptr_id`) REFERENCES `tiger_contact` (`id`);
CREATE TABLE `tiger_instructoravailability` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `starting` datetime NOT NULL,
    `ending` datetime NOT NULL,
    `open` bool NOT NULL,
    `instructor_id` integer NOT NULL
)
;
ALTER TABLE `tiger_instructoravailability` ADD CONSTRAINT instructor_id_refs_contact_ptr_id_54865900 FOREIGN KEY (`instructor_id`) REFERENCES `tiger_instructor` (`contact_ptr_id`);
CREATE TABLE `tiger_clientavailability` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `starting` datetime NOT NULL,
    `ending` datetime NOT NULL,
    `open` bool NOT NULL,
    `client_id` integer NOT NULL,
    `course_request_id` integer NOT NULL
)
;
ALTER TABLE `tiger_clientavailability` ADD CONSTRAINT client_id_refs_id_22f51500 FOREIGN KEY (`client_id`) REFERENCES `tiger_contact` (`id`);
CREATE TABLE `tiger_course` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(256) NOT NULL,
    `subject` varchar(128) NOT NULL,
    `description` longtext NOT NULL,
    `cost` numeric(8, 2) NULL
)
;
CREATE TABLE `tiger_courserequest` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `client_id` integer NOT NULL,
    `course_id` integer NOT NULL,
    `number_of_students` integer NOT NULL,
    `status` integer NOT NULL,
    `schedule_id` integer NULL
)
;
ALTER TABLE `tiger_courserequest` ADD CONSTRAINT course_id_refs_id_79bc137 FOREIGN KEY (`course_id`) REFERENCES `tiger_course` (`id`);
ALTER TABLE `tiger_courserequest` ADD CONSTRAINT client_id_refs_id_1062bcaf FOREIGN KEY (`client_id`) REFERENCES `tiger_contact` (`id`);
ALTER TABLE `tiger_clientavailability` ADD CONSTRAINT course_request_id_refs_id_4986cafc FOREIGN KEY (`course_request_id`) REFERENCES `tiger_courserequest` (`id`);
CREATE TABLE `tiger_coursesession` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `starting` datetime NOT NULL,
    `ending` datetime NOT NULL,
    `open` bool NOT NULL,
    `location` longtext NOT NULL,
    `description` longtext NOT NULL,
    `notes` longtext NOT NULL,
    `schedule_id` integer NOT NULL
)
;
CREATE TABLE `tiger_courseschedule` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `course_id` integer NOT NULL,
    `instructor_id` integer NOT NULL
)
;
ALTER TABLE `tiger_courseschedule` ADD CONSTRAINT instructor_id_refs_contact_ptr_id_56031770 FOREIGN KEY (`instructor_id`) REFERENCES `tiger_instructor` (`contact_ptr_id`);
ALTER TABLE `tiger_courseschedule` ADD CONSTRAINT course_id_refs_id_78ea13ae FOREIGN KEY (`course_id`) REFERENCES `tiger_course` (`id`);
ALTER TABLE `tiger_courserequest` ADD CONSTRAINT schedule_id_refs_id_4ff4e5fa FOREIGN KEY (`schedule_id`) REFERENCES `tiger_courseschedule` (`id`);
ALTER TABLE `tiger_coursesession` ADD CONSTRAINT schedule_id_refs_id_4d79d585 FOREIGN KEY (`schedule_id`) REFERENCES `tiger_courseschedule` (`id`);
CREATE TABLE `tiger_instructor_courses` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `instructor_id` integer NOT NULL,
    `course_id` integer NOT NULL,
    UNIQUE (`instructor_id`, `course_id`)
)
;
ALTER TABLE `tiger_instructor_courses` ADD CONSTRAINT instructor_id_refs_contact_ptr_id_5b2a16d6 FOREIGN KEY (`instructor_id`) REFERENCES `tiger_instructor` (`contact_ptr_id`);
ALTER TABLE `tiger_instructor_courses` ADD CONSTRAINT course_id_refs_id_7353bf0c FOREIGN KEY (`course_id`) REFERENCES `tiger_course` (`id`);
CREATE TABLE `tiger_courseschedule_students` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `courseschedule_id` integer NOT NULL,
    `contact_id` integer NOT NULL,
    UNIQUE (`courseschedule_id`, `contact_id`)
)
;
ALTER TABLE `tiger_courseschedule_students` ADD CONSTRAINT courseschedule_id_refs_id_fbc3a61 FOREIGN KEY (`courseschedule_id`) REFERENCES `tiger_courseschedule` (`id`);
ALTER TABLE `tiger_courseschedule_students` ADD CONSTRAINT contact_id_refs_id_50719cea FOREIGN KEY (`contact_id`) REFERENCES `tiger_contact` (`id`);
CREATE INDEX `tiger_contact_company_id` ON `tiger_contact` (`company_id`);
CREATE INDEX `tiger_instructoravailability_instructor_id` ON `tiger_instructoravailability` (`instructor_id`);
CREATE INDEX `tiger_clientavailability_client_id` ON `tiger_clientavailability` (`client_id`);
CREATE INDEX `tiger_clientavailability_course_request_id` ON `tiger_clientavailability` (`course_request_id`);
CREATE INDEX `tiger_courserequest_client_id` ON `tiger_courserequest` (`client_id`);
CREATE INDEX `tiger_courserequest_course_id` ON `tiger_courserequest` (`course_id`);
CREATE INDEX `tiger_courserequest_schedule_id` ON `tiger_courserequest` (`schedule_id`);
CREATE INDEX `tiger_coursesession_schedule_id` ON `tiger_coursesession` (`schedule_id`);
CREATE INDEX `tiger_courseschedule_course_id` ON `tiger_courseschedule` (`course_id`);
CREATE INDEX `tiger_courseschedule_instructor_id` ON `tiger_courseschedule` (`instructor_id`);
COMMIT;
