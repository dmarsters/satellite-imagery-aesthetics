# Satellite Imagery Aesthetics MCP Server

Translates satellite and aerial imagery aesthetics into vivid visual language for image generation using a three-layer categorical architecture.

## Quick Start

```bash
pip install -e ".[dev]"
./tests/run_tests.sh
python -m satellite_imagery_aesthetics.server
```

## Architecture

- **Layer 1**: YAML olog taxonomy (6 imagery types × 8 dimensions)
- **Layer 2**: Deterministic parameter mapping (zero inference cost)
- **Layer 3**: Single Claude synthesis call

## Cost & Performance

- ~$0.0003 per enhancement (97% cheaper than pure LLM)
- <50ms overhead (deterministic layers)
- 288 valid parameter combinations

## Documentation

- `docs/architecture.md` - Deep dive
- `docs/usage.md` - How to use
- `docs/parameters.md` - Parameter reference
