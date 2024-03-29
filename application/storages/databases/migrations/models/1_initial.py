from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "category" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "name" VARCHAR(1024) NOT NULL UNIQUE,
            "parent_category_id" INT  UNIQUE REFERENCES "category" ("id") ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS "idx_category_name_8b0cb9" ON "category" ("name");
        CREATE TABLE IF NOT EXISTS "product" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "goods_id" VARCHAR(128) NOT NULL UNIQUE,
            "name" VARCHAR(1024) NOT NULL,
            "price" DECIMAL(10,2) NOT NULL
        );
        CREATE INDEX IF NOT EXISTS "idx_product_goods_i_c9c212" ON "product" ("goods_id");
        CREATE TABLE IF NOT EXISTS "product_attribute" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "name" VARCHAR(256) NOT NULL,
            "value" VARCHAR(1024) NOT NULL,
            "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS "idx_product_att_name_53aec4" ON "product_attribute" ("name");
        CREATE INDEX IF NOT EXISTS "idx_product_att_product_d7f30a" ON "product_attribute" ("product_id");
        CREATE UNIQUE INDEX "uid_product_ima_product_841bff" ON "product_attribute" ("product_id", "name");
        CREATE TABLE IF NOT EXISTS "product_image" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "name" VARCHAR(256) NOT NULL,
            "url" VARCHAR(512) NOT NULL,
            "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS "idx_product_ima_name_92f7a8" ON "product_image" ("name");
        CREATE INDEX IF NOT EXISTS "idx_product_ima_product_39930c" ON "product_image" ("product_id");
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_product_ima_product_841bfe" ON "product_image" ("product_id", "name");
        CREATE TABLE IF NOT EXISTS "aerich" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "version" VARCHAR(255) NOT NULL,
            "app" VARCHAR(100) NOT NULL,
            "content" JSONB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS "product_category" (
            "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE SET NULL,
            "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE SET NULL
        );
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "product_category";
        DROP TABLE IF EXISTS "product_image";
        DROP TABLE IF EXISTS "product_attribute";
        DROP TABLE IF EXISTS "product";
        DROP TABLE IF EXISTS "category";
    """
