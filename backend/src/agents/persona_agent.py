"""
Persona Agent Module

This module provides the PersonaAgent class that can take personality surveys
based on a defined persona profile. The agent uses an LLM to respond to survey
questions in a manner consistent with its assigned personality traits.
"""

import json
import os
from pathlib import Path
from typing import Optional
from openai import OpenAI


class PersonaAgent:
    """
    An AI agent that responds to personality surveys based on a defined persona.
    
    The agent loads a persona profile (system prompt) and uses it to guide
    responses to BFI-2 survey questions, simulating how a person with that
    personality would answer.
    """
    
    def __init__(
        self,
        persona_name: str,
        model: str = "gpt-4o",
        api_key: Optional[str] = None
    ):
        """
        Initialize the PersonaAgent.
        
        Args:
            persona_name: Name of the persona profile (e.g., "high_agreeableness")
            model: OpenAI model to use for responses
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.persona_name = persona_name
        self.model = model
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
        # Load paths
        self.base_path = Path(__file__).parent.parent.parent
        self.data_path = self.base_path / "data"
        
        # Load persona and survey data
        self.system_prompt = self._load_persona_prompt()
        self.questions = self._load_questions()
        self.responses: dict[int, int] = {}
        
    def _load_persona_prompt(self) -> str:
        """Load the persona system prompt from the prompts folder."""
        prompt_path = self.data_path / "prompts" / f"{self.persona_name}.md"
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Persona prompt not found: {prompt_path}")
        
        with open(prompt_path, "r") as f:
            content = f.read()
        
        # Extract the system prompt from the markdown file
        # The prompt is between ```\n and \n```
        start_marker = "## System Prompt\n\n```\n"
        end_marker = "\n```\n"
        
        start_idx = content.find(start_marker)
        if start_idx == -1:
            # Fallback: use the entire content
            return content
        
        start_idx += len(start_marker)
        end_idx = content.find(end_marker, start_idx)
        
        if end_idx == -1:
            return content[start_idx:]
        
        return content[start_idx:end_idx]
    
    def _load_questions(self) -> list[dict]:
        """Load BFI-2 questions from the data folder."""
        questions_path = self.data_path / "bfi2" / "questions.json"
        
        with open(questions_path, "r") as f:
            data = json.load(f)
        
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
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=10,
            temperature=0.3  # Lower temperature for more consistent responses
        )
        
        answer_text = response.choices[0].message.content.strip()
        
        # Parse the response to get the number
        try:
            answer = int(answer_text[0])  # Get first character in case of extra text
            if answer < 1 or answer > 5:
                answer = 3  # Default to neutral if invalid
        except (ValueError, IndexError):
            answer = 3  # Default to neutral if parsing fails
            
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
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"Agent '{self.persona_name}' taking BFI-2 survey...")
            print(f"{'='*60}\n")
        
        for i, question in enumerate(self.questions):
            answer = self.answer_question(question)
            self.responses[question["id"]] = answer
            
            if verbose:
                print(f"Q{question['id']:2d} [{question['domain']}] {question['text'][:40]:<40} -> {answer}")
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"Survey complete! {len(self.responses)} questions answered.")
            print(f"{'='*60}\n")
        
        return self.responses
    
    def save_responses(self, output_path: Optional[Path] = None) -> Path:
        """
        Save the survey responses to a JSON file.
        
        Args:
            output_path: Custom output path (defaults to analysis folder)
            
        Returns:
            Path to the saved file
        """
        if not self.responses:
            raise ValueError("No responses to save. Run take_survey() first.")
        
        if output_path is None:
            output_dir = self.base_path / "src" / "analysis" / "results"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{self.persona_name}_responses.json"
        
        output_data = {
            "persona": self.persona_name,
            "model": self.model,
            "total_questions": len(self.responses),
            "responses": self.responses
        }
        
        with open(output_path, "w") as f:
            json.dump(output_data, f, indent=2)
        
        print(f"Responses saved to: {output_path}")
        return output_path


def main():
    """Run a demo of the PersonaAgent taking the BFI-2 survey."""
    # Create agent with high agreeableness persona
    agent = PersonaAgent(persona_name="high_agreeableness")
    
    # Take the survey
    responses = agent.take_survey(verbose=True)
    
    # Save responses
    output_path = agent.save_responses()
    
    print(f"\nResponses saved to: {output_path}")
    return responses


if __name__ == "__main__":
    main()
