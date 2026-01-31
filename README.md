# Sermon AI Bot

An AI-powered sermon generation assistant that helps pastors, ministers, and church leaders create meaningful, biblically-grounded sermons.

## Features

- **Sermon from Verse**: Generate complete sermons from any Bible passage
- **Sermon from Topic**: Create sermons on specific themes or topics
- **Sermon Outlines**: Get structured outlines to guide your sermon preparation
- **Illustrations**: Generate engaging illustrations for your sermons
- **Scripture Suggestions**: Find relevant Bible passages for any topic
- **Sermon Series**: Plan multi-week sermon series
- **Prayers**: Generate opening, closing, and responsive prayers
- **Interactive Mode**: Step-by-step guided sermon creation

## Installation

### Prerequisites

- Python 3.8 or higher
- An API key from either [Anthropic](https://console.anthropic.com/) or [OpenAI](https://platform.openai.com/)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Sermon.git
   cd Sermon
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

5. (Optional) Install as a command:
   ```bash
   pip install -e .
   ```

## Configuration

Edit the `.env` file to configure the bot:

```bash
# Choose your AI provider: "anthropic" or "openai"
AI_PROVIDER=anthropic

# Your API key
ANTHROPIC_API_KEY=your-key-here
# or
OPENAI_API_KEY=your-key-here

# Model selection (optional)
DEFAULT_MODEL=claude-sonnet-4-20250514
```

## Usage

### Command Line

After installation, you can use the `sermon` command:

```bash
# Generate a sermon from a Bible verse
sermon verse "John 3:16"
sermon verse "Romans 8:28-30" --length "30 minutes" --save

# Generate a sermon on a topic
sermon topic "forgiveness"
sermon topic "faith in difficult times" --save

# Generate a sermon outline
sermon outline "Philippians 4:6-7"
sermon outline "prayer" --topic  # Treat as topic, not verse

# Get sermon illustrations
sermon illustrations "hope" --scripture "Romans 5:1-5"

# Find relevant scriptures for a topic
sermon scriptures "dealing with anxiety"

# Plan a sermon series
sermon series "The Beatitudes" --count 8

# Generate prayers for a sermon
sermon prayers "grace" --scripture "Ephesians 2:8-9"

# Start interactive mode
sermon interactive

# Check configuration
sermon config
```

### Running as a Module

```bash
python -m sermon_bot verse "John 3:16"
python -m sermon_bot interactive
```

### Python API

```python
from sermon_bot.generator import SermonGenerator

generator = SermonGenerator()

# Generate a sermon from a verse
sermon = generator.generate_sermon_from_verse("John 3:16")
print(sermon)

# Generate a sermon on a topic
sermon = generator.generate_sermon_from_topic("forgiveness")
print(sermon)

# Generate an outline
outline = generator.generate_outline("Psalm 23", is_verse=True)
print(outline)

# Get illustrations
illustrations = generator.generate_illustrations("hope", scripture="Romans 5:1-5")
print(illustrations)
```

## Output Options

All commands support saving output to files:

```bash
sermon verse "John 3:16" --save
# Saves to output/sermon_verse_YYYYMMDD_HHMMSS.md
```

## Examples

### Generate a sermon from John 3:16

```bash
sermon verse "John 3:16" --length "20 minutes"
```

Output includes:
- Compelling title
- Engaging introduction
- Historical context
- 3-4 main points with illustrations and applications
- Cross references
- Powerful conclusion
- Discussion questions

### Plan a 4-part series on "The Fruit of the Spirit"

```bash
sermon series "The Fruit of the Spirit" --count 4
```

Output includes:
- Series overview
- For each sermon: title, scripture, theme, description
- How sermons connect and build on each other
- Visual branding suggestions

## Supported AI Providers

### Anthropic (Claude)
- claude-opus-4-5-20251101 (most capable)
- claude-sonnet-4-20250514 (balanced, default)

### OpenAI
- gpt-4o (recommended)
- gpt-4-turbo

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- Beautiful output with [Rich](https://rich.readthedocs.io/)
- AI powered by [Anthropic Claude](https://www.anthropic.com/) and [OpenAI](https://openai.com/)
