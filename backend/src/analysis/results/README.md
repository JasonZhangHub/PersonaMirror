# Results Directory

This directory stores the output from BFI-2 survey runs:

- `{persona}_responses.json` - Raw survey responses from the agent
- `{persona}_scored.json` - Scored results with domain and facet calculations

## File Structure

### Response Files
```json
{
  "persona": "high_agreeableness",
  "model": "gpt-4o",
  "timestamp": "20260109_143022",
  "total_questions": 60,
  "responses": {
    "1": 4,
    "2": 5,
    ...
  }
}
```

### Scored Files
```json
{
  "persona": "high_agreeableness",
  "total_questions": 60,
  "summary": {
    "E": 3.5,
    "A": 4.67,
    "C": 3.25,
    "N": 2.08,
    "O": 3.42
  },
  "domains": {
    "Extraversion": { ... },
    "Agreeableness": { ... },
    ...
  }
}
```
