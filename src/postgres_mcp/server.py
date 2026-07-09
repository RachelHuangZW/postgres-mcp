from mcp.server.fastmcp import FastMCP

from . import tools

mcp = FastMCP("postgres-mcp")


@mcp.tool()
def execute_query(sql: str) -> str:
    """Execute a SQL query against the connected PostgreSQL database and return results as JSON."""
    return tools.execute_query(sql)


@mcp.tool()
def explain_query(sql: str, analyze: bool = False) -> str:
    """
    Return the EXPLAIN execution plan for a SQL query.
    Set analyze=True to run EXPLAIN ANALYZE (this actually executes the query).
    """
    return tools.explain_query(sql, analyze)


@mcp.tool()
def list_tables(schema: str = "public") -> str:
    """List all tables in a PostgreSQL schema."""
    return tools.list_tables(schema)


@mcp.tool()
def get_table_schema(table_name: str, schema: str = "public") -> str:
    """Get columns and indexes for a PostgreSQL table."""
    return tools.get_table_schema(table_name, schema)


@mcp.tool()
def analyze_query(sql: str, ddl: str = "", table_name: str = "") -> str:
    """Analyzes a slow SQL query and returns optimization advice. DDL is optional — the tool automatically fetches the schema for tables referenced in the query if not provided. Use this whenever the user asks for query optimization, regardless of whether they have the DDL handy."""
    return tools.analyze_query(sql, ddl, table_name)


@mcp.tool()
def get_slow_queries(limit: int = 5, include_system_queries: bool = False) -> str:
    """Return the slowest SQL queries by mean execution time from pg_stat_statements. System and diagnostic queries are excluded by default; set include_system_queries=true to include them."""
    return tools.get_slow_queries(limit, include_system_queries)

def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
