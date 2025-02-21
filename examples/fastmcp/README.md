# FastMCP server for Sherlock Domains

## Usage

Copy `.env.example` to `.env` and set the `SHERLOCK_API_KEY` environment variable. You can get an API key by:
- Signing up at sherlockdomains.com
- Creating your own key (e.g. https://pk-generator.replit.app/)
- Leaving it blank (one will be auto-generated, but note that MCP does not save it. If you lose this key, you will lose access to any purchases made with it)

### Claude desktop app

```
fastmcp install main.py -f .env
```

This will add the server to `$HOME/Library/Application Support/Claude/claude_desktop_config.json` so it can be used in Claude desktop app directly.

You can ask Claude "what tools are available?" and it will list the tools.

### Cursor

1. Add a new command as explained in [here](https://docs.cursor.com/context/model-context-protocol)
2. Select `type: command`
3. Add the following command:
   `env SHERLOCK_API_KEY=YOUR_API_KEY uv run --with fastmcp fastmcp run path/to/sherlock/examples/fastmcp/main.py`
   - Make sure to replace `YOUR_API_KEY` with your actual API key
   - Make sure to replace `path/to/sherlock/examples/fastmcp/main.py` with the correct path

## Debug

To try out the tools:

```
pip install -r requirements.txt
fastmcp dev main.py
```

Open the inspector and use the tools.

