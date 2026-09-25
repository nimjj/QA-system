"""PostgreSQL database layer for Tenants, Categories, Line Items, and Tenant Lines."""

import os
import uuid
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "qa_database")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    """Initializes tables matching the ERD schema and seeds default data."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # 1. Tenants table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tenants (
                    tenant_id VARCHAR(100) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
            """)

            # 2. Categories table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    category_id VARCHAR(100) PRIMARY KEY,
                    tenant_id VARCHAR(100) NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    category_weight DOUBLE PRECISION NOT NULL DEFAULT 1.0
                );
            """)

            # 3. Line Items table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS line_items (
                    line_item_id VARCHAR(100) PRIMARY KEY,
                    category_id VARCHAR(100) NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    deduction_value INTEGER NOT NULL DEFAULT 10
                );
            """)

            # 4. Tenant Lines table (junction with toggle isActive)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tenant_lines (
                    tenant_id VARCHAR(100) NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
                    line_item_id VARCHAR(100) NOT NULL REFERENCES line_items(line_item_id) ON DELETE CASCADE,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    PRIMARY KEY (tenant_id, line_item_id)
                );
            """)
        conn.commit()

    seed_default_data()


def seed_default_data():
    """Seeds default tenant-abc with the 11 standard criteria if not present."""
    default_tenant_id = "tenant-abc"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT tenant_id FROM tenants WHERE tenant_id = %s;", (default_tenant_id,))
            if cur.fetchone():
                return  # already seeded

            # Insert default tenant
            cur.execute(
                "INSERT INTO tenants (tenant_id, name) VALUES (%s, %s);",
                (default_tenant_id, "Tenant ABC")
            )

            # Insert categories
            cat_soft_id = "cat-soft-skills"
            cat_tech_id = "cat-tech-knowledge"
            cur.execute(
                "INSERT INTO categories (category_id, tenant_id, name, category_weight) VALUES (%s, %s, %s, %s);",
                (cat_soft_id, default_tenant_id, "Soft Skills", 0.333)
            )
            cur.execute(
                "INSERT INTO categories (category_id, tenant_id, name, category_weight) VALUES (%s, %s, %s, %s);",
                (cat_tech_id, default_tenant_id, "Technical Knowledge", 0.667)
            )

            # The 11 standard criteria
            items = [
                # Soft Skills
                (
                    "item-branding", cat_soft_id, "Branding and Survey Check",
                    "Handled by Rule Engine.", 15
                ),
                (
                    "item-hold-dead-air", cat_soft_id, "Hold time and Dead Air",
                    "Handled by Rule Engine.", 15
                ),
                (
                    "item-personalized-call", cat_soft_id, "Personalized the call/ticket appropriately",
                    "Handled by Rule Engine.", 15
                ),
                (
                    "item-empathy", cat_soft_id, "Empathy & Acknowledgment Statement",
                    "Handled by Rule Engine and Snippet LLM.", 35
                ),
                (
                    "item-rapport", cat_soft_id, "Build rapport and observed professionalism",
                    "VIOLATION-BASED: Default to PASS. Rate FAIL only if you can quote a specific agent line that is rude, condescending, dismissive, sarcastic, or unprofessional.", 20
                ),
                # Technical Knowledge
                (
                    "item-paraphrasing", cat_tech_id, "Paraphrasing",
                    "Handled dynamically by Vector Engine.", 15
                ),
                (
                    "item-verified-customer", cat_tech_id, "Verified customer",
                    "Handled deterministically by Rule Engine.", 25
                ),
                (
                    "item-probing", cat_tech_id, "Probing",
                    "Based on the customer's problem provided in the context, did the agent ask diagnostic questions to probe this problem? Output YES or NO.", 25
                ),
                (
                    "item-ownership", cat_tech_id, "Took ownership of the problem",
                    "VIOLATION-BASED: Default to PASS. Rate FAIL only if you can quote a specific agent line that blames another department/team, deflects responsibility, tells the customer to call back elsewhere, or refuses to help.", 25
                ),
                (
                    "item-active-listening", cat_tech_id, "Active listening",
                    "Handled by Snippet LLM.", 10
                ),
                (
                    "item-confirmed-resolved", cat_tech_id, "Confirmed the issue is resolved",
                    "Did the agent explicitly confirm that the issue was resolved? Output YES or NO.", 15
                )
            ]

            for line_item_id, category_id, name, desc, ded_val in items:
                cur.execute(
                    """
                    INSERT INTO line_items (line_item_id, category_id, name, description, deduction_value)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (line_item_id) DO NOTHING;
                    """,
                    (line_item_id, category_id, name, desc, ded_val)
                )
                cur.execute(
                    """
                    INSERT INTO tenant_lines (tenant_id, line_item_id, is_active)
                    VALUES (%s, %s, TRUE)
                    ON CONFLICT (tenant_id, line_item_id) DO NOTHING;
                    """,
                    (default_tenant_id, line_item_id)
                )
        conn.commit()


def get_all_tenants() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT tenant_id, name FROM tenants ORDER BY name ASC;")
            return cur.fetchall()


def create_tenant(tenant_id: str, name: str) -> Dict[str, Any]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO tenants (tenant_id, name) VALUES (%s, %s) RETURNING tenant_id, name;",
                (tenant_id, name)
            )
            # Replicate standard categories for this tenant
            cat_soft_id = f"cat-soft-{tenant_id}"
            cat_tech_id = f"cat-tech-{tenant_id}"
            cur.execute(
                "INSERT INTO categories (category_id, tenant_id, name, category_weight) VALUES (%s, %s, %s, %s);",
                (cat_soft_id, tenant_id, "Soft Skills", 0.333)
            )
            cur.execute(
                "INSERT INTO categories (category_id, tenant_id, name, category_weight) VALUES (%s, %s, %s, %s);",
                (cat_tech_id, tenant_id, "Technical Knowledge", 0.667)
            )
            # Link existing standard line items to this tenant in tenant_lines
            cur.execute("SELECT line_item_id FROM line_items;")
            all_lines = cur.fetchall()
            for row in all_lines:
                cur.execute(
                    """
                    INSERT INTO tenant_lines (tenant_id, line_item_id, is_active)
                    VALUES (%s, %s, TRUE)
                    ON CONFLICT DO NOTHING;
                    """,
                    (tenant_id, row["line_item_id"])
                )
        conn.commit()
    return {"tenant_id": tenant_id, "name": name}


def get_tenant_criteria(tenant_id: str) -> Dict[str, Any]:
    """Retrieves all categories and line items with is_active status for a tenant."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check tenant exists
            cur.execute("SELECT tenant_id, name FROM tenants WHERE tenant_id = %s;", (tenant_id,))
            tenant = cur.fetchone()
            if not tenant:
                # If tenant doesn't exist, fallback to tenant-abc
                tenant_id = "tenant-abc"

            # Fetch categories for this tenant (or default)
            cur.execute(
                "SELECT category_id, name, category_weight FROM categories WHERE tenant_id = %s ORDER BY name ASC;",
                (tenant_id,)
            )
            categories = cur.fetchall()
            if not categories:
                # Fallback to default categories
                cur.execute(
                    "SELECT category_id, name, category_weight FROM categories WHERE tenant_id = 'tenant-abc' ORDER BY name ASC;"
                )
                categories = cur.fetchall()

            category_weights = {c["name"]: float(c["category_weight"]) for c in categories}

            result_categories = []
            for cat in categories:
                cur.execute(
                    """
                    SELECT 
                        li.line_item_id, 
                        li.name, 
                        li.description, 
                        li.deduction_value,
                        COALESCE(tl.is_active, TRUE) as is_active
                    FROM line_items li
                    LEFT JOIN tenant_lines tl ON li.line_item_id = tl.line_item_id AND tl.tenant_id = %s
                    WHERE li.category_id = %s
                    ORDER BY li.name ASC;
                    """,
                    (tenant_id, cat["category_id"])
                )
                items = cur.fetchall()
                result_categories.append({
                    "category_id": cat["category_id"],
                    "name": cat["name"],
                    "category_weight": float(cat["category_weight"]),
                    "line_items": items
                })

            return {
                "tenant_id": tenant_id,
                "category_weights": category_weights,
                "categories": result_categories
            }


