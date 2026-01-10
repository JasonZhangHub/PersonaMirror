"""
BFI-2 Scoring Pipeline

This module provides functionality to score BFI-2 survey responses,
calculating domain scores (Big Five traits) and facet scores.
"""

import json
from pathlib import Path
from dataclasses import dataclass, field

from src.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class FacetScore:
    """Score for a single BFI-2 facet."""
    name: str
    score: float
    items: list[int]
    raw_responses: dict[int, int]
    scored_responses: dict[int, int]  # After reverse scoring


@dataclass
class DomainScore:
    """Score for a single BFI-2 domain (Big Five trait)."""
    name: str
    code: str
    score: float
    interpretation: str
    items: list[int]
    facets: dict[str, FacetScore]
    raw_responses: dict[int, int]
    scored_responses: dict[int, int]


@dataclass
class BFI2Result:
    """Complete BFI-2 scoring result."""
    persona: str
    total_questions: int
    domains: dict[str, DomainScore]
    summary: dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        """Generate summary after initialization."""
        self.summary = {
            domain.code: domain.score
            for domain in self.domains.values()
        }

    def to_dict(self) -> dict:
        """Convert result to dictionary for JSON serialization."""
        return {
            "persona": self.persona,
            "total_questions": self.total_questions,
            "summary": self.summary,
            "domains": {
                name: {
                    "name": d.name,
                    "code": d.code,
                    "score": d.score,
                    "interpretation": d.interpretation,
                    "items": d.items,
                    "raw_responses": d.raw_responses,
                    "scored_responses": d.scored_responses,
                    "facets": {
                        fname: {
                            "name": f.name,
                            "score": f.score,
                            "items": f.items,
                            "raw_responses": f.raw_responses,
                            "scored_responses": f.scored_responses
                        }
                        for fname, f in d.facets.items()
                    }
                }
                for name, d in self.domains.items()
            }
        }


class BFI2Scorer:
    """
    Scores BFI-2 survey responses to calculate Big Five personality traits.

    Calculates both domain-level scores (Extraversion, Agreeableness,
    Conscientiousness, Neuroticism, Open-Mindedness) and facet-level scores.
    """

    def __init__(self):
        """Initialize the scorer with scoring configuration."""
        self.backend_path = Path(__file__).resolve().parent.parent.parent
        self.scoring_config = self._load_scoring_config()
        self.interpretation_ranges = self.scoring_config["interpretation"]["ranges"]
        logger.debug("Initialized BFI2Scorer")

    def _load_scoring_config(self) -> dict:
        """Load the BFI-2 scoring configuration."""
        scoring_path = self.backend_path / "data" / "bfi2" / "scoring.json"

        data = json.loads(scoring_path.read_text())
        logger.debug(f"Loaded scoring config from {scoring_path}")
        return data

    def _reverse_score(self, response: int, is_reverse: bool) -> int:
        """
        Apply reverse scoring if needed.

        Args:
            response: Original response (1-5)
            is_reverse: Whether this item should be reverse scored

        Returns:
            Scored value (1-5)
        """
        if is_reverse:
            return 6 - response
        return response

    def _interpret_score(self, score: float) -> str:
        """
        Interpret a domain/facet score based on predefined ranges.

        Args:
            score: Mean score (1.0-5.0)

        Returns:
            Interpretation label (e.g., "High", "Very High")
        """
        for range_name, range_info in self.interpretation_ranges.items():
            if range_info["min"] <= score < range_info["max"]:
                return range_info["label"]

        # Handle edge case for max score
        if score >= 5.0:
            return "Very High"
        return "Average"

    def _calculate_mean(self, values: list[int]) -> float:
        """Calculate mean and round to 2 decimal places."""
        if not values:
            return 0.0
        return round(sum(values) / len(values), 2)

    def score_facet(
        self,
        facet_name: str,
        facet_config: dict,
        responses: dict[int, int]
    ) -> FacetScore:
        """
        Calculate score for a single facet.

        Args:
            facet_name: Name of the facet
            facet_config: Configuration with items and reverseItems
            responses: Dictionary mapping question IDs to responses

        Returns:
            FacetScore object
        """
        items = facet_config["items"]
        reverse_items = set(facet_config.get("reverseItems", []))

        raw_responses = {item: responses.get(item, 3) for item in items}
        scored_responses = {
            item: self._reverse_score(resp, item in reverse_items)
            for item, resp in raw_responses.items()
        }

        score = self._calculate_mean(list(scored_responses.values()))

        return FacetScore(
            name=facet_name,
            score=score,
            items=items,
            raw_responses=raw_responses,
            scored_responses=scored_responses
        )

    def score_domain(
        self,
        domain_name: str,
        domain_config: dict,
        responses: dict[int, int]
    ) -> DomainScore:
        """
        Calculate score for a single domain (Big Five trait).

        Args:
            domain_name: Name of the domain
            domain_config: Configuration with items, reverseItems, and facets
            responses: Dictionary mapping question IDs to responses

        Returns:
            DomainScore object
        """
        items = domain_config["items"]
        reverse_items = set(domain_config.get("reverseItems", []))

        # Calculate raw and scored responses for domain
        raw_responses = {item: responses.get(item, 3) for item in items}
        scored_responses = {
            item: self._reverse_score(resp, item in reverse_items)
            for item, resp in raw_responses.items()
        }

        # Calculate domain score
        domain_score = self._calculate_mean(list(scored_responses.values()))

        # Calculate facet scores
        facets = {}
        for facet_name, facet_config in domain_config.get("facets", {}).items():
            facets[facet_name] = self.score_facet(
                facet_name, facet_config, responses)

        return DomainScore(
            name=domain_name,
            code=domain_config["code"],
            score=domain_score,
            interpretation=self._interpret_score(domain_score),
            items=items,
            facets=facets,
            raw_responses=raw_responses,
            scored_responses=scored_responses
        )

    def score(self, responses: dict[int, int], persona: str = "unknown") -> BFI2Result:
        """
        Score a complete set of BFI-2 responses.

        Args:
            responses: Dictionary mapping question IDs to responses (1-5)
            persona: Name of the persona (for labeling)

        Returns:
            BFI2Result object with all domain and facet scores
        """
        domains = {}

        for domain_name, domain_config in self.scoring_config["domains"].items():
            domains[domain_name] = self.score_domain(
                domain_name, domain_config, responses
            )

        logger.info(
            f"Scored {len(responses)} responses for persona: {persona}")
        return BFI2Result(
            persona=persona,
            total_questions=len(responses),
            domains=domains
        )

    def score_from_file(self, responses_path: Path) -> BFI2Result:
        """
        Score responses from a saved JSON file.

        Args:
            responses_path: Path to the responses JSON file

        Returns:
            BFI2Result object
        """
        data = json.loads(responses_path.read_text())

        # Convert string keys back to integers
        responses = {int(k): v for k, v in data["responses"].items()}
        persona = data.get("persona", "unknown")

        logger.info(f"Loaded responses from: {responses_path}")
        return self.score(responses, persona)


