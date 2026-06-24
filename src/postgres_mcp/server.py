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
def get_table_schema(table_name: str, schema: str = "public") -> str:
    """Get columns and indexes for a PostgreSQL table."""
    return tools.get_table_schema(table_name, schema)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
