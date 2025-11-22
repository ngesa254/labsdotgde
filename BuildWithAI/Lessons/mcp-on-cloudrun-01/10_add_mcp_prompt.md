# (Optional) Add MCP Prompt to Server

An MCP prompt can speed up your workflow for prompts you run often by creating a shorthand for a longer prompt.

Gemini CLI automatically converts MCP prompts into custom slash commands so that you can invoke an MCP prompt by typing `/prompt_name` where `prompt_name` is the name of your MCP prompt.

Create an MCP prompt so you can quickly find an animal in the zoo by typing `/find animal` into Gemini CLI.

## Add the Prompt to Your Server

Add this code to your `server.py` file above the main guard (`if __name__ == "__main__":`):

```python
@mcp.prompt()
def find(animal: str) -> str:
    """
    Find which exhibit and trail a specific animal might be located.
    """

    return (
        f"Please find the exhibit and trail information for {animal} in the zoo. "
        f"Respond with '[animal] can be found in the [exhibit] on the [trail].'"
        f"Example: Penguins can be found in The Arctic Exhibit on the Polar Path."
    )
```

## Re-deploy to Cloud Run

Deploy the updated application:

```bash
gcloud run deploy zoo-mcp-server \
    --region=europe-west1 \
    --source=. \
    --labels=dev-tutorial=codelab-mcp
```

You should see output similar to:

```
Building using Dockerfile and deploying container to Cloud Run service [zoo-mcp-server] in project [unstacked-labs-477314] region [europe-west1]
OK Building and deploying... Done.
  OK Uploading sources...
  OK Building Container...
  OK Creating Revision...
  OK Routing traffic...
Done.
Service [zoo-mcp-server] revision [zoo-mcp-server-00002-hgh] has been deployed and is serving 100 percent of traffic.
Service URL: https://zoo-mcp-server-683099143523.europe-west1.run.app
```

## Refresh Your ID Token

Refresh your ID_TOKEN for your remote MCP server:

```bash
export ID_TOKEN=$(gcloud auth print-identity-token)
```

Regenerate the settings file with the new token:

```bash
cat > ~/.gemini/settings.json << EOF
{
  "ide": {
    "hasSeenNudge": true
  },
  "mcpServers": {
    "zoo-remote": {
      "httpUrl": "https://zoo-mcp-server-${PROJECT_NUMBER}.europe-west1.run.app/mcp",
      "headers": {
        "Authorization": "Bearer ${ID_TOKEN}"
      }
    }
  },
  "security": {
    "auth": {
      "selectedType": "cloud-shell"
    }
  }
}
EOF
```

## Test the Custom Command

Start Gemini CLI:

```bash
gemini
```

Use the new custom command that you created:

```
/find --animal="lions"
```

Or simply:

```
/find lions
```

You should see that Gemini CLI calls the `get_animals_by_species` tool and formats the response as instructed by the MCP prompt!

```
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✔  get_animals_by_species (zoo-remote MCP Server) {"species":"lion"}                              │
│                                                                                                   │
│    [{"species":"lion","name":"Leo","age":7,"enclosure":"The Big Cat                               │
│    Plains","trail":"Savannah Heights"},...]                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯

✦ Leo can be found in The Big Cat Plains on the Savannah Heights.
  Nala can be found in The Big Cat Plains on the Savannah Heights.
  Simba can be found in The Big Cat Plains on the Savannah Heights.
  King can be found in The Big Cat Plains on the Savannah Heights.
```

The MCP prompt automatically instructs Gemini to format the response in a consistent, user-friendly way!