def print_results(result: BFI2Result):
    """Pretty print BFI-2 results to console."""
    print(f"\n{'=' * 70}")
    print(f"BFI-2 SCORING RESULTS: {result.persona}")
    print(f"{'=' * 70}")

    print(f"\n{'─' * 70}")
    print("DOMAIN SCORES (Big Five Traits)")
    print(f"{'─' * 70}")

    for domain_name, domain in result.domains.items():
        bar_length = int(domain.score * 10)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        print(f"\n{domain.name} ({domain.code})")
        print(f"  Score: {domain.score:.2f} / 5.00  [{domain.interpretation}]")
        print(f"  [{bar}]")

        print(f"\n  Facets:")
        for facet_name, facet in domain.facets.items():
            print(f"    • {facet_name}: {facet.score:.2f}")

    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")

    for code, score in result.summary.items():
        print(f"  {code}: {score:.2f}")

    print(f"\n{'=' * 70}\n")


def main():
    """Run a demo of the BFI-2 scoring pipeline."""
    logger.info("Starting BFI-2 Scorer demo")

    scorer = BFI2Scorer()

    # Check for existing responses file
    backend_path = Path(__file__).resolve().parent.parent.parent
    responses_path = (
        backend_path / "scripts" / "analysis" /
        "results" / "high_agreeableness_responses.json"
    )

    if responses_path.exists():
        print(f"Loading responses from: {responses_path}")
        result = scorer.score_from_file(responses_path)
    else:
        print("No responses file found. Creating sample data...")
        # Create sample responses for demo (simulating high agreeableness)
        # Default to "Agree a little"
        sample_responses = {i: 4 for i in range(1, 61)}

        # Boost agreeableness items
        agreeableness_items = [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57]
        for item in agreeableness_items:
            sample_responses[item] = 5  # Strongly agree

        result = scorer.score(
            sample_responses, persona="high_agreeableness_sample")

    # Print results
    print_results(result)

    # Save results
    results_dir = backend_path / "scripts" / "analysis" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    output_path = results_dir / f"{result.persona}_scored.json"
    output_path.write_text(json.dumps(result.to_dict(), indent=2))

    print(f"Scored results saved to: {output_path}")
    logger.info(f"Demo complete, results saved to: {output_path}")

    return result


if __name__ == "__main__":
    main()
