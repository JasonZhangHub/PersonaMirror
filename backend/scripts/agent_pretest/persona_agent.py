"""
Persona Agent Module

This module provides the PersonaAgent class that can take personality surveys
based on a defined persona profile. The agent uses an LLM to respond to survey
questions in a manner consistent with its assigned personality traits.
"""

import json
from pathlib import Path
from typing import Optional

from openai import OpenAI

from src.settings import app_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PersonaAgent:
    """
    An AI agent that responds to personality surveys based on a defined persona.

    The agent loads a persona profile (system prompt) and uses it to guide
    responses to BFI-2 survey questions, simulating how a person with that
    personality would answer.
    """

    # Constants
    RESPONSE_MIN = 1
    RESPONSE_MAX = 5
    RESPONSE_NEUTRAL = 3

    def __init__(
        self,
        persona_name: str,
        model: Optional[str] = None,
    ):
        """
        Initialize the PersonaAgent.

        Args:
            persona_name: Name of the persona profile (e.g., "high_agreeableness")
            model: Model to use for responses (defaults to settings)
        """
        self.persona_name = persona_name
        self.model = model or app_settings.openrouter.model_name

        # Initialize OpenRouter client (OpenAI-compatible API)
        self.client = OpenAI(
            base_url=app_settings.openrouter.base_url,
            api_key=app_settings.openrouter.api_key,
        )

        # Set up paths
        self.backend_path = Path(__file__).resolve().parent.parent.parent
        self.data_path = self.backend_path / "data"

        # Load persona and survey data
        self.system_prompt = self._load_persona_prompt()
        self.questions = self._load_questions()
        self.responses: dict[int, int] = {}

        logger.info(
            f"Initialized PersonaAgent",
            extra={"persona": persona_name, "model": self.model},
        )

    def _load_persona_prompt(self) -> str:
        """Load the persona system prompt from the prompts folder."""
        prompt_path = self.data_path / "prompts" / f"{self.persona_name}.md"

        if not prompt_path.exists():
            logger.error(f"Persona prompt not found: {prompt_path}")
            raise FileNotFoundError(f"Persona prompt not found: {prompt_path}")

        content = prompt_path.read_text()

        # Extract the system prompt from the markdown file
        # The prompt is between ```\n and \n```
        start_marker = "## System Prompt\n\n```\n"
        end_marker = "\n```\n"

        start_idx = content.find(start_marker)
        if start_idx == -1:
            logger.warning(
                "System prompt markers not found, using entire file content")
            return content

        start_idx += len(start_marker)
        end_idx = content.find(end_marker, start_idx)

        if end_idx == -1:
            return content[start_idx:]

        return content[start_idx:end_idx]

    def _load_questions(self) -> list[dict]:
        """Load BFI-2 questions from the data folder."""
        questions_path = self.data_path / "bfi2" / "questions.json"

        data = json.loads(questions_path.read_text())
        logger.debug(f"Loaded {len(data['items'])} survey questions")

        return data["items"]

    def _create_survey_prompt(self, question: dict) -> str:
        """Create a prompt for the agent to answer a single survey question."""
        return f"""You are taking a personality survey. Answer the following question based on your personality and how you genuinely see yourself.

Question: "I am someone who {question['text'].lower()}"

Response options:
1 - Disagree strongly
2 - Disagree a little
3 - Neutral; no opinion
4 - Agree a little
5 - Agree strongly

Based on your personality, which response (1-5) best describes you?

IMPORTANT: Respond with ONLY a single number (1, 2, 3, 4, or 5). No explanation needed."""

    def answer_question(self, question: dict) -> int:
        """
        Have the agent answer a single survey question.

        Args:
            question: Question dict with 'id', 'text', 'domain', 'facet', 'reverse'

        Returns:
            Integer response (1-5)
        """
        user_prompt = self._create_survey_prompt(question)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=10,
            temperature=0.3,  # Lower temperature for more consistent responses
        )

        answer_text = response.choices[0].message.content.strip()

        # Parse the response to get the number
        try:
            # Get first character in case of extra text
            answer = int(answer_text[0])
            if not (self.RESPONSE_MIN <= answer <= self.RESPONSE_MAX):
                logger.warning(
                    f"Invalid response {answer} for Q{question['id']}, defaulting to neutral"
                )
                answer = self.RESPONSE_NEUTRAL
        except (ValueError, IndexError):
            logger.warning(
                f"Failed to parse response '{answer_text}' for Q{question['id']}, defaulting to neutral"
            )
            answer = self.RESPONSE_NEUTRAL

        return answer

    def take_survey(self, verbose: bool = True) -> dict[int, int]:
        """
        Have the agent complete the entire BFI-2 survey.

        Args:
            verbose: Whether to print progress

        Returns:
            Dictionary mapping question IDs to responses (1-5)
        """
        self.responses = {}

        logger.info(f"Starting BFI-2 survey for persona: {self.persona_name}")

        if verbose:
            print(f"\n{'=' * 60}")
            print(f"Agent '{self.persona_name}' taking BFI-2 survey...")
            print(f"{'=' * 60}\n")

        for question in self.questions:
            answer = self.answer_question(question)
            self.responses[question["id"]] = answer

            if verbose:
                print(
                    f"Q{question['id']:2d} [{question['domain']}] "
                    f"{question['text'][:40]:<40} -> {answer}"
                )

        logger.info(
            f"Survey complete: {len(self.responses)} questions answered")

        if verbose:
            print(f"\n{'=' * 60}")
            print(
                f"Survey complete! {len(self.responses)} questions answered.")
            print(f"{'=' * 60}\n")

        return self.responses

    def save_responses(self, output_path: Optional[Path] = None) -> Path:
        """Save survey responses to a JSON file."""
        if output_path is None:
            results_dir = self.backend_path / "scripts" / "analysis" / "results"
            results_dir.mkdir(parents=True, exist_ok=True)
            output_path = results_dir / f"{self.persona_name}_responses.json"

        output_data = {
            "persona": self.persona_name,
            "model": self.model,
            "responses": self.responses,
        }

        output_path.write_text(json.dumps(output_data, indent=2))
        logger.info(f"Saved responses to {output_path}")

        return output_path


def main():
    """Run a demo of the PersonaAgent taking the BFI-2 survey."""
    logger.info("Starting PersonaAgent demo")

    # Create agent with high agreeableness persona
    agent = PersonaAgent(persona_name="high_agreeableness")

    # Take the survey
    responses = agent.take_survey(verbose=True)

    # Save responses
    output_path = agent.save_responses()

    print(f"\nResponses saved to: {output_path}")
    logger.info(f"Demo complete, responses saved to: {output_path}")

    return responses


if __name__ == "__main__":
    main()
