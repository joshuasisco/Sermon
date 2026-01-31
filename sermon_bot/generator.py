"""
Core sermon generation logic using the 12-Module Preparation System.

This generator walks preachers through a pastoral preparation process
that prioritizes transformation over information.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import json

from .config import Config
from .prompts import (
    SYSTEM_PROMPT,
    MODULE_1_PROMPT,
    MODULE_2_PROMPT,
    MODULE_3_PROMPT,
    MODULE_4_PROMPT,
    MODULE_5_PROMPT,
    MODULE_6_PROMPT,
    MODULE_7_PROMPT,
    MODULE_8_PROMPT,
    MODULE_9_PROMPT,
    MODULE_10_PROMPT,
    MODULE_11_PROMPT,
    MODULE_12_PROMPT,
    FULL_SERMON_ASSEMBLY_PROMPT,
    QUICK_ILLUSTRATION_PROMPT,
    QUICK_SCRIPTURE_PROMPT,
    QUICK_SERIES_PROMPT,
)


@dataclass
class SermonSession:
    """Holds the state of a sermon preparation session."""

    # Input
    scripture: str = ""
    topic: str = ""

    # Module outputs
    transformation_goal: str = ""
    audience_analysis: str = ""
    target_condition: str = ""
    exegesis: str = ""
    text_movement: str = ""
    surprise_offense: str = ""
    modern_bridges: str = ""
    bottom_line: str = ""
    structure: str = ""
    applications: str = ""
    gospel_center: str = ""
    preacher_formation: str = ""

    # Final output
    full_sermon: str = ""

    # Metadata
    current_module: int = 0
    completed_modules: list = field(default_factory=list)

    def to_context(self) -> str:
        """Convert session state to context string for prompts."""
        parts = []
        if self.scripture:
            parts.append(f"Scripture: {self.scripture}")
        if self.topic:
            parts.append(f"Topic: {self.topic}")
        if self.transformation_goal:
            parts.append(f"Transformation Goal: {self.transformation_goal}")
        if self.audience_analysis:
            parts.append(f"Audience Analysis: {self.audience_analysis}")
        if self.target_condition:
            parts.append(f"Target Condition: {self.target_condition}")
        if self.exegesis:
            parts.append(f"Exegesis Summary: {self.exegesis[:500]}...")
        if self.text_movement:
            parts.append(f"Text Movement: {self.text_movement[:500]}...")
        if self.surprise_offense:
            parts.append(f"Surprise/Offense: {self.surprise_offense[:500]}...")
        if self.modern_bridges:
            parts.append(f"Modern Bridges: {self.modern_bridges[:500]}...")
        if self.bottom_line:
            parts.append(f"Bottom Line: {self.bottom_line}")
        if self.structure:
            parts.append(f"Structure: {self.structure[:500]}...")
        if self.applications:
            parts.append(f"Applications: {self.applications[:500]}...")
        if self.gospel_center:
            parts.append(f"Gospel Center: {self.gospel_center[:500]}...")
        return "\n\n".join(parts) if parts else "No context yet."

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for saving."""
        return {
            "scripture": self.scripture,
            "topic": self.topic,
            "transformation_goal": self.transformation_goal,
            "audience_analysis": self.audience_analysis,
            "target_condition": self.target_condition,
            "exegesis": self.exegesis,
            "text_movement": self.text_movement,
            "surprise_offense": self.surprise_offense,
            "modern_bridges": self.modern_bridges,
            "bottom_line": self.bottom_line,
            "structure": self.structure,
            "applications": self.applications,
            "gospel_center": self.gospel_center,
            "preacher_formation": self.preacher_formation,
            "full_sermon": self.full_sermon,
            "current_module": self.current_module,
            "completed_modules": self.completed_modules,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SermonSession":
        """Create session from dictionary."""
        session = cls()
        for key, value in data.items():
            if hasattr(session, key):
                setattr(session, key, value)
        return session


class SermonGenerator:
    """Generate sermons using the 12-Module Preparation System."""

    MODULE_NAMES = {
        1: "Define Preaching (Foundation)",
        2: "Identify the People (Audience)",
        3: "Pick the Text and Target",
        4: "Original Context Exegesis",
        5: "Find Movement in the Text",
        6: "Discover Surprise and Offense",
        7: "Bridge to Today",
        8: "Form the Bottom Line",
        9: "Build the Structure",
        10: "Application Engine",
        11: "Gospel Centering Check",
        12: "Preacher Formation",
    }

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with configuration."""
        self.config = config or Config.load()
        self._client = None
        self.session = SermonSession()

    def _get_client(self):
        """Get or create the AI client."""
        if self._client is None:
            if self.config.ai_provider == "anthropic":
                import anthropic
                self._client = anthropic.Anthropic(
                    api_key=self.config.anthropic_api_key
                )
            elif self.config.ai_provider == "openai":
                import openai
                self._client = openai.OpenAI(
                    api_key=self.config.openai_api_key
                )
        return self._client

    def _generate(self, user_prompt: str, system_prompt: str = SYSTEM_PROMPT) -> str:
        """Generate content using the configured AI provider."""
        client = self._get_client()

        if self.config.ai_provider == "anthropic":
            response = client.messages.create(
                model=self.config.default_model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text

        elif self.config.ai_provider == "openai":
            response = client.chat.completions.create(
                model=self.config.default_model,
                max_tokens=4096,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content

        raise ValueError(f"Unsupported AI provider: {self.config.ai_provider}")

    def new_session(self, scripture: str = "", topic: str = "") -> SermonSession:
        """Start a new sermon preparation session."""
        self.session = SermonSession(scripture=scripture, topic=topic)
        return self.session

    def get_module_name(self, module_num: int) -> str:
        """Get the name of a module by number."""
        return self.MODULE_NAMES.get(module_num, f"Module {module_num}")

    # =========================================================================
    # MODULE METHODS
    # =========================================================================

    def module_1_define_preaching(self, initial_thoughts: str = "") -> str:
        """Module 1: Define the transformation goal and preaching posture."""
        context = self.session.to_context()
        if initial_thoughts:
            context += f"\n\nPreacher's initial thoughts: {initial_thoughts}"

        prompt = MODULE_1_PROMPT.format(context=context)
        result = self._generate(prompt)

        self.session.transformation_goal = result
        self.session.current_module = 1
        if 1 not in self.session.completed_modules:
            self.session.completed_modules.append(1)

        return result

    def module_2_identify_audience(self, audience_notes: str = "") -> str:
        """Module 2: Understand the audience deeply."""
        context = self.session.to_context()
        if audience_notes:
            context += f"\n\nPreacher's notes about audience: {audience_notes}"

        prompt = MODULE_2_PROMPT.format(context=context)
        result = self._generate(prompt)

        self.session.audience_analysis = result
        self.session.current_module = 2
        if 2 not in self.session.completed_modules:
            self.session.completed_modules.append(2)

        return result

    def module_3_text_and_target(self, scripture: str = "", target_notes: str = "") -> str:
        """Module 3: Anchor in Scripture and identify the target condition."""
        if scripture:
            self.session.scripture = scripture

        context = self.session.to_context()
        if target_notes:
            context += f"\n\nPreacher's thoughts on target: {target_notes}"

        prompt = MODULE_3_PROMPT.format(context=context)
        result = self._generate(prompt)

        self.session.target_condition = result
        self.session.current_module = 3
        if 3 not in self.session.completed_modules:
            self.session.completed_modules.append(3)

        return result

    def module_4_exegesis(self, exegesis_notes: str = "") -> str:
        """Module 4: Original context exegesis."""
        context = self.session.to_context()
        if exegesis_notes:
            context += f"\n\nPreacher's exegetical notes: {exegesis_notes}"

        prompt = MODULE_4_PROMPT.format(
            scripture=self.session.scripture,
            context=context
        )
        result = self._generate(prompt)

        self.session.exegesis = result
        self.session.current_module = 4
        if 4 not in self.session.completed_modules:
            self.session.completed_modules.append(4)

        return result

    def module_5_find_movement(self, movement_notes: str = "") -> str:
        """Module 5: Find the movement in the text."""
        context = self.session.to_context()
        if movement_notes:
            context += f"\n\nPreacher's notes on movement: {movement_notes}"

        prompt = MODULE_5_PROMPT.format(
            scripture=self.session.scripture,
            context=context
        )
        result = self._generate(prompt)

        self.session.text_movement = result
        self.session.current_module = 5
        if 5 not in self.session.completed_modules:
            self.session.completed_modules.append(5)

        return result

    def module_6_surprise_offense(self, notes: str = "") -> str:
        """Module 6: Discover the surprise and offense in the text."""
        context = self.session.to_context()
        if notes:
            context += f"\n\nPreacher's notes: {notes}"

        prompt = MODULE_6_PROMPT.format(
            scripture=self.session.scripture,
            context=context
        )
        result = self._generate(prompt)

        self.session.surprise_offense = result
        self.session.current_module = 6
        if 6 not in self.session.completed_modules:
            self.session.completed_modules.append(6)

        return result

    def module_7_bridge_to_today(self, bridge_notes: str = "") -> str:
        """Module 7: Bridge the biblical world to today."""
        context = self.session.to_context()
        if bridge_notes:
            context += f"\n\nPreacher's bridge ideas: {bridge_notes}"

        prompt = MODULE_7_PROMPT.format(
            scripture=self.session.scripture,
            context=context
        )
        result = self._generate(prompt)

        self.session.modern_bridges = result
        self.session.current_module = 7
        if 7 not in self.session.completed_modules:
            self.session.completed_modules.append(7)

        return result

    def module_8_bottom_line(self, draft_ideas: str = "") -> str:
        """Module 8: Form the bottom line (single sentence)."""
        context = self.session.to_context()
        if draft_ideas:
            context += f"\n\nPreacher's draft bottom line ideas: {draft_ideas}"

        prompt = MODULE_8_PROMPT.format(
            scripture=self.session.scripture,
            context=context
        )
        result = self._generate(prompt)

        self.session.bottom_line = result
        self.session.current_module = 8
        if 8 not in self.session.completed_modules:
            self.session.completed_modules.append(8)

        return result

    def module_9_build_structure(self, structure_notes: str = "") -> str:
        """Module 9: Build the sermon structure (movements, chunks, seams)."""
        context = self.session.to_context()
        if structure_notes:
            context += f"\n\nPreacher's structure ideas: {structure_notes}"

        # Extract just the bottom line sentence if we have it
        bottom_line = self.session.bottom_line[:500] if self.session.bottom_line else "Not yet defined"

        prompt = MODULE_9_PROMPT.format(
            scripture=self.session.scripture,
            bottom_line=bottom_line,
            context=context
        )
        result = self._generate(prompt)

        self.session.structure = result
        self.session.current_module = 9
        if 9 not in self.session.completed_modules:
            self.session.completed_modules.append(9)

        return result

    def module_10_applications(self, application_notes: str = "") -> str:
        """Module 10: Create specific, embodied applications."""
        context = self.session.to_context()
        if application_notes:
            context += f"\n\nPreacher's application ideas: {application_notes}"

        bottom_line = self.session.bottom_line[:500] if self.session.bottom_line else "Not yet defined"

        prompt = MODULE_10_PROMPT.format(
            scripture=self.session.scripture,
            bottom_line=bottom_line,
            context=context
        )
        result = self._generate(prompt)

        self.session.applications = result
        self.session.current_module = 10
        if 10 not in self.session.completed_modules:
            self.session.completed_modules.append(10)

        return result

    def module_11_gospel_center(self, notes: str = "") -> str:
        """Module 11: Ensure Jesus is central, not optional."""
        context = self.session.to_context()
        if notes:
            context += f"\n\nPreacher's notes: {notes}"

        bottom_line = self.session.bottom_line[:500] if self.session.bottom_line else "Not yet defined"
        structure = self.session.structure[:1000] if self.session.structure else "Not yet defined"

        prompt = MODULE_11_PROMPT.format(
            scripture=self.session.scripture,
            bottom_line=bottom_line,
            structure=structure,
            context=context
        )
        result = self._generate(prompt)

        self.session.gospel_center = result
        self.session.current_module = 11
        if 11 not in self.session.completed_modules:
            self.session.completed_modules.append(11)

        return result

    def module_12_preacher_formation(self, personal_notes: str = "") -> str:
        """Module 12: Form the preacher, not just the sermon."""
        context = self.session.to_context()
        if personal_notes:
            context += f"\n\nPreacher's personal reflections: {personal_notes}"

        # Create a summary of the sermon so far
        summary = f"""
Scripture: {self.session.scripture}
Bottom Line: {self.session.bottom_line[:300] if self.session.bottom_line else 'TBD'}
Target: {self.session.target_condition[:300] if self.session.target_condition else 'TBD'}
"""

        prompt = MODULE_12_PROMPT.format(
            scripture=self.session.scripture,
            summary=summary,
            context=context
        )
        result = self._generate(prompt)

        self.session.preacher_formation = result
        self.session.current_module = 12
        if 12 not in self.session.completed_modules:
            self.session.completed_modules.append(12)

        return result

    def assemble_full_sermon(self) -> str:
        """Assemble the complete sermon from all module outputs."""
        prompt = FULL_SERMON_ASSEMBLY_PROMPT.format(
            scripture=self.session.scripture,
            bottom_line=self.session.bottom_line[:500] if self.session.bottom_line else "Not defined",
            audience=self.session.audience_analysis[:500] if self.session.audience_analysis else "Not defined",
            target_condition=self.session.target_condition[:500] if self.session.target_condition else "Not defined",
            structure=self.session.structure[:1000] if self.session.structure else "Not defined",
            applications=self.session.applications[:1000] if self.session.applications else "Not defined",
            gospel_center=self.session.gospel_center[:500] if self.session.gospel_center else "Not defined",
        )

        result = self._generate(prompt)
        self.session.full_sermon = result
        return result

    # =========================================================================
    # QUICK TOOLS (for standalone use)
    # =========================================================================

    def quick_illustrations(self, topic: str, scripture: str = "", bottom_line: str = "") -> str:
        """Generate illustrations without going through full modules."""
        prompt = QUICK_ILLUSTRATION_PROMPT.format(
            topic=topic,
            scripture=scripture or "Not specified",
            bottom_line=bottom_line or "Not specified"
        )
        return self._generate(prompt)

    def quick_scriptures(self, topic: str) -> str:
        """Find relevant scriptures for a topic."""
        prompt = QUICK_SCRIPTURE_PROMPT.format(topic=topic)
        return self._generate(prompt)

    def quick_series(self, theme: str, count: int = 4) -> str:
        """Design a sermon series."""
        prompt = QUICK_SERIES_PROMPT.format(theme=theme, count=count)
        return self._generate(prompt)

    def custom_request(self, request: str) -> str:
        """Handle a custom sermon-related request."""
        return self._generate(request)

    # =========================================================================
    # SESSION MANAGEMENT
    # =========================================================================

    def save_session(self, filepath: str) -> None:
        """Save the current session to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.session.to_dict(), f, indent=2)

    def load_session(self, filepath: str) -> SermonSession:
        """Load a session from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        self.session = SermonSession.from_dict(data)
        return self.session

    def get_progress(self) -> Dict[str, Any]:
        """Get the current progress through the modules."""
        return {
            "current_module": self.session.current_module,
            "completed_modules": self.session.completed_modules,
            "total_modules": 12,
            "percent_complete": len(self.session.completed_modules) / 12 * 100,
            "next_module": self._get_next_module(),
        }

    def _get_next_module(self) -> Optional[int]:
        """Get the next module that should be completed."""
        for i in range(1, 13):
            if i not in self.session.completed_modules:
                return i
        return None
