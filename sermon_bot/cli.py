"""Command-line interface for Sermon AI Bot."""

import os
import sys
from datetime import datetime

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from .config import Config
from .generator import SermonGenerator


console = Console()


def print_result(content: str, title: str = "Result"):
    """Print formatted result to console."""
    console.print()
    console.print(Panel(Markdown(content), title=title, border_style="green"))
    console.print()


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
            "[red]Error:[/red] API key not configured. "
            "Please copy .env.example to .env and add your API key.",
            style="bold"
        )
        console.print(f"[yellow]Current provider:[/yellow] {config.ai_provider}")
        sys.exit(1)
    return config


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Sermon AI Bot - Your AI-powered sermon writing assistant.

    Generate sermons, outlines, illustrations, and more using AI.
    """
    pass


@cli.command()
@click.argument("scripture")
@click.option(
    "--length", "-l",
    default="20-25 minutes",
    help="Target sermon length (e.g., '15 minutes', '30 minutes')"
)
@click.option(
    "--save", "-s",
    is_flag=True,
    help="Save the output to a file"
)
def verse(scripture: str, length: str, save: bool):
    """Generate a sermon from a Bible verse or passage.

    SCRIPTURE: The Bible reference (e.g., "John 3:16" or "Romans 8:28-30")
    """
    config = check_config()
    generator = SermonGenerator(config)

    console.print(f"\n[bold blue]Generating sermon from:[/bold blue] {scripture}")
    console.print("[dim]This may take a moment...[/dim]\n")

    with console.status("[bold green]Generating sermon..."):
        result = generator.generate_sermon_from_verse(scripture, length)

    print_result(result, f"Sermon: {scripture}")

    if save:
        filename = save_to_file(result, "sermon_verse")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.argument("topic")
@click.option(
    "--length", "-l",
    default="20-25 minutes",
    help="Target sermon length (e.g., '15 minutes', '30 minutes')"
)
@click.option(
    "--save", "-s",
    is_flag=True,
    help="Save the output to a file"
)
def topic(topic: str, length: str, save: bool):
    """Generate a sermon on a specific topic.

    TOPIC: The sermon topic (e.g., "forgiveness", "faith in difficult times")
    """
    config = check_config()
    generator = SermonGenerator(config)

    console.print(f"\n[bold blue]Generating sermon on:[/bold blue] {topic}")
    console.print("[dim]This may take a moment...[/dim]\n")

    with console.status("[bold green]Generating sermon..."):
        result = generator.generate_sermon_from_topic(topic, length)

    print_result(result, f"Sermon: {topic}")

    if save:
        filename = save_to_file(result, "sermon_topic")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.argument("input_value")
@click.option(
    "--verse", "-v",
    is_flag=True,
    default=True,
    help="Treat input as a Bible verse (default)"
)
@click.option(
    "--topic", "-t",
    is_flag=True,
    help="Treat input as a topic"
)
@click.option(
    "--save", "-s",
    is_flag=True,
    help="Save the output to a file"
)
def outline(input_value: str, verse: bool, topic: bool, save: bool):
    """Generate a sermon outline.

    INPUT_VALUE: A Bible verse or topic for the outline
    """
    config = check_config()
    generator = SermonGenerator(config)

    is_verse = not topic
    input_type = "verse" if is_verse else "topic"

    console.print(f"\n[bold blue]Generating outline from {input_type}:[/bold blue] {input_value}")
    console.print("[dim]This may take a moment...[/dim]\n")

    with console.status("[bold green]Generating outline..."):
        result = generator.generate_outline(input_value, is_verse)

    print_result(result, f"Sermon Outline: {input_value}")

    if save:
        filename = save_to_file(result, "outline")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.argument("topic")
@click.option(
    "--scripture", "-sc",
    default="",
    help="Related scripture for context"
)
@click.option(
    "--save", "-s",
    is_flag=True,
    help="Save the output to a file"
)
def illustrations(topic: str, scripture: str, save: bool):
    """Generate sermon illustrations for a topic.

    TOPIC: The topic or theme for illustrations
    """
    config = check_config()
    generator = SermonGenerator(config)

    console.print(f"\n[bold blue]Generating illustrations for:[/bold blue] {topic}")
    console.print("[dim]This may take a moment...[/dim]\n")

    with console.status("[bold green]Generating illustrations..."):
        result = generator.generate_illustrations(topic, scripture)

    print_result(result, f"Illustrations: {topic}")

    if save:
        filename = save_to_file(result, "illustrations")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.argument("topic")
@click.option(
    "--save", "-s",
    is_flag=True,
    help="Save the output to a file"
)
def scriptures(topic: str, save: bool):
    """Suggest Bible passages for a sermon topic.

    TOPIC: The topic to find scriptures for
    """
    config = check_config()
    generator = SermonGenerator(config)

    console.print(f"\n[bold blue]Finding scriptures for:[/bold blue] {topic}")
    console.print("[dim]This may take a moment...[/dim]\n")

    with console.status("[bold green]Finding scriptures..."):
        result = generator.suggest_scriptures(topic)

    print_result(result, f"Scripture Suggestions: {topic}")

    if save:
        filename = save_to_file(result, "scriptures")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.argument("theme")
@click.option(
    "--count", "-c",
    default=4,
    help="Number of sermons in the series"
)
@click.option(
    "--save", "-s",
    is_flag=True,
    help="Save the output to a file"
)
def series(theme: str, count: int, save: bool):
    """Generate a sermon series plan.

    THEME: The overarching theme for the series
    """
    config = check_config()
    generator = SermonGenerator(config)

    console.print(f"\n[bold blue]Generating {count}-part series on:[/bold blue] {theme}")
    console.print("[dim]This may take a moment...[/dim]\n")

    with console.status("[bold green]Generating series..."):
        result = generator.generate_sermon_series(theme, count)

    print_result(result, f"Sermon Series: {theme}")

    if save:
        filename = save_to_file(result, "series")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.argument("topic")
@click.option(
    "--scripture", "-sc",
    default="",
    help="Related scripture for context"
)
@click.option(
    "--save", "-s",
    is_flag=True,
    help="Save the output to a file"
)
def prayers(topic: str, scripture: str, save: bool):
    """Generate prayers for a sermon.

    TOPIC: The sermon topic for the prayers
    """
    config = check_config()
    generator = SermonGenerator(config)

    console.print(f"\n[bold blue]Generating prayers for:[/bold blue] {topic}")
    console.print("[dim]This may take a moment...[/dim]\n")

    with console.status("[bold green]Generating prayers..."):
        result = generator.generate_prayers(topic, scripture)

    print_result(result, f"Prayers: {topic}")

    if save:
        filename = save_to_file(result, "prayers")
        console.print(f"[green]Saved to:[/green] {filename}")


@cli.command()
@click.option(
    "--save", "-s",
    is_flag=True,
    help="Save the output to a file"
)
def interactive(save: bool):
    """Start an interactive sermon writing session."""
    config = check_config()
    generator = SermonGenerator(config)

    console.print(Panel(
        "[bold]Welcome to Sermon AI Bot Interactive Mode![/bold]\n\n"
        "I'll help you create sermons, outlines, and more.\n"
        "Type 'quit' or 'exit' to leave.",
        title="Sermon AI Bot",
        border_style="blue"
    ))

    while True:
        console.print("\n[bold cyan]What would you like to create?[/bold cyan]")
        console.print("1. Sermon from Bible verse")
        console.print("2. Sermon from topic")
        console.print("3. Sermon outline")
        console.print("4. Sermon illustrations")
        console.print("5. Scripture suggestions")
        console.print("6. Sermon series plan")
        console.print("7. Prayers")
        console.print("8. Custom request")
        console.print("9. Exit")

        choice = Prompt.ask(
            "\n[bold]Enter your choice[/bold]",
            choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "quit", "exit"],
            default="1"
        )

        if choice in ["9", "quit", "exit"]:
            console.print("\n[bold green]Thank you for using Sermon AI Bot. God bless![/bold green]\n")
            break

        result = None
        title = "Result"

        if choice == "1":
            scripture = Prompt.ask("[bold]Enter Bible reference[/bold]")
            length = Prompt.ask("[bold]Sermon length[/bold]", default="20-25 minutes")
            with console.status("[bold green]Generating sermon..."):
                result = generator.generate_sermon_from_verse(scripture, length)
            title = f"Sermon: {scripture}"

        elif choice == "2":
            topic = Prompt.ask("[bold]Enter sermon topic[/bold]")
            length = Prompt.ask("[bold]Sermon length[/bold]", default="20-25 minutes")
            with console.status("[bold green]Generating sermon..."):
                result = generator.generate_sermon_from_topic(topic, length)
            title = f"Sermon: {topic}"

        elif choice == "3":
            input_val = Prompt.ask("[bold]Enter verse or topic[/bold]")
            is_verse = Confirm.ask("[bold]Is this a Bible verse?[/bold]", default=True)
            with console.status("[bold green]Generating outline..."):
                result = generator.generate_outline(input_val, is_verse)
            title = f"Outline: {input_val}"

        elif choice == "4":
            topic = Prompt.ask("[bold]Enter topic for illustrations[/bold]")
            scripture = Prompt.ask("[bold]Related scripture (optional)[/bold]", default="")
            with console.status("[bold green]Generating illustrations..."):
                result = generator.generate_illustrations(topic, scripture)
            title = f"Illustrations: {topic}"

        elif choice == "5":
            topic = Prompt.ask("[bold]Enter topic to find scriptures[/bold]")
            with console.status("[bold green]Finding scriptures..."):
                result = generator.suggest_scriptures(topic)
            title = f"Scriptures: {topic}"

        elif choice == "6":
            theme = Prompt.ask("[bold]Enter series theme[/bold]")
            count = int(Prompt.ask("[bold]Number of sermons[/bold]", default="4"))
            with console.status("[bold green]Generating series..."):
                result = generator.generate_sermon_series(theme, count)
            title = f"Series: {theme}"

        elif choice == "7":
            topic = Prompt.ask("[bold]Enter sermon topic[/bold]")
            scripture = Prompt.ask("[bold]Related scripture (optional)[/bold]", default="")
            with console.status("[bold green]Generating prayers..."):
                result = generator.generate_prayers(topic, scripture)
            title = f"Prayers: {topic}"

        elif choice == "8":
            request = Prompt.ask("[bold]Enter your custom request[/bold]")
            with console.status("[bold green]Processing request..."):
                result = generator.custom_request(request)
            title = "Custom Request"

        if result:
            print_result(result, title)

            if save or Confirm.ask("[bold]Save to file?[/bold]", default=False):
                filename = save_to_file(result, title.lower().replace(" ", "_").replace(":", ""))
                console.print(f"[green]Saved to:[/green] {filename}")


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


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
