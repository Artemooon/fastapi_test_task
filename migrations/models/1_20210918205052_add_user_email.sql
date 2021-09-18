-- upgrade --
ALTER TABLE "user" ADD "email" VARCHAR(255) NOT NULL UNIQUE;
-- downgrade --
ALTER TABLE "user" DROP COLUMN "email";
