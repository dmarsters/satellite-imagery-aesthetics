import yaml
import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("satellite-imagery-aesthetics")

# Load YAML olog on startup
yaml_path = Path(__file__).parent / "ologs" / "imagery_profiles.yaml"
with open(yaml_path) as f:
    olog = yaml.safe_load(f)

imagery_profiles = olog["imagery_profiles"]
altitude_perspectives = olog["altitude_perspectives"]
feature_emphasis = olog["feature_emphasis"]
aesthetic_strength = olog["aesthetic_strength"]


@mcp.tool()
def list_imagery_types() -> str:
    """List all available satellite imagery types."""
    types = list(imagery_profiles.keys())
    return json.dumps({
        "imagery_types": types,
        "count": len(types)
    })


@mcp.tool()
def get_imagery_profile(imagery_type: str) -> str:
    """Layer 1: Retrieve complete profile data for an imagery type."""
    imagery_type_normalized = imagery_type.lower().replace(" ", "_")
    
    if imagery_type_normalized not in imagery_profiles:
        return json.dumps({
            "error": f"Unknown imagery type: {imagery_type}",
            "available": list(imagery_profiles.keys())
        })
    
    profile = imagery_profiles[imagery_type_normalized]
    return json.dumps({
        "imagery_type": imagery_type_normalized,
        "profile": profile
    })


@mcp.tool()
def list_altitude_perspectives() -> str:
    """List all available altitude perspectives for composition."""
    perspectives = list(altitude_perspectives.keys())
    details = {k: v for k, v in altitude_perspectives.items()}
    return json.dumps({
        "perspectives": perspectives,
        "details": details
    })


@mcp.tool()
def list_feature_emphasis_options() -> str:
    """List all available feature emphasis types."""
    options = list(feature_emphasis.keys())
    details = {k: v for k, v in feature_emphasis.items()}
    return json.dumps({
        "options": options,
        "details": details
    })


@mcp.tool()
def list_aesthetic_strengths() -> str:
    """List all available aesthetic strength levels."""
    strengths = list(aesthetic_strength.keys())
    details = {k: v for k, v in aesthetic_strength.items()}
    return json.dumps({
        "strengths": strengths,
        "details": details
    })


@mcp.tool()
def map_satellite_parameters(imagery_type: str, altitude: str, 
                           feature_emphasis_type: str, strength: str) -> str:
    """Layer 2: Deterministic mapping of parameters (zero LLM cost)."""
    imagery_type_normalized = imagery_type.lower().replace(" ", "_")
    altitude_normalized = altitude.lower().replace(" ", "_")
    feature_normalized = feature_emphasis_type.lower().replace(" ", "_")
    strength_normalized = strength.lower().replace(" ", "_")
    
    # Validate all inputs
    errors = []
    if imagery_type_normalized not in imagery_profiles:
        errors.append(f"Unknown imagery type: {imagery_type}")
    if altitude_normalized not in altitude_perspectives:
        errors.append(f"Unknown altitude: {altitude}")
    if feature_normalized not in feature_emphasis:
        errors.append(f"Unknown feature emphasis: {feature_emphasis_type}")
    if strength_normalized not in aesthetic_strength:
        errors.append(f"Unknown aesthetic strength: {strength}")
    
    if errors:
        return json.dumps({"errors": errors})
    
    # Build semantic bridge
    profile = imagery_profiles[imagery_type_normalized]
    altitude_data = altitude_perspectives[altitude_normalized]
    feature_data = feature_emphasis[feature_normalized]
    strength_data = aesthetic_strength[strength_normalized]
    
    # Determine which characteristics to weave in
    characteristic_count = strength_data["characteristics"]
    all_characteristics = [
        ("structure", profile["structure"]),
        ("material", profile["material"]),
        ("color", profile["color"]),
        ("texture", profile["texture"]),
        ("composition", profile["composition"]),
        ("style", profile["style"]),
        ("quality", profile["quality"]),
        ("mood", profile["mood"])
    ]
    
    # Select top N characteristics based on strength
    selected_characteristics = all_characteristics[:characteristic_count]
    
    mapped_parameters = {
        "imagery_type": imagery_type_normalized,
        "profile_name": profile["name"],
        "altitude_perspective": {
            "type": altitude_normalized,
            "description": altitude_data["description"],
            "scale": altitude_data["scale"],
            "context": altitude_data["context"]
        },
        "feature_emphasis": {
            "type": feature_normalized,
            "focus": feature_data["focus"]
        },
        "aesthetic_strength": {
            "type": strength_normalized,
            "approach": strength_data["approach"],
            "characteristic_count": characteristic_count
        },
        "selected_characteristics": {
            name: value for name, value in selected_characteristics
        },
        "all_available_characteristics": {
            name: value for name, value in all_characteristics
        },
        "examples": profile["examples"],
        "output_format": "60-80 words, natural sentence flow, vivid artistic language, ending with 'highly detailed, 8k, satellite imagery aesthetic'"
    }
    
    return json.dumps(mapped_parameters, indent=2)


@mcp.tool()
def get_enhancement_guidance(imagery_type: str, altitude: str,
                            feature_emphasis_type: str, strength: str) -> str:
    """Get human-readable guidance for enhancement parameters."""
    imagery_type_normalized = imagery_type.lower().replace(" ", "_")
    altitude_normalized = altitude.lower().replace(" ", "_")
    feature_normalized = feature_emphasis_type.lower().replace(" ", "_")
    strength_normalized = strength.lower().replace(" ", "_")
    
    if imagery_type_normalized not in imagery_profiles:
        return json.dumps({"error": f"Unknown imagery type: {imagery_type}"})
    
    profile = imagery_profiles[imagery_type_normalized]
    altitude_data = altitude_perspectives.get(altitude_normalized)
    feature_data = feature_emphasis.get(feature_normalized)
    strength_data = aesthetic_strength.get(strength_normalized)
    
    guidance = f"""
SATELLITE IMAGERY ENHANCEMENT GUIDANCE

Imagery Type: {profile['name']}
Altitude Perspective: {altitude_data.get('description', 'Unknown') if altitude_data else 'Unknown'}
Feature Emphasis: {feature_data.get('focus', 'Unknown') if feature_data else 'Unknown'}
Aesthetic Strength: {strength_data.get('approach', 'Unknown') if strength_data else 'Unknown'}

Key Visual Elements:
- Colors: {profile['color']}
- Textures: {profile['texture']}
- Mood: {profile['mood']}

Examples to draw from: {profile['examples']}

Remember:
1. Preserve the user's core concept completely
2. Use vivid, artistic language
3. Emphasize HOW it looks (colors, patterns, perspective), not WHAT it is
4. End with "highly detailed, 8k, satellite imagery aesthetic"
5. Never add subjects the user didn't request
"""
    
    return guidance.strip()


if __name__ == "__main__":
    mcp.run()
