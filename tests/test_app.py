import pytest
from app import (
    detect_emotion,
    create_forest_animation,
    create_ocean_animation,
    create_neon_animation,
)


def test_detect_emotion_output_format():
    """Test that detect_emotion returns expected keys and value ranges."""
    result = detect_emotion("I feel great today!")
    assert isinstance(result, dict)
    assert set(result.keys()) == {"emotion", "intensity"}
    assert result["emotion"] in {"joy", "sadness", "anger", "fear", "surprise"}
    assert 0.0 < result["intensity"] <= 1.0


@pytest.mark.parametrize(
    "generator",
    [
        create_forest_animation,
        create_ocean_animation,
        create_neon_animation,
    ],
)
def test_animation_generator_returns_pil(generator):
    """Each animation function must return a PIL.Image.Image with correct size."""
    dummy_emotions = [{"emotion": "joy", "intensity": 0.8}]
    img = generator(dummy_emotions)

    from PIL.Image import Image as PILImage

    assert isinstance(img, PILImage)
    assert img.size == (1000, 600)