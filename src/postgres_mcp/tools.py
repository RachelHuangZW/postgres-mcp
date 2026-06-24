import json

import psycopg2.extras

from .db import get_connection


def execute_query(sql: str) -> str:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql)
            if cur.description:
                rows = [dict(r) for r in cur.fetchall()]
                return json.dumps(rows, default=str, indent=2)
            conn.commit()
            return f"{cur.rowcount} rows affected"
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def explain_query(sql: str, analyze: bool = False) -> str:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            prefix = (
                "EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)"
                if analyze
                else "EXPLAIN (FORMAT TEXT)"
            )
            cur.execute(f"{prefix} {sql}")
            return "\n".join(row[0] for row in cur.fetchall())
    finally:
        conn.close()


def get_table_schema(table_name: str, schema: str = "public") -> str:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT column_name, data_type, character_maximum_length,
                       is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
                """,
                (schema, table_name),
            )
            columns = cur.fetchall()
            if not columns:
                return f"Table '{schema}.{table_name}' not found"

            cur.execute(
                "SELECT indexname, indexdef FROM pg_indexes WHERE schemaname = %s AND tablename = %s",
                (schema, table_name),
            )
            indexes = cur.fetchall()

        lines = [f"Table: {schema}.{table_name}\n", "Columns:"]
        for col in columns:
            dtype = col["data_type"]
            if col["character_maximum_length"]:
                dtype += f"({col['character_maximum_length']})"
            nullable = "NULL" if col["is_nullable"] == "YES" else "NOT NULL"
            default = f" DEFAULT {col['column_default']}" if col["column_default"] else ""
            lines.append(f"  {col['column_name']}: {dtype} {nullable}{default}")

        if indexes:
            lines.append("\nIndexes:")
            for idx in indexes:
                lines.append(f"  {idx['indexname']}: {idx['indexdef']}")

        return "\n".join(lines)
    finally:
        conn.close()
