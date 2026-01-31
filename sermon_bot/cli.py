"""
Command-line interface for the 12-Module Sermon Preparation System.

This CLI guides preachers through a pastoral preparation process
that prioritizes transformation over information.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table

from .config import Config
from .generator import SermonGenerator


console = Console()

# Session storage directory
SESSIONS_DIR = Path("sessions")


def print_result(content: str, title: str = "Result"):
    """Print formatted result to console."""
    console.print()
    console.print(Panel(Markdown(content), title=title, border_style="green"))
    console.print()


def print_module_header(module_num: int, module_name: str):
    """Print a module header."""
    console.print()
    console.print(Panel(
        f"[bold white]Module {module_num}[/bold white]\n{module_name}",
        border_style="blue",
        padding=(1, 2)
    ))


def save_to_file(content: str, prefix: str = "sermon") -> str:
    """Save content to a file and return the filename."""
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/{prefix}_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(content)
    return filename


def check_config():
    """Check if the configuration is valid."""
    config = Config.load()
    if not config.validate():
        console.print(
            "[red]Error:[/red] API key not configured.\n"
            "Please copy .env.example to .env and add your API key.",
            style="bold"
        )
        console.print(f"[yellow]Current provider:[/yellow] {config.ai_provider}")
        sys.exit(1)
    return config


def show_progress_table(generator: SermonGenerator):
    """Display a progress table showing completed modules."""
    progress = generator.get_progress()

    table = Table(title="Sermon Preparation Progress", border_style="blue")
    table.add_column("#", style="dim", width=4)
    table.add_column("Module", style="cyan")
    table.add_column("Status", justify="center")

    for i in range(1, 13):
        name = generator.get_module_name(i)
        if i in progress["completed_modules"]:
            status = "[green]Complete[/green]"
        elif i == progress["next_module"]:
            status = "[yellow]Next[/yellow]"
        else:
            status = "[dim]Pending[/dim]"
        table.add_row(str(i), name, status)

    console.print()
    console.print(table)
    console.print(f"\n[bold]Progress:[/bold] {progress['percent_complete']:.0f}% complete")


@click.group()
@click.version_option(version="2.0.0")
def cli():
    """Sermon AI Bot - 12-Module Sermon Preparation System

    A pastoral preparation tool that guides you from text to transformation.

    QUICK START:
      sermon prep        - Full guided preparation (recommended)
      sermon module 1    - Work on a specific module

    QUICK TOOLS:
      sermon scriptures  - Find scriptures for a topic
      sermon illustrations - Generate illustrations
      sermon series      - Plan a sermon series
    """
    pass


# =============================================================================
# MAIN PREPARATION WORKFLOW
# =============================================================================

@cli.command()
@click.option("--scripture", "-s", default="", help="Starting Bible passage")
@click.option("--topic", "-t", default="", help="Starting topic (if no specific passage)")
@click.option("--resume", "-r", default="", help="Resume from a saved session file")
def prep(scripture: str, topic: str, resume: str):
    """Start the full 12-module sermon preparation workflow.

    This is the recommended way to prepare a sermon. It walks you through
    each module sequentially, building context as you go.

    Examples:
      sermon prep -s "John 3:16"
      sermon prep -t "forgiveness"
      sermon prep -r sessions/my_sermon.json
    """
    config = check_config()
    generator = SermonGenerator(config)

    # Resume or start new
    if resume:
        if os.path.exists(resume):
            generator.load_session(resume)
            console.print(f"[green]Resumed session from:[/green] {resume}")
            show_progress_table(generator)
        else:
            console.print(f"[red]Session file not found:[/red] {resume}")
            return
    else:
        # Get scripture or topic if not provided
        if not scripture and not topic:
            console.print(Panel(
                "[bold]Welcome to the Sermon Preparation System[/bold]\n\n"
                "This tool will walk you through 12 modules designed to help you\n"
                "move from biblical text to transformational proclamation.\n\n"
                "[dim]Based on the principle: Preaching is proclamation aimed at\n"
                "transformation of the heart, not just information transfer.[/dim]",
                title="Sermon AI Bot",
                border_style="blue"
            ))

            choice = Prompt.ask(
                "\n[bold]Start with[/bold]",
                choices=["verse", "topic"],
                default="verse"
            )

            if choice == "verse":
                scripture = Prompt.ask("[bold]Enter Bible reference[/bold]")
            else:
                topic = Prompt.ask("[bold]Enter sermon topic[/bold]")

        generator.new_session(scripture=scripture, topic=topic)

    # Main preparation loop
    while True:
        progress = generator.get_progress()
        next_module = progress["next_module"]

        if next_module is None:
            # All modules complete
            console.print("\n[bold green]All modules complete![/bold green]")
            if Confirm.ask("Would you like to assemble the full sermon?"):
                with console.status("[bold green]Assembling sermon..."):
                    result = generator.assemble_full_sermon()
                print_result(result, "Complete Sermon")

                if Confirm.ask("Save to file?"):
                    filename = save_to_file(result, "sermon_complete")
                    console.print(f"[green]Saved to:[/green] {filename}")
            break

        # Show current progress
        show_progress_table(generator)

        # Ask what to do
        console.print(f"\n[bold]Next module:[/bold] {next_module}. {generator.get_module_name(next_module)}")

        action = Prompt.ask(
            "[bold]Action[/bold]",
            choices=["continue", "skip", "jump", "save", "quit"],
            default="continue"
        )

        if action == "quit":
            if Confirm.ask("Save session before quitting?"):
                save_session_interactive(generator)
            break

        elif action == "save":
            save_session_interactive(generator)
            continue

        elif action == "skip":
            generator.session.completed_modules.append(next_module)
            console.print(f"[yellow]Skipped module {next_module}[/yellow]")
            continue

        elif action == "jump":
            jump_to = Prompt.ask("Jump to module number", default=str(next_module))
            try:
                next_module = int(jump_to)
                if not 1 <= next_module <= 12:
                    console.print("[red]Module must be 1-12[/red]")
                    continue
            except ValueError:
                console.print("[red]Invalid module number[/red]")
                continue

        # Run the module
        run_module(generator, next_module)


def run_module(generator: SermonGenerator, module_num: int):
    """Run a specific module."""
    module_name = generator.get_module_name(module_num)
    print_module_header(module_num, module_name)

    # Get optional preacher notes
    notes = ""
    if Confirm.ask("Do you have any thoughts or notes to add?", default=False):
        notes = Prompt.ask("[dim]Your notes[/dim]")

    # Run the appropriate module
    with console.status(f"[bold green]Processing Module {module_num}..."):
        if module_num == 1:
            result = generator.module_1_define_preaching(notes)
        elif module_num == 2:
            result = generator.module_2_identify_audience(notes)
        elif module_num == 3:
            # Module 3 might need scripture input
            if not generator.session.scripture:
                scripture = Prompt.ask("[bold]Enter the primary Scripture passage[/bold]")
                result = generator.module_3_text_and_target(scripture=scripture, target_notes=notes)
            else:
                result = generator.module_3_text_and_target(target_notes=notes)
        elif module_num == 4:
            result = generator.module_4_exegesis(notes)
        elif module_num == 5:
            result = generator.module_5_find_movement(notes)
        elif module_num == 6:
            result = generator.module_6_surprise_offense(notes)
        elif module_num == 7:
            result = generator.module_7_bridge_to_today(notes)
        elif module_num == 8:
            result = generator.module_8_bottom_line(notes)
        elif module_num == 9:
            result = generator.module_9_build_structure(notes)
        elif module_num == 10:
            result = generator.module_10_applications(notes)
        elif module_num == 11:
            result = generator.module_11_gospel_center(notes)
        elif module_num == 12:
            result = generator.module_12_preacher_formation(notes)
        else:
            console.print(f"[red]Unknown module: {module_num}[/red]")
            return

    print_result(result, f"Module {module_num}: {module_name}")

    # Option to save output
    if Confirm.ask("Save this module's output?", default=False):
        filename = save_to_file(result, f"module_{module_num}")
        console.print(f"[green]Saved to:[/green] {filename}")


def save_session_interactive(generator: SermonGenerator):
    """Save the current session interactively."""
    SESSIONS_DIR.mkdir(exist_ok=True)

    default_name = f"sermon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    if generator.session.scripture:
        default_name = f"sermon_{generator.session.scripture.replace(' ', '_').replace(':', '-')}.json"

    filename = Prompt.ask("[bold]Session filename[/bold]", default=default_name)
    filepath = SESSIONS_DIR / filename

    generator.save_session(str(filepath))
    console.print(f"[green]Session saved to:[/green] {filepath}")


# =============================================================================
# INDIVIDUAL MODULE ACCESS
# =============================================================================

@cli.command()
@click.argument("module_num", type=int)
@click.option("--scripture", "-s", default="", help="Bible passage for context")
@click.option("--notes", "-n", default="", help="Your notes or thoughts")
@click.option("--save", is_flag=True, help="Save output to file")
def module(module_num: int, scripture: str, notes: str, save: bool):
    """Run a specific module directly.

    MODULE_NUM: The module number (1-12)

    Modules:
      1  - Define Preaching (Foundation)
      2  - Identify the People (Audience)
      3  - Pick the Text and Target
      4  - Original Context Exegesis
      5  - Find Movement in the Text
      6  - Discover Surprise and Offense
      7  - Bridge to Today
      8  - Form the Bottom Line
      9  - Build the Structure
      10 - Application Engine
      11 - Gospel Centering Check
      12 - Preacher Formation

    Example:
      sermon module 4 -s "Romans 8:28" -n "Congregation struggling with suffering"
    """
    if not 1 <= module_num <= 12:
        console.print("[red]Module number must be between 1 and 12[/red]")
        return

    config = check_config()
    generator = SermonGenerator(config)

    if scripture:
        generator.session.scripture = scripture

    module_name = generator.get_module_name(module_num)
    print_module_header(module_num, module_name)

    with console.status(f"[bold green]Processing Module {module_num}..."):
        run_module(generator, module_num)


# =============================================================================
# QUICK TOOLS
# =============================================================================

@cli.command()
@click.argument("topic")
@click.option("--save", "-s", is_flag=True, help="Save output to file")
def scriptures(topic: str, save: bool):
    """Find relevant Bible passages for a sermon topic.

    Example: sermon scriptures "dealing with anxiety"
    """
    config = check_config()
    generator = SermonGenerator(config)

    console.print(f"\n[bold blue]Finding scriptures for:[/bold blue] {topic}")

    with console.status("[bold green]Searching..."):
        result = generator.quick_scriptures(topic)

    print_result(result, f"Scripture Suggestions: {topic}")

    if save:
        filename = save_to_file(result, "scriptures")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.argument("topic")
@click.option("--scripture", "-sc", default="", help="Related scripture for context")
@click.option("--bottom-line", "-bl", default="", help="The sermon's bottom line")
@click.option("--save", "-s", is_flag=True, help="Save output to file")
def illustrations(topic: str, scripture: str, bottom_line: str, save: bool):
    """Generate sermon illustrations for a topic.

    Example: sermon illustrations "hope" -sc "Romans 5:1-5"
    """
    config = check_config()
    generator = SermonGenerator(config)

    console.print(f"\n[bold blue]Generating illustrations for:[/bold blue] {topic}")

    with console.status("[bold green]Generating..."):
        result = generator.quick_illustrations(topic, scripture, bottom_line)

    print_result(result, f"Illustrations: {topic}")

    if save:
        filename = save_to_file(result, "illustrations")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.argument("theme")
@click.option("--count", "-c", default=4, help="Number of sermons in the series")
@click.option("--save", "-s", is_flag=True, help="Save output to file")
def series(theme: str, count: int, save: bool):
    """Plan a sermon series on a theme.

    Example: sermon series "The Beatitudes" --count 8
    """
    config = check_config()
    generator = SermonGenerator(config)

    console.print(f"\n[bold blue]Planning {count}-week series on:[/bold blue] {theme}")

    with console.status("[bold green]Planning series..."):
        result = generator.quick_series(theme, count)

    print_result(result, f"Sermon Series: {theme}")

    if save:
        filename = save_to_file(result, "series")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.option("--save", "-s", is_flag=True, help="Save output to file")
def ask(save: bool):
    """Ask a custom sermon-related question.

    Example: sermon ask
    """
    config = check_config()
    generator = SermonGenerator(config)

    request = Prompt.ask("[bold]What would you like help with?[/bold]")

    with console.status("[bold green]Thinking..."):
        result = generator.custom_request(request)

    print_result(result, "Response")

    if save:
        filename = save_to_file(result, "custom")
        console.print(f"[green]Saved to:[/green] {filename}")


# =============================================================================
# SESSION MANAGEMENT
# =============================================================================

@cli.command()
def sessions():
    """List saved sermon preparation sessions."""
    SESSIONS_DIR.mkdir(exist_ok=True)

    session_files = list(SESSIONS_DIR.glob("*.json"))

    if not session_files:
        console.print("[dim]No saved sessions found.[/dim]")
        console.print("Start a new session with: [bold]sermon prep[/bold]")
        return

    table = Table(title="Saved Sessions", border_style="blue")
    table.add_column("Filename", style="cyan")
    table.add_column("Modified", style="dim")

    for f in sorted(session_files, key=lambda x: x.stat().st_mtime, reverse=True):
        mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        table.add_row(f.name, mtime)

    console.print(table)
    console.print("\nResume with: [bold]sermon prep -r sessions/<filename>[/bold]")


# =============================================================================
# CONFIGURATION
# =============================================================================

@cli.command()
def config():
    """Show current configuration."""
    cfg = Config.load()

    console.print(Panel(
        f"[bold]AI Provider:[/bold] {cfg.ai_provider}\n"
        f"[bold]Model:[/bold] {cfg.default_model}\n"
        f"[bold]API Key Configured:[/bold] {'Yes' if cfg.validate() else 'No'}",
        title="Configuration",
        border_style="blue"
    ))


@cli.command()
def modules():
    """List all 12 preparation modules."""
    table = Table(title="12-Module Sermon Preparation System", border_style="blue")
    table.add_column("#", style="dim", width=4)
    table.add_column("Module", style="cyan")
    table.add_column("Purpose", style="dim")

    module_purposes = {
        1: "Clarify transformation goal, not just information",
        2: "Understand both churched and unchurched listeners",
        3: "Anchor in Scripture, identify target condition",
        4: "Understand original context before application",
        5: "Trace geographic, emotional, theological movement",
        6: "Recover the sharp edge of Scripture",
        7: "Make ancient truth emotionally present",
        8: "Distill to one memorable sentence",
        9: "Build movements, chunks, and seams",
        10: "Create specific, embodied, achievable applications",
        11: "Ensure Jesus is central, not optional",
        12: "Form the preacher, not just the sermon",
    }

    for i in range(1, 13):
        name = SermonGenerator.MODULE_NAMES[i]
        purpose = module_purposes[i]
        table.add_row(str(i), name, purpose)

    console.print()
    console.print(table)
    console.print("\nRun individual modules with: [bold]sermon module <number>[/bold]")
    console.print("Start full preparation with: [bold]sermon prep[/bold]")


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
