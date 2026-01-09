"""
BFI-2 Survey Pipeline

This script runs the complete pipeline:
1. Creates a PersonaAgent with the specified persona
2. Has the agent take the BFI-2 survey
3. Scores the responses
4. Saves and displays results
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from scripts.agent_pretest.persona_agent import PersonaAgent
from scripts.analysis.bfi2_scorer import BFI2Scorer, print_results
from src.settings import app_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_pipeline(
    persona_name: str = "high_agreeableness",
    model: str | None = None,
    verbose: bool = True,
) -> dict:
    """
    Run the complete BFI-2 survey pipeline for a persona.

    Args:
        persona_name: Name of the persona profile
        model: Model to use (defaults to settings)
        verbose: Whether to print progress

    Returns:
        Dictionary with responses and scored results
    """
    # Use model from settings if not specified
    model = model or app_settings.openrouter.model_name

    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    logger.info(
        f"Starting pipeline for persona: {persona_name}, model: {model}")

    # Step 1: Create agent and take survey
    if verbose:
        print(f"\n{'#' * 70}")
        print(f"# STEP 1: Agent Taking BFI-2 Survey")
        print(f"# Persona: {persona_name}")
        print(f"# Model: {model}")
        print(f"{'#' * 70}")

    agent = PersonaAgent(persona_name=persona_name, model=model)
    responses = agent.take_survey(verbose=verbose)

    # Save raw responses
    responses_path = results_dir / f"{persona_name}_responses_{timestamp}.json"
    responses_data = {
        "persona": persona_name,
        "model": model,
        "timestamp": timestamp,
        "total_questions": len(responses),
        "responses": responses,
    }

    responses_path.write_text(json.dumps(responses_data, indent=2))
    logger.info(f"Responses saved to: {responses_path}")

    if verbose:
        print(f"\nResponses saved to: {responses_path}")

    # Step 2: Score the responses
    if verbose:
        print(f"\n{'#' * 70}")
        print(f"# STEP 2: Scoring BFI-2 Responses")
        print(f"{'#' * 70}")

    scorer = BFI2Scorer()
    result = scorer.score(responses, persona=persona_name)

    # Print results
    if verbose:
        print_results(result)

    # Save scored results
    scored_path = results_dir / f"{persona_name}_scored_{timestamp}.json"
    scored_path.write_text(json.dumps(result.to_dict(), indent=2))
    logger.info(f"Scored results saved to: {scored_path}")

    if verbose:
        print(f"Scored results saved to: {scored_path}")

    # Also save a "latest" version for easy access
    latest_responses = results_dir / f"{persona_name}_responses.json"
    latest_scored = results_dir / f"{persona_name}_scored.json"

    latest_responses.write_text(json.dumps(responses_data, indent=2))
    latest_scored.write_text(json.dumps(result.to_dict(), indent=2))

    if verbose:
        print(f"\n{'#' * 70}")
        print(f"# PIPELINE COMPLETE")
        print(f"{'#' * 70}")
        print(f"\nFiles saved:")
        print(f"  • {responses_path}")
        print(f"  • {scored_path}")
        print(f"  • {latest_responses} (latest)")
        print(f"  • {latest_scored} (latest)")

    logger.info("Pipeline complete")

    return {
        "responses": responses_data,
        "result": result.to_dict(),
        "paths": {
            "responses": str(responses_path),
            "scored": str(scored_path),
        },
    }


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Run BFI-2 survey pipeline with a persona agent"
    )
    parser.add_argument(
        "--persona",
        "-p",
        type=str,
        default="high_agreeableness",
        choices=[
            "high_agreeableness",
            "high_conscientiousness",
            "high_neuroticism",
            "neutral_control",
        ],
        help="Persona name (default: high_agreeableness)",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help=f"Model to use (default: from settings - {app_settings.openrouter.model_name})",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress verbose output",
    )

    args = parser.parse_args()

    logger.info(
        f"CLI args: persona={args.persona}, model={args.model}, quiet={args.quiet}")

    run_pipeline(
        persona_name=args.persona,
        model=args.model,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
