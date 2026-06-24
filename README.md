# postgres-mcp

An [MCP](https://modelcontextprotocol.io) server that exposes PostgreSQL query, EXPLAIN, and schema inspection tools to Claude Desktop (or any MCP-compatible client).

## Tools

| Tool | Parameters | Description |
|---|---|---|
| `execute_query` | `sql` | Run any SQL statement; SELECT returns rows as JSON, DML returns affected row count |
| `explain_query` | `sql`, `analyze` (bool, default `false`) | Get the query execution plan. When `analyze=true` runs `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` |
| `get_table_schema` | `table_name`, `schema` (default `"public"`) | List columns (type, nullability, default) and indexes for a table |

## Project layout

```
src/postgres_mcp/
  server.py   # FastMCP entry point, tool registrations
  tools.py    # SQL execution logic
  db.py       # Connection helper (reads DATABASE_URL)
tests/
  test_tools.py
examples/
  claude_desktop_config.json
```

## Setup

### 1. Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) — `brew install uv`
- A running PostgreSQL instance
- [Claude Desktop](https://claude.ai/download) (or another MCP client)

### 2. Clone and install

```bash
git clone https://github.com/RachelHuangZW/postgres-mcp
cd postgres-mcp
uv sync
```

### 3. Configure your database

Copy `.env.example` to `.env` and fill in your connection string:

```bash
cp .env.example .env
# edit .env: DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### 4. Register with Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` and merge in the `mcpServers` block (see `examples/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "postgres-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/postgres-mcp", "python", "-m", "postgres_mcp.server"],
      "env": {
        "DATABASE_URL": "postgresql://user:password@localhost:5432/dbname"
      }
    }
  }
}
```

Replace `/path/to/postgres-mcp` with the absolute path to this repo and fill in your `DATABASE_URL`. Then **fully quit and reopen Claude Desktop**.

> **Tip:** You can also run the server directly with `uv run postgres-mcp` after `uv sync`.

### 5. Verify

Open a new Claude Desktop conversation and ask:

> "Use get_table_schema to show me the schema for the users table."

Claude should call the tool and return the column list.

## Development

```bash
uv sync --group dev
uv run pytest
```

## Security note

`execute_query` runs whatever SQL you pass — use a **read-only database role** in production, or restrict access to trusted users only.
