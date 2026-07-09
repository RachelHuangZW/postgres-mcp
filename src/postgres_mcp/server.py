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
    """Analyze a slow SQL query using SQL-Surgeon and return optimization advice."""
    return tools.analyze_query(sql, ddl, table_name)


@mcp.tool()
def get_slow_queries(limit: int = 5) -> str:
    """Return the slowest SQL queries by mean execution time from pg_stat_statements."""
    return tools.get_slow_queries(limit)

def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
