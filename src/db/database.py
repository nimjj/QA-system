"""PostgreSQL database layer for Tenants, Categories, Line Items, and Tenant Lines.

Connects to existing connect_first.tenants and app.qa_* tables, with graceful fallback
to built-in criteria.json when database is unavailable.
"""

import os
import json
import uuid
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "ciap")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_CRITERIA_JSON_PATH = os.path.join(_ROOT, "src", "v3", "config", "criteria.json")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def _default_criteria_json(tenant_id: str = "S-NET") -> Dict[str, Any]:
    """Fail-safe default: load criteria from src/v3/config/criteria.json."""
    try:
        with open(_CRITERIA_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            data["tenant_id"] = tenant_id
            return data
    except Exception:
        return {
            "tenant_id": tenant_id,
            "category_weights": {"Soft Skills": 0.333, "Technical Knowledge": 0.667},
            "categories": []
        }


def init_db():
    """Initializes app.qa_* tables matching schema and seeds default criteria without touching existing PBX tables."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS app.qa_categories (
                    category_id VARCHAR(100) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    category_weight DOUBLE PRECISION NOT NULL DEFAULT 1.0
                );

                CREATE TABLE IF NOT EXISTS app.qa_line_items (
                    line_item_id VARCHAR(100) PRIMARY KEY,
                    category_id VARCHAR(100) NOT NULL REFERENCES app.qa_categories(category_id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    deduction_value INTEGER NOT NULL DEFAULT 10
                );

                CREATE TABLE IF NOT EXISTS app.qa_tenant_criteria (
                    tenant_id INTEGER NOT NULL REFERENCES connect_first.tenants(code) ON DELETE CASCADE,
                    line_item_id VARCHAR(100) NOT NULL REFERENCES app.qa_line_items(line_item_id) ON DELETE CASCADE,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    custom_deduction INTEGER,
                    PRIMARY KEY (tenant_id, line_item_id)
                );
            """)

            # Seed default categories
            cur.execute("""
                INSERT INTO app.qa_categories (category_id, name, category_weight)
                VALUES 
                    ('cat-soft-skills', 'Soft Skills', 0.333),
                    ('cat-tech-knowledge', 'Technical Knowledge', 0.667)
                ON CONFLICT (category_id) DO UPDATE SET 
                    name = EXCLUDED.name,
                    category_weight = EXCLUDED.category_weight;
            """)

            # Seed default 11 line items
            items = [
                ('item-branding', 'cat-soft-skills', 'Branding and Survey Check', 'Handled by Rule Engine.', 15),
                ('item-dead-air', 'cat-soft-skills', 'Hold time and Dead Air', 'Handled by Rule Engine.', 15),
                ('item-personalized', 'cat-soft-skills', 'Personalized the call/ticket appropriately', 'Handled by Rule Engine.', 15),
                ('item-empathy', 'cat-soft-skills', 'Empathy & Acknowledgment Statement', 'Handled by Rule Engine and Snippet LLM.', 35),
                ('item-rapport', 'cat-soft-skills', 'Build rapport and observed professionalism', 'VIOLATION-BASED: Default to PASS.', 20),
                ('item-paraphrasing', 'cat-tech-knowledge', 'Paraphrasing', 'Handled dynamically by Vector Engine.', 15),
                ('item-verified', 'cat-tech-knowledge', 'Verified customer', 'Handled deterministically by Rule Engine.', 25),
                ('item-probing', 'cat-tech-knowledge', 'Probing', 'Diagnostic probing questions check.', 25),
                ('item-ownership', 'cat-tech-knowledge', 'Took ownership of the problem', 'VIOLATION-BASED: Default to PASS.', 25),
                ('item-active-listening', 'cat-tech-knowledge', 'Active listening', 'Handled by Snippet LLM.', 10),
                ('item-resolved', 'cat-tech-knowledge', 'Confirmed the issue is resolved', 'Explicit confirmation of resolution.', 15)
            ]
            for lid, cid, name, desc, ded in items:
                cur.execute("""
                    INSERT INTO app.qa_line_items (line_item_id, category_id, name, description, deduction_value)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (line_item_id) DO UPDATE SET
                        category_id = EXCLUDED.category_id,
                        name = EXCLUDED.name,
                        description = EXCLUDED.description,
                        deduction_value = EXCLUDED.deduction_value;
                """, (lid, cid, name, desc, ded))

        conn.commit()


def _resolve_tenant_code(cur, tenant_id: Any) -> Optional[int]:
    """Resolve string or integer tenant identifier to connect_first.tenants integer code."""
    s = str(tenant_id).strip()
    if s.isdigit():
        val = int(s)
        cur.execute("SELECT code FROM connect_first.tenants WHERE code = %s;", (val,))
        row = cur.fetchone()
        if row:
            return row["code"]
        cur.execute("SELECT code FROM connect_first.tenants WHERE id = %s;", (val,))
        row = cur.fetchone()
        if row:
            return row["code"]
    cur.execute("SELECT code FROM connect_first.tenants WHERE LOWER(name) = LOWER(%s);", (s,))
    row = cur.fetchone()
    return row["code"] if row else None


