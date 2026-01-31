# Sermon AI Bot

A pastoral sermon preparation system that guides preachers from biblical text to transformational proclamation.

## Philosophy

> **Preaching is not information transfer. Preaching is proclamation that aims at transformation of the heart and affections.**

This tool doesn't just generate content—it thinks like:
- A **pastor** who cares for souls
- A **communicator** who connects truth to real life
- A **spiritual guide** who leads people toward transformation
- A **cultural translator** who bridges ancient text to modern experience

## The 12-Module System

| # | Module | Purpose |
|---|--------|---------|
| 1 | **Define Preaching** | Clarify transformation goal, not just information |
| 2 | **Identify the People** | Understand both churched and unchurched listeners |
| 3 | **Pick Text & Target** | Anchor in Scripture, identify target condition |
| 4 | **Original Context** | Understand what the text meant THEN |
| 5 | **Find Movement** | Trace geographic, emotional, theological movement |
| 6 | **Surprise & Offense** | Recover the sharp edge of Scripture |
| 7 | **Bridge to Today** | Make ancient truth emotionally present |
| 8 | **Bottom Line** | Distill to one memorable sentence (C.R.E.A.M.) |
| 9 | **Build Structure** | Create movements, chunks, and seams |
| 10 | **Applications** | Specific, embodied, achievable applications |
| 11 | **Gospel Center** | Ensure Jesus is central, not optional |
| 12 | **Preacher Formation** | Form the preacher, not just the sermon |

## Installation

### Prerequisites

- Python 3.8+
- API key from [Anthropic](https://console.anthropic.com/) or [OpenAI](https://platform.openai.com/)

### Setup

```bash
# Clone and enter directory
git clone https://github.com/yourusername/Sermon.git
cd Sermon

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your API key

# (Optional) Install as command
pip install -e .
```

## Usage

### Full Sermon Preparation (Recommended)

The `prep` command walks you through all 12 modules sequentially:

```bash
# Start with a Bible passage
sermon prep -s "John 3:16"

# Start with a topic
sermon prep -t "forgiveness"

# Resume a saved session
sermon prep -r sessions/my_sermon.json
```

During preparation, you can:
- **continue** - Run the next module
- **skip** - Skip to the following module
- **jump** - Jump to a specific module number
- **save** - Save your progress
- **quit** - Exit (with option to save)

### Individual Modules

Run any module directly:

```bash
sermon module 4 -s "Romans 8:28"
sermon module 8 -s "Psalm 23" -n "Focus on God's provision in uncertainty"
```

### Quick Tools

```bash
# Find scriptures for a topic
sermon scriptures "dealing with anxiety"

# Generate illustrations
sermon illustrations "hope" -sc "Romans 5:1-5"

# Plan a sermon series
sermon series "The Beatitudes" --count 8

# Ask a custom question
sermon ask
```

### Session Management

```bash
# List saved sessions
sermon sessions

# Resume a session
sermon prep -r sessions/sermon_John_3-16.json
```

### View Module List

```bash
sermon modules
```

## The Preparation Flow

### Module 1: Define Preaching
*"What transformation should this sermon invite people into?"*

Before content, clarify the **why**:
- Transformation goal (not just learning)
- Heart target (fear→trust, despair→hope, pride→humility)
- Proclamation posture (announcing, calling, comforting, challenging)

### Module 2: Identify the People
*"Who is in the room?"*

Every sermon speaks to:
- **Younger Brother**: Unchurched, skeptical, seeking
- **Older Brother**: Churched, possibly burned out or complacent
- **Universal struggles**: What keeps everyone up at 2am?

### Module 3: Pick Text & Target
*"What needs healing, confronting, or re-orienting?"*

- Anchor in Scripture (the text has authority)
- Identify the target condition
- Ask: "Who is this message MOST for?"

### Module 4: Original Context
*"What did this mean THEN?"*

- Before/after context
- Historical setting
- Literary genre
- What was at stake for original hearers?

### Module 5: Find Movement
*"How does this passage journey?"*

Trace the movement:
- Geographic (where does it go?)
- Emotional (what shifts?)
- Theological (lost→found, broken→restored, blind→seeing)

### Module 6: Surprise & Offense
*"What edge has familiarity dulled?"*

- What surprises modern listeners?
- What offends natural instincts?
- How does offense become invitation?

### Module 7: Bridge to Today
*"Where does this show up in Tuesday life?"*

- Shared human emotions
- Family, work, inner, cultural parallels
- Create "That's me" moments

### Module 8: Bottom Line
*"If they remember one sentence in 10 years?"*

Apply the **C.R.E.A.M.** filter:
- **C**ontrast
- **R**hyme
- **E**cho
- **A**lliteration
- **M**etaphor

### Module 9: Build Structure
*"How do we move people from here to there?"*

The **Movements—Chunks—Seams** model:
- **Movements**: Introduction → Tension → Revelation → Invitation
- **Chunks**: Stories, exegesis, illustrations, applications
- **Seams**: Transitions that make the journey clear

### Module 10: Applications
*"What does obedience look like Monday at 9am?"*

Applications must be:
- **Specific** (not "love more" but "text the person who hurt you")
- **Embodied** (involves action)
- **Achievable** (this week)
- **Grace-rooted** (flows from what God has done)

### Module 11: Gospel Center
*"How does this collapse without Jesus?"*

Run the checks:
- **Collapse Test**: Could a non-Christian preach this?
- **Moralism Detector**: Is this "try harder" or "Christ has"?
- Make the Person, Work, Presence, and Promise of Jesus explicit

### Module 12: Preacher Formation
*"Let the sermon form you before you deliver it."*

- Where has this text confronted YOU?
- Where should you "preach with a limp"?
- What spiritual preparation is needed?

## Configuration

Edit `.env`:

```bash
# AI Provider: "anthropic" or "openai"
AI_PROVIDER=anthropic

# API Key
ANTHROPIC_API_KEY=your-key-here

# Model (optional)
DEFAULT_MODEL=claude-sonnet-4-20250514
```

## Python API

```python
from sermon_bot.generator import SermonGenerator

generator = SermonGenerator()

# Start a new session
generator.new_session(scripture="John 3:16")

# Work through modules
result = generator.module_1_define_preaching("I want people to move from fear to trust")
result = generator.module_2_identify_audience()
result = generator.module_3_text_and_target()
# ... continue through module 12 ...

# Assemble final sermon
sermon = generator.assemble_full_sermon()

# Save/load sessions
generator.save_session("my_sermon.json")
generator.load_session("my_sermon.json")
```

## Output Structure

The final assembled sermon includes:
- **Title**
- **Opening** (2-3 min): Hook, felt need, roadmap
- **Movement 1: Tension** (5-7 min): Build the problem
- **Movement 2: Text** (8-10 min): Walk through Scripture
- **Movement 3: Truth** (5-7 min): Deliver bottom line, gospel-center
- **Movement 4: Transformation** (5-7 min): Specific applications
- **Closing** (2-3 min): Memorable landing, final gospel word

## Contributing

Contributions welcome! Please submit issues and pull requests.

## License

MIT License - See LICENSE file for details.

---

*"You cannot give what you do not have. Let the sermon form you before you deliver it."*
