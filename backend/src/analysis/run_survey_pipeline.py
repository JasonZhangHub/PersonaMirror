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
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.persona_agent import PersonaAgent
from analysis.bfi2_scorer import BFI2Scorer, print_results


def run_pipeline(
    persona_name: str = "high_agreeableness",
    model: str = "gpt-4o",
    verbose: bool = True
) -> dict:
    """
    Run the complete BFI-2 survey pipeline for a persona.
    
    Args:
        persona_name: Name of the persona profile
        model: OpenAI model to use
        verbose: Whether to print progress
        
    Returns:
        Dictionary with responses and scored results
    """
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Step 1: Create agent and take survey
    if verbose:
        print(f"\n{'#'*70}")
        print(f"# STEP 1: Agent Taking BFI-2 Survey")
        print(f"# Persona: {persona_name}")
        print(f"# Model: {model}")
        print(f"{'#'*70}")
    
    agent = PersonaAgent(persona_name=persona_name, model=model)
    responses = agent.take_survey(verbose=verbose)
    
    # Save raw responses
    responses_path = results_dir / f"{persona_name}_responses_{timestamp}.json"
    responses_data = {
        "persona": persona_name,
        "model": model,
        "timestamp": timestamp,
        "total_questions": len(responses),
        "responses": responses
    }
    
    with open(responses_path, "w") as f:
        json.dump(responses_data, f, indent=2)
    
    if verbose:
        print(f"\nResponses saved to: {responses_path}")
    
    # Step 2: Score the responses
    if verbose:
        print(f"\n{'#'*70}")
        print(f"# STEP 2: Scoring BFI-2 Responses")
        print(f"{'#'*70}")
    
    scorer = BFI2Scorer()
    result = scorer.score(responses, persona=persona_name)
    
    # Print results
    if verbose:
        print_results(result)
    
    # Save scored results
    scored_path = results_dir / f"{persona_name}_scored_{timestamp}.json"
    with open(scored_path, "w") as f:
        json.dump(result.to_dict(), f, indent=2)
    
    if verbose:
        print(f"Scored results saved to: {scored_path}")
    
    # Also save a "latest" version for easy access
    latest_responses = results_dir / f"{persona_name}_responses.json"
    latest_scored = results_dir / f"{persona_name}_scored.json"
    
    with open(latest_responses, "w") as f:
        json.dump(responses_data, f, indent=2)
    
    with open(latest_scored, "w") as f:
        json.dump(result.to_dict(), f, indent=2)
    
    if verbose:
        print(f"\n{'#'*70}")
        print(f"# PIPELINE COMPLETE")
        print(f"{'#'*70}")
        print(f"\nFiles saved:")
        print(f"  • {responses_path}")
        print(f"  • {scored_path}")
        print(f"  • {latest_responses} (latest)")
        print(f"  • {latest_scored} (latest)")
    
    return {
        "responses": responses_data,
        "result": result.to_dict(),
        "paths": {
            "responses": str(responses_path),
            "scored": str(scored_path)
        }
    }


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Run BFI-2 survey pipeline with a persona agent"
    )
    parser.add_argument(
        "--persona", "-p",
        type=str,
        default="high_agreeableness",
        help="Persona name (e.g., high_agreeableness, high_conscientiousness)"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress verbose output"
    )
    
    args = parser.parse_args()
    
    run_pipeline(
        persona_name=args.persona,
        model=args.model,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()