def get_all_tenants() -> List[Dict[str, Any]]:
    """Lists all active tenants from connect_first.tenants using code as the unique tenant_id."""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT code, name, status FROM connect_first.tenants WHERE status = 'ACTIVE' ORDER BY code ASC;")
                rows = cur.fetchall()
                if rows:
                    return [{"tenant_id": str(r["code"]), "code": r["code"], "name": r["name"]} for r in rows]
    except Exception:
        pass
    return [{"tenant_id": "S-NET", "code": 0, "name": "S-Net Communications"}]


def create_tenant(tenant_id: str, name: str) -> Dict[str, Any]:
    """Compatibility endpoint for creating tenants."""
    return {"tenant_id": tenant_id, "name": name}


def create_category(category_id: Optional[str], tenant_id: str, name: str, category_weight: float = 1.0) -> Dict[str, Any]:
    cat_id = category_id or f"cat-{uuid.uuid4().hex[:8]}"
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO app.qa_categories (category_id, name, category_weight)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (category_id) DO UPDATE SET name = EXCLUDED.name, category_weight = EXCLUDED.category_weight
                    RETURNING category_id, name, category_weight;
                    """,
                    (cat_id, name, category_weight)
                )
                row = cur.fetchone()
            conn.commit()
        return dict(row)
    except Exception:
        return {"category_id": cat_id, "name": name, "category_weight": category_weight}


def get_categories(tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT category_id, name, category_weight FROM app.qa_categories ORDER BY name ASC;")
                return cur.fetchall()
    except Exception:
        return [
            {"category_id": "cat-soft-skills", "name": "Soft Skills", "category_weight": 0.333},
            {"category_id": "cat-tech-knowledge", "name": "Technical Knowledge", "category_weight": 0.667}
        ]


def get_tenant_criteria(tenant_id: str) -> Dict[str, Any]:
    """Retrieves all categories and line items with is_active toggle status for a tenant by code."""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                code = _resolve_tenant_code(cur, tenant_id)
                cur.execute("""
                    SELECT 
                        li.line_item_id, 
                        c.category_id,
                        c.name as category_name,
                        c.category_weight,
                        li.name, 
                        li.description, 
                        COALESCE(tc.custom_deduction, li.deduction_value) as deduction_value,
                        COALESCE(tc.is_active, TRUE) as is_active
                    FROM app.qa_line_items li
                    JOIN app.qa_categories c ON li.category_id = c.category_id
                    LEFT JOIN app.qa_tenant_criteria tc ON li.line_item_id = tc.line_item_id AND tc.tenant_id = %s
                    ORDER BY c.name, li.name;
                """, (code,))
                rows = cur.fetchall()

                if rows:
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
                        "tenant_id": str(code) if code is not None else str(tenant_id),
                        "category_weights": category_weights,
                        "categories": result_categories
                    }
    except Exception:
        pass
    return _default_criteria_json(tenant_id)


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

    if not active_categories:
        return _default_criteria_json(tenant_id)

    return {
        "tenant_id": tenant_id,
        "category_weights": active_weights,
        "categories": active_categories
    }


def toggle_tenant_criterion(tenant_id: str, line_item_id: str, is_active: bool) -> Dict[str, Any]:
    """Toggles a criterion ON or OFF for a specific tenant by code in app.qa_tenant_criteria."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            code = _resolve_tenant_code(cur, tenant_id)
            if code is None:
                code = int(tenant_id) if str(tenant_id).isdigit() else 208
            cur.execute(
                """
                INSERT INTO app.qa_tenant_criteria (tenant_id, line_item_id, is_active)
                VALUES (%s, %s, %s)
                ON CONFLICT (tenant_id, line_item_id)
                DO UPDATE SET is_active = EXCLUDED.is_active;
                """,
                (code, line_item_id, is_active)
            )
        conn.commit()
    return {"tenant_id": str(code), "line_item_id": line_item_id, "is_active": is_active}


def get_all_criteria() -> List[Dict[str, Any]]:
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT li.line_item_id, li.category_id, c.name as category_name, li.name, li.description, li.deduction_value
                    FROM app.qa_line_items li
                    JOIN app.qa_categories c ON li.category_id = c.category_id
                    ORDER BY c.name, li.name;
                """)
                return cur.fetchall()
    except Exception:
        raw = _default_criteria_json()
        out = []
        for cat in raw.get("categories", []):
            for i in cat.get("line_items", []):
                out.append({
                    "line_item_id": f"item-{i.get('name', '').lower()[:10]}",
                    "category_id": cat.get("name"),
                    "category_name": cat.get("name"),
                    "name": i.get("name"),
                    "description": i.get("description", ""),
                    "deduction_value": i.get("deduction_value", 10)
                })
        return out


def create_criterion(category_id: str, name: str, description: str, deduction_value: int, line_item_id: Optional[str] = None) -> Dict[str, Any]:
    item_id = line_item_id or f"item-{uuid.uuid4().hex[:8]}"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO app.qa_line_items (line_item_id, category_id, name, description, deduction_value)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING line_item_id, category_id, name, description, deduction_value;
                """,
                (item_id, category_id, name, description, deduction_value)
            )
            item = cur.fetchone()
        conn.commit()
    return item


def update_criterion(line_item_id: str, name: str, description: str, deduction_value: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE app.qa_line_items
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
            cur.execute("DELETE FROM app.qa_line_items WHERE line_item_id = %s;", (line_item_id,))
            deleted = cur.rowcount > 0
        conn.commit()
    return deleted
