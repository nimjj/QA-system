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
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tenants (
                    tenant_id VARCHAR(100) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    category_id VARCHAR(100) PRIMARY KEY,
                    tenant_id VARCHAR(100) NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    category_weight DOUBLE PRECISION NOT NULL DEFAULT 1.0
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS line_items (
                    line_item_id VARCHAR(100) PRIMARY KEY,
                    category_id VARCHAR(100) NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    deduction_value INTEGER NOT NULL DEFAULT 10
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS tenant_lines (
                    tenant_id VARCHAR(100) NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
                    line_item_id VARCHAR(100) NOT NULL REFERENCES line_items(line_item_id) ON DELETE CASCADE,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    PRIMARY KEY (tenant_id, line_item_id)
                );
            """)
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


def create_category(category_id: Optional[str], tenant_id: str, name: str, category_weight: float = 1.0) -> Dict[str, Any]:
    cat_id = category_id or f"cat-{uuid.uuid4().hex[:8]}"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO categories (category_id, tenant_id, name, category_weight)
                VALUES (%s, %s, %s, %s)
                RETURNING category_id, tenant_id, name, category_weight;
                """,
                (cat_id, tenant_id, name, category_weight)
            )
            row = cur.fetchone()
        conn.commit()
    return row


def get_categories(tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if tenant_id:
                cur.execute(
                    "SELECT category_id, tenant_id, name, category_weight FROM categories WHERE tenant_id = %s ORDER BY name ASC;",
                    (tenant_id,)
                )
            else:
                cur.execute(
                    "SELECT category_id, tenant_id, name, category_weight FROM categories ORDER BY tenant_id, name ASC;"
                )
            return cur.fetchall()


def get_tenant_criteria(tenant_id: str) -> Dict[str, Any]:
    """Retrieves all categories and line items with is_active toggle status for a tenant."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    li.line_item_id, 
                    c.category_id,
                    c.name as category_name,
                    c.category_weight,
                    li.name, 
                    li.description, 
                    li.deduction_value,
                    COALESCE(tl.is_active, TRUE) as is_active
                FROM line_items li
                JOIN categories c ON li.category_id = c.category_id
                LEFT JOIN tenant_lines tl ON li.line_item_id = tl.line_item_id AND tl.tenant_id = %s
                ORDER BY c.name, li.name;
            """, (tenant_id,))
            rows = cur.fetchall()

            category_map = {}
            for r in rows:
                cname = r["category_name"]
                if cname not in category_map:
                    category_map[cname] = {
                        "category_id": r["category_id"],
                        "name": cname,
                        "category_weight": float(r["category_weight"]),
                        "line_items": []
                    }
                category_map[cname]["line_items"].append({
                    "line_item_id": r["line_item_id"],
                    "name": r["name"],
                    "description": r["description"],
                    "deduction_value": r["deduction_value"],
                    "is_active": r["is_active"]
                })

            result_categories = list(category_map.values())
            category_weights = {c["name"]: c["category_weight"] for c in result_categories}

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


def create_criterion(category_id: str, name: str, description: str, deduction_value: int, line_item_id: Optional[str] = None) -> Dict[str, Any]:
    item_id = line_item_id or f"item-{uuid.uuid4().hex[:8]}"
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