def get_active_criteria_for_evaluation(tenant_id: str) -> Dict[str, Any]:
    """Returns criteria JSON for evaluate_interaction containing ONLY active line items."""
    raw = get_tenant_criteria(tenant_id)
    active_categories = []
    active_weights = {}

    for cat in raw.get("categories", []):
        # Filter line items that are active
        active_items = [
            {
                "name": item["name"],
                "description": item.get("description", ""),
                "deduction_value": item.get("deduction_value", 10)
            }
            for item in cat.get("line_items", [])
            if item.get("is_active", True)
        ]
        if active_items:
            active_categories.append({
                "name": cat["name"],
                "line_items": active_items
            })
            active_weights[cat["name"]] = raw.get("category_weights", {}).get(cat["name"], 1.0)

    return {
        "tenant_id": tenant_id,
        "category_weights": active_weights,
        "categories": active_categories
    }


def toggle_tenant_criterion(tenant_id: str, line_item_id: str, is_active: bool) -> Dict[str, Any]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tenant_lines (tenant_id, line_item_id, is_active)
                VALUES (%s, %s, %s)
                ON CONFLICT (tenant_id, line_item_id)
                DO UPDATE SET is_active = EXCLUDED.is_active;
                """,
                (tenant_id, line_item_id, is_active)
            )
        conn.commit()
    return {"tenant_id": tenant_id, "line_item_id": line_item_id, "is_active": is_active}


def get_all_criteria() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT li.line_item_id, li.category_id, c.name as category_name, li.name, li.description, li.deduction_value
                FROM line_items li
                JOIN categories c ON li.category_id = c.category_id
                ORDER BY c.name, li.name;
            """)
            return cur.fetchall()


def create_criterion(category_id: str, name: str, description: str, deduction_value: int) -> Dict[str, Any]:
    line_item_id = f"item-{uuid.uuid4().hex[:8]}"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO line_items (line_item_id, category_id, name, description, deduction_value)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING line_item_id, category_id, name, description, deduction_value;
                """,
                (line_item_id, category_id, name, description, deduction_value)
            )
            item = cur.fetchone()

            # Link to all existing tenants as active
            cur.execute("SELECT tenant_id FROM tenants;")
            tenants = cur.fetchall()
            for t in tenants:
                cur.execute(
                    "INSERT INTO tenant_lines (tenant_id, line_item_id, is_active) VALUES (%s, %s, TRUE) ON CONFLICT DO NOTHING;",
                    (t["tenant_id"], line_item_id)
                )
        conn.commit()
    return item


def update_criterion(line_item_id: str, name: str, description: str, deduction_value: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE line_items
                SET name = %s, description = %s, deduction_value = %s
                WHERE line_item_id = %s
                RETURNING line_item_id, category_id, name, description, deduction_value;
                """,
                (name, description, deduction_value, line_item_id)
            )
            item = cur.fetchone()
        conn.commit()
    return item


def delete_criterion(line_item_id: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM line_items WHERE line_item_id = %s;", (line_item_id,))
            deleted = cur.rowcount > 0
        conn.commit()
    return deleted
