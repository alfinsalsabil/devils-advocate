import typer
import os
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv
import litellm
from rich.console import Console
import importlib.resources
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env if present
load_dotenv()

app = typer.Typer()
console = Console()

DEFAULT_MAX_STEPS = 15
SAFE_MAX_STEPS = 5
TRUNCATE_LIMIT = 4000

def validate_env():
    # LiteLLM can handle various keys, checking for general readiness
    pass

def truncate_output(text: str) -> str:
    if len(text) > TRUNCATE_LIMIT:
        return text[:2000] + "\n...[TRUNCATED]...\n" + text[-2000:]
    return text

async def read_file(file_path: str, mcp_session: ClientSession):
    """Read a file using MCP filesystem server."""
    try:
        # Check if the tool exists/works via MCP
        result = await mcp_session.call_tool("read_file", arguments={"path": file_path})
        # MCP server-filesystem returns content as a list of TextContent
        content = "".join([c.text for c in result.content if hasattr(c, 'text')])
        return truncate_output(content)
    except Exception as e:
        return f"Error reading file via MCP: {str(e)}"

async def write_file(file_path: str, content: str, mcp_session: ClientSession, auto_approve: bool = False):
    """Write to a file with HITL confirmation via MCP."""
    if auto_approve or typer.confirm(f"Do you want to write to {file_path}?"):
        try:
            result = await mcp_session.call_tool("write_file", arguments={"path": file_path, "content": content})
            output = "".join([c.text for c in result.content if hasattr(c, 'text')])
            return output or f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file via MCP: {str(e)}"
    return "SYSTEM: User rejected this action. Do not retry."

async def run_bash(command: str, mcp_session: ClientSession, auto_approve: bool = False):
    """Run a bash command with HITL confirmation via MCP (if supported) or locally."""
    if auto_approve or typer.confirm(f"Do you want to run the command: '{command}'?"):
        try:
            # Note: server-filesystem doesn't have run_bash, but we follow the middleware pattern.
            # If the MCP server doesn't support it, we could fall back or error.
            # For this PoC, we try to call it via MCP if available.
            result = await mcp_session.call_tool("run_bash", arguments={"command": command})
            output = "".join([c.text for c in result.content if hasattr(c, 'text')])
            return truncate_output(output)
        except Exception:
            # Fallback to local execution if MCP tool fails (e.g. not implemented in server-filesystem)
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout + result.stderr
                return truncate_output(output)
            except Exception as e:
                return f"Error running command locally: {str(e)}"
    return "SYSTEM: User rejected this action. Do not retry."

async def async_run(task: str, model: str, yes: bool):
    """Async implementation of the task runner with MCP integration."""
    validate_env()
    
    max_steps = DEFAULT_MAX_STEPS
    if yes:
        max_steps = SAFE_MAX_STEPS
        console.print("\n[bold red]WARNING: Autonomous mode (--yes) enabled.[/bold red]")
        console.print(f"[bold red]Limiting to {max_steps} steps to prevent excessive agency.[/bold red]\n")
    
    # Use importlib.resources to read SKILL.md from package data
    try:
        skill_content = importlib.resources.read_text("devils_advocate_cli.data", "SKILL.md")
    except Exception as e:
        console.print(f"[yellow]Warning: Could not load SKILL.md from package data: {e}[/yellow]")
        skill_content = ""
    
    system_prompt = f"You are an AI assistant following the Devil's Advocate workflow.\n\n{skill_content}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task}
    ]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read a file from the filesystem",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string"}
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Write content to a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["file_path", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "run_bash",
                "description": "Run a bash command",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"}
                    },
                    "required": ["command"]
                }
            }
        }
    ]

    base_dir = os.getcwd()
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", base_dir]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            console.print(f"[bold blue]Starting task with model {model}:[/bold blue] {task}")
            
            step = 0
            while step < max_steps:
                step += 1
                console.print(f"[bold green]Step {step}/{max_steps}[/bold green]")
                
                try:
                    response = litellm.completion(
                        model=model,
                        messages=messages,
                        tools=tools,
                        tool_choice="auto"
                    )
                    
                    assistant_message = response.choices[0].message
                    messages.append(assistant_message)
                    
                    if assistant_message.content:
                        console.print(f"[white]{assistant_message.content}[/white]")
                    
                    if not assistant_message.tool_calls:
                        break
                        
                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        args = json.loads(tool_call.function.arguments)
                        
                        console.print(f"[cyan]Calling tool: {tool_name}[/cyan]")
                        
                        if tool_name == "read_file":
                            result = await read_file(args["file_path"], session)
                        elif tool_name == "write_file":
                            result = await write_file(args["file_path"], args["content"], session, yes)
                        elif tool_name == "run_bash":
                            result = await run_bash(args["command"], session, yes)
                        else:
                            result = f"Error: Unknown tool {tool_name}"
                        
                        console.print(f"[magenta]Tool output:[/magenta] {result}")
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": result
                        })

                except Exception as e:
                    console.print(f"[red]Error during completion: {str(e)}[/red]")
                    break
                    
            if step >= max_steps:
                console.print(f"[bold red]Reached maximum iteration limit ({max_steps}). Exiting.[/bold red]")

@app.command()
def run(
    task: str, 
    model: str = typer.Option("gpt-4o", help="Model to use via LiteLLM"),
    yes: bool = typer.Option(False, "--yes", help="Auto-approve all actions")
):
    """
    Run a task using the Devil's Advocate workflow.
    """
    asyncio.run(async_run(task, model, yes))

if __name__ == "__main__":
    app()
