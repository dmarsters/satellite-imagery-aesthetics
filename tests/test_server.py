"""Tests for satellite imagery aesthetics MCP server."""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import yaml
from satellite_imagery_aesthetics.server import (
    imagery_profiles, altitude_perspectives, feature_emphasis, aesthetic_strength
)


class TestImageryProfiles:
    """Test imagery profile taxonomy."""
    
    def test_all_imagery_types_present(self):
        """Verify all 6 imagery types are present."""
        expected_types = [
            "false_color_infrared",
            "true_color_rgb",
            "thermal_infrared",
            "synthetic_aperture_radar",
            "lidar_elevation",
            "multispectral_agriculture"
        ]
        assert len(imagery_profiles) == 6
        assert set(imagery_profiles.keys()) == set(expected_types)
    
    def test_profile_completeness(self):
        """Verify each profile has all required dimensions."""
        required_dimensions = [
            "name", "structure", "material", "color", "texture",
            "composition", "style", "quality", "mood", "examples"
        ]
        
        for imagery_type, profile in imagery_profiles.items():
            assert isinstance(profile, dict), f"{imagery_type} is not a dict"
            for dimension in required_dimensions:
                assert dimension in profile, f"{imagery_type} missing {dimension}"
                assert isinstance(profile[dimension], str), f"{imagery_type}.{dimension} is not a string"
    
    def test_profile_non_empty(self):
        """Verify no profile dimensions are empty."""
        for imagery_type, profile in imagery_profiles.items():
            for dimension, value in profile.items():
                assert value and len(value) > 0, f"{imagery_type}.{dimension} is empty"


class TestAltitudePerspectives:
    """Test altitude perspective taxonomy."""
    
    def test_all_perspectives_present(self):
        """Verify all 4 altitude perspectives are present."""
        expected = ["orbital", "high_altitude", "medium_altitude", "low_altitude"]
        assert len(altitude_perspectives) == 4
        assert set(altitude_perspectives.keys()) == set(expected)
    
    def test_perspective_structure(self):
        """Verify each perspective has required fields."""
        required_fields = ["description", "scale", "context"]
        
        for perspective, data in altitude_perspectives.items():
            assert isinstance(data, dict)
            for field in required_fields:
                assert field in data, f"{perspective} missing {field}"
                assert isinstance(data[field], str) and len(data[field]) > 0


class TestFeatureEmphasis:
    """Test feature emphasis taxonomy."""
    
    def test_all_emphasis_types_present(self):
        """Verify all 4 feature emphasis types are present."""
        expected = ["natural", "urban", "abstract", "mixed"]
        assert len(feature_emphasis) == 4
        assert set(feature_emphasis.keys()) == set(expected)
    
    def test_emphasis_structure(self):
        """Verify each emphasis type has focus field."""
        for emphasis_type, data in feature_emphasis.items():
            assert isinstance(data, dict)
            assert "focus" in data
            assert isinstance(data["focus"], str) and len(data["focus"]) > 0


class TestAestheticStrength:
    """Test aesthetic strength taxonomy."""
    
    def test_all_strengths_present(self):
        """Verify all 3 aesthetic strengths are present."""
        expected = ["subtle", "balanced", "strong"]
        assert len(aesthetic_strength) == 3
        assert set(aesthetic_strength.keys()) == set(expected)
    
    def test_strength_structure(self):
        """Verify each strength has required fields."""
        required_fields = ["characteristics", "approach"]
        
        for strength, data in aesthetic_strength.items():
            assert isinstance(data, dict)
            for field in required_fields:
                assert field in data, f"{strength} missing {field}"
            assert isinstance(data["characteristics"], int)
            assert isinstance(data["approach"], str)
    
    def test_characteristic_counts(self):
        """Verify characteristic counts make sense."""
        assert aesthetic_strength["subtle"]["characteristics"] == 2
        assert aesthetic_strength["balanced"]["characteristics"] == 4
        assert aesthetic_strength["strong"]["characteristics"] == 6


class TestCombinations:
    """Test valid parameter combinations."""
    
    def test_total_combinations(self):
        """Verify total combinations count."""
        total = (len(imagery_profiles) * 
                 len(altitude_perspectives) * 
                 len(feature_emphasis) * 
                 len(aesthetic_strength))
        assert total == 288  # 6 × 4 × 4 × 3
    
    def test_sample_combinations(self):
        """Test a few representative combinations work."""
        test_cases = [
            ("false_color_infrared", "orbital", "natural", "strong"),
            ("true_color_rgb", "medium_altitude", "mixed", "balanced"),
            ("thermal_infrared", "high_altitude", "urban", "subtle"),
            ("lidar_elevation", "low_altitude", "abstract", "balanced"),
        ]
        
        for imagery, altitude, feature, strength in test_cases:
            # Just verify they all exist
            assert imagery in imagery_profiles
            assert altitude in altitude_perspectives
            assert feature in feature_emphasis
            assert strength in aesthetic_strength


def run_tests():
    """Run all tests and report results."""
    test_classes = [
        TestImageryProfiles,
        TestAltitudePerspectives,
        TestFeatureEmphasis,
        TestAestheticStrength,
        TestCombinations,
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}")
        print("-" * 60)
        
        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith("test_")]
        
        for test_method in test_methods:
            total_tests += 1
            try:
                getattr(instance, test_method)()
                print(f"  ✓ {test_method}")
                passed_tests += 1
            except AssertionError as e:
                print(f"  ✗ {test_method}: {e}")
                failed_tests += 1
            except Exception as e:
                print(f"  ✗ {test_method}: {type(e).__name__}: {e}")
                failed_tests += 1
    
    print("\n" + "=" * 60)
    print(f"Tests: {passed_tests} passed, {failed_tests} failed, {total_tests} total")
    
    if failed_tests == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {failed_tests} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
