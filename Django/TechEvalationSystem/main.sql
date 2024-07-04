/*
 Navicat Premium Data Transfer

 Source Server         : db
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 17/04/2023 12:22:08
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for GuanLiYuan
-- ----------------------------
DROP TABLE IF EXISTS "GuanLiYuan";
CREATE TABLE "GuanLiYuan" ("name" varchar(32) NOT NULL PRIMARY KEY, "password" varchar(32) NOT NULL, "email" varchar(254) NOT NULL, "phone" varchar(11) NOT NULL, "zhiwu" varchar(28) NOT NULL, "photo" varchar(100) NOT NULL, "is_active" bool NOT NULL);

-- ----------------------------
-- Records of GuanLiYuan
-- ----------------------------
BEGIN;
INSERT INTO "GuanLiYuan" ("name", "password", "email", "phone", "zhiwu", "photo", "is_active") VALUES ('zhangsan', '202cb962ac59075b964b07152d234b70', '169330@qq.com', '1991', '管理员', ' ', 1);
COMMIT;

-- ----------------------------
-- Table structure for Kecheng
-- ----------------------------
DROP TABLE IF EXISTS "Kecheng";
CREATE TABLE "Kecheng" ("id" varchar(11) NOT NULL PRIMARY KEY, "kecheng" varchar(128) NOT NULL, "ok" varchar(6) NOT NULL, "is_active" bool NOT NULL, "teacher_id_id" varchar(12) NOT NULL REFERENCES "Teachers" ("teacher_id") DEFERRABLE INITIALLY DEFERRED, "xuehao_id" varchar(12) NOT NULL REFERENCES "Students" ("xuehao") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of Kecheng
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for PingJia
-- ----------------------------
DROP TABLE IF EXISTS "PingJia";
CREATE TABLE "PingJia" ("id" varchar(11) NOT NULL PRIMARY KEY, "s_daan1" decimal NOT NULL, "s_daan2" decimal NOT NULL, "s_daan3" decimal NOT NULL, "s_daan4" decimal NOT NULL, "s_daan5" decimal NOT NULL, "s_daan6" decimal NOT NULL, "s_daan7" decimal NOT NULL, "s_daan8" decimal NOT NULL, "s_daan9" decimal NOT NULL, "s_daan10" decimal NOT NULL, "s_avg" decimal NOT NULL, "s_liuyan" text NULL, "is_active" bool NOT NULL, "kecheng_id" varchar(11) NOT NULL UNIQUE REFERENCES "Kecheng" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of PingJia
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for Students
-- ----------------------------
DROP TABLE IF EXISTS "Students";
CREATE TABLE "Students" ("name" varchar(28) NOT NULL, "xueyuan" varchar(28) NOT NULL, "banji" varchar(28) NOT NULL, "xuehao" varchar(12) NOT NULL PRIMARY KEY, "sex" varchar(6) NOT NULL, "email" varchar(254) NOT NULL, "phone" varchar(11) NOT NULL, "photo" varchar(100) NOT NULL, "is_active" bool NOT NULL, "password" varchar(60) NOT NULL);

-- ----------------------------
-- Records of Students
-- ----------------------------
BEGIN;
INSERT INTO "Students" ("name", "xueyuan", "banji", "xuehao", "sex", "email", "phone", "photo", "is_active", "password") VALUES ('20180001', '计科学院', '计科1801', '20180001', '18', '169330@qq.com', '1991', '11', 1, '202cb962ac59075b964b07152d234b70');
COMMIT;

-- ----------------------------
-- Table structure for Teachers
-- ----------------------------
DROP TABLE IF EXISTS "Teachers";
CREATE TABLE "Teachers" ("name" varchar(28) NOT NULL, "teacher_id" varchar(12) NOT NULL PRIMARY KEY, "sex" varchar(6) NOT NULL, "email" varchar(254) NOT NULL, "phone" varchar(11) NOT NULL, "photo" varchar(100) NOT NULL, "is_active" bool NOT NULL, "password" varchar(60) NOT NULL);

-- ----------------------------
-- Records of Teachers
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for TiKu_1
-- ----------------------------
DROP TABLE IF EXISTS "TiKu_1";
CREATE TABLE "TiKu_1" ("id" integer NOT NULL PRIMARY KEY, "timu" text NOT NULL, "is_active" bool NOT NULL);

-- ----------------------------
-- Records of TiKu_1
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS "auth_group";
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS "auth_group_permissions";
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS "auth_permission";
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (1, 1, 'add_logentry', 'Can add log entry');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (2, 1, 'change_logentry', 'Can change log entry');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (3, 1, 'delete_logentry', 'Can delete log entry');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (4, 1, 'view_logentry', 'Can view log entry');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (5, 2, 'add_permission', 'Can add permission');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (6, 2, 'change_permission', 'Can change permission');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (7, 2, 'delete_permission', 'Can delete permission');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (8, 2, 'view_permission', 'Can view permission');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (9, 3, 'add_group', 'Can add group');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (10, 3, 'change_group', 'Can change group');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (11, 3, 'delete_group', 'Can delete group');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (12, 3, 'view_group', 'Can view group');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (13, 4, 'add_user', 'Can add user');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (14, 4, 'change_user', 'Can change user');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (15, 4, 'delete_user', 'Can delete user');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (16, 4, 'view_user', 'Can view user');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (17, 5, 'add_contenttype', 'Can add content type');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (18, 5, 'change_contenttype', 'Can change content type');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (19, 5, 'delete_contenttype', 'Can delete content type');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (20, 5, 'view_contenttype', 'Can view content type');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (21, 6, 'add_session', 'Can add session');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (22, 6, 'change_session', 'Can change session');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (23, 6, 'delete_session', 'Can delete session');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (24, 6, 'view_session', 'Can view session');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (25, 7, 'add_guanliyuan', 'Can add guan li yuan');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (26, 7, 'change_guanliyuan', 'Can change guan li yuan');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (27, 7, 'delete_guanliyuan', 'Can delete guan li yuan');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (28, 7, 'view_guanliyuan', 'Can view guan li yuan');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (29, 8, 'add_kecheng', 'Can add ke cheng');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (30, 8, 'change_kecheng', 'Can change ke cheng');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (31, 8, 'delete_kecheng', 'Can delete ke cheng');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (32, 8, 'view_kecheng', 'Can view ke cheng');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (33, 9, 'add_students', 'Can add students');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (34, 9, 'change_students', 'Can change students');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (35, 9, 'delete_students', 'Can delete students');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (36, 9, 'view_students', 'Can view students');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (37, 10, 'add_teachers', 'Can add teachers');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (38, 10, 'change_teachers', 'Can change teachers');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (39, 10, 'delete_teachers', 'Can delete teachers');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (40, 10, 'view_teachers', 'Can view teachers');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (41, 11, 'add_tiku_1', 'Can add ti ku_1');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (42, 11, 'change_tiku_1', 'Can change ti ku_1');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (43, 11, 'delete_tiku_1', 'Can delete ti ku_1');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (44, 11, 'view_tiku_1', 'Can view ti ku_1');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (45, 12, 'add_pingjia', 'Can add ping jia');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (46, 12, 'change_pingjia', 'Can change ping jia');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (47, 12, 'delete_pingjia', 'Can delete ping jia');
INSERT INTO "auth_permission" ("id", "content_type_id", "codename", "name") VALUES (48, 12, 'view_pingjia', 'Can view ping jia');
COMMIT;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS "auth_user";
CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);

-- ----------------------------
-- Records of auth_user
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS "auth_user_groups";
CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS "auth_user_user_permissions";
CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS "django_admin_log";
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action_time" datetime NOT NULL, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0));

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS "django_content_type";
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (1, 'admin', 'logentry');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (2, 'auth', 'permission');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (3, 'auth', 'group');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (4, 'auth', 'user');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (6, 'sessions', 'session');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (7, 'login', 'guanliyuan');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (8, 'login', 'kecheng');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (9, 'login', 'students');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (10, 'login', 'teachers');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (11, 'login', 'tiku_1');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (12, 'login', 'pingjia');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS "django_migrations";
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (1, 'contenttypes', '0001_initial', '2022-01-12 14:16:35.951898');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (2, 'auth', '0001_initial', '2022-01-12 14:16:35.991790');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (3, 'admin', '0001_initial', '2022-01-12 14:16:36.021715');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2022-01-12 14:16:36.058783');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2022-01-12 14:16:36.088739');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2022-01-12 14:16:36.138637');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2022-01-12 14:16:36.161586');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (8, 'auth', '0003_alter_user_email_max_length', '2022-01-12 14:16:36.193501');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (9, 'auth', '0004_alter_user_username_opts', '2022-01-12 14:16:36.223420');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (10, 'auth', '0005_alter_user_last_login_null', '2022-01-12 14:16:36.257284');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (11, 'auth', '0006_require_contenttypes_0002', '2022-01-12 14:16:36.267258');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2022-01-12 14:16:36.301172');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (13, 'auth', '0008_alter_user_username_max_length', '2022-01-12 14:16:36.332084');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2022-01-12 14:16:36.363008');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (15, 'auth', '0010_alter_group_name_max_length', '2022-01-12 14:16:36.392926');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (16, 'auth', '0011_update_proxy_permissions', '2022-01-12 14:16:36.419850');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (17, 'login', '0001_initial', '2022-01-12 14:16:36.496645');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (18, 'sessions', '0001_initial', '2022-01-12 14:16:36.511607');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (19, 'auth', '0012_alter_user_first_name_max_length', '2023-04-17 12:08:39.120574');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (20, 'login', '0002_auto_20220112_1438', '2023-04-17 12:08:39.126082');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS "django_session";
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
INSERT INTO "django_session" ("session_key", "session_data", "expire_date") VALUES ('i38w9dxezf2q46ycdt0l2vdygywpd291', 'e30:1poGG2:LTlzYXQ8N7juZCVh6TuHWW11S_t-KZOvc4fGYOpxjqI', '2023-05-01 12:14:26.931316');
INSERT INTO "django_session" ("session_key", "session_data", "expire_date") VALUES ('sz4hib6u6c2y7nlnm0c5cteu1m4w2389', 'eyJuYW1lIjoiemhhbmdzYW4ifQ:1poGEe:EMFISOGin9xlBBoGO8fjcPE40N1NlWD18LA9l4xCUq8', '2023-05-01 12:13:00.953417');
COMMIT;

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE sqlite_sequence(name,seq);

-- ----------------------------
-- Records of sqlite_sequence
-- ----------------------------
BEGIN;
INSERT INTO "sqlite_sequence" ("name", "seq") VALUES ('django_migrations', 20);
INSERT INTO "sqlite_sequence" ("name", "seq") VALUES ('django_admin_log', 0);
INSERT INTO "sqlite_sequence" ("name", "seq") VALUES ('django_content_type', 12);
INSERT INTO "sqlite_sequence" ("name", "seq") VALUES ('auth_permission', 48);
INSERT INTO "sqlite_sequence" ("name", "seq") VALUES ('auth_group', 0);
INSERT INTO "sqlite_sequence" ("name", "seq") VALUES ('auth_user', 0);
COMMIT;

-- ----------------------------
-- Indexes structure for table Kecheng
-- ----------------------------
CREATE INDEX "main"."Kecheng_teacher_id_id_66df79ab"
ON "Kecheng" (
  "teacher_id_id" ASC
);
CREATE INDEX "main"."Kecheng_xuehao_id_30ea35a5"
ON "Kecheng" (
  "xuehao_id" ASC
);

-- ----------------------------
-- Auto increment value for auth_group
-- ----------------------------

-- ----------------------------
-- Indexes structure for table auth_group_permissions
-- ----------------------------
CREATE INDEX "main"."auth_group_permissions_group_id_b120cbf9"
ON "auth_group_permissions" (
  "group_id" ASC
);
CREATE UNIQUE INDEX "main"."auth_group_permissions_group_id_permission_id_0cd325b0_uniq"
ON "auth_group_permissions" (
  "group_id" ASC,
  "permission_id" ASC
);
CREATE INDEX "main"."auth_group_permissions_permission_id_84c5c92e"
ON "auth_group_permissions" (
  "permission_id" ASC
);

-- ----------------------------
-- Auto increment value for auth_permission
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 48 WHERE name = 'auth_permission';

-- ----------------------------
-- Indexes structure for table auth_permission
-- ----------------------------
CREATE INDEX "main"."auth_permission_content_type_id_2f476e4b"
ON "auth_permission" (
  "content_type_id" ASC
);
CREATE UNIQUE INDEX "main"."auth_permission_content_type_id_codename_01ab375a_uniq"
ON "auth_permission" (
  "content_type_id" ASC,
  "codename" ASC
);

-- ----------------------------
-- Auto increment value for auth_user
-- ----------------------------

-- ----------------------------
-- Indexes structure for table auth_user_groups
-- ----------------------------
CREATE INDEX "main"."auth_user_groups_group_id_97559544"
ON "auth_user_groups" (
  "group_id" ASC
);
CREATE INDEX "main"."auth_user_groups_user_id_6a12ed8b"
ON "auth_user_groups" (
  "user_id" ASC
);
CREATE UNIQUE INDEX "main"."auth_user_groups_user_id_group_id_94350c0c_uniq"
ON "auth_user_groups" (
  "user_id" ASC,
  "group_id" ASC
);

-- ----------------------------
-- Indexes structure for table auth_user_user_permissions
-- ----------------------------
CREATE INDEX "main"."auth_user_user_permissions_permission_id_1fbb5f2c"
ON "auth_user_user_permissions" (
  "permission_id" ASC
);
CREATE INDEX "main"."auth_user_user_permissions_user_id_a95ead1b"
ON "auth_user_user_permissions" (
  "user_id" ASC
);
CREATE UNIQUE INDEX "main"."auth_user_user_permissions_user_id_permission_id_14a6b632_uniq"
ON "auth_user_user_permissions" (
  "user_id" ASC,
  "permission_id" ASC
);

-- ----------------------------
-- Auto increment value for django_admin_log
-- ----------------------------

-- ----------------------------
-- Indexes structure for table django_admin_log
-- ----------------------------
CREATE INDEX "main"."django_admin_log_content_type_id_c4bce8eb"
ON "django_admin_log" (
  "content_type_id" ASC
);
CREATE INDEX "main"."django_admin_log_user_id_c564eba6"
ON "django_admin_log" (
  "user_id" ASC
);

-- ----------------------------
-- Auto increment value for django_content_type
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 12 WHERE name = 'django_content_type';

-- ----------------------------
-- Indexes structure for table django_content_type
-- ----------------------------
CREATE UNIQUE INDEX "main"."django_content_type_app_label_model_76bd3d3b_uniq"
ON "django_content_type" (
  "app_label" ASC,
  "model" ASC
);

-- ----------------------------
-- Auto increment value for django_migrations
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 20 WHERE name = 'django_migrations';

-- ----------------------------
-- Indexes structure for table django_session
-- ----------------------------
CREATE INDEX "main"."django_session_expire_date_a5c62663"
ON "django_session" (
  "expire_date" ASC
);

PRAGMA foreign_keys = true;
