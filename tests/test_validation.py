import pytest

from validation import validate_generation_params, validate_prompt


def test_validate_prompt_strips_whitespace():
    assert validate_prompt("  a cat walking  ") == "a cat walking"


@pytest.mark.parametrize("value", ["", "   ", None])
def test_validate_prompt_rejects_empty(value):
    with pytest.raises(ValueError, match="Prompt is required"):
        validate_prompt(value)


def test_validate_prompt_rejects_oversized_prompt():
    with pytest.raises(ValueError, match="1000"):
        validate_prompt("x" * 1001)


def test_validate_generation_params_accepts_bounds():
    assert validate_generation_params(8, 17, 1.0) == (8, 17, 1.0)
    assert validate_generation_params(40, 49, 12.0) == (40, 49, 12.0)


@pytest.mark.parametrize("steps", [7, 41])
def test_validate_generation_params_rejects_steps(steps):
    with pytest.raises(ValueError, match="steps"):
        validate_generation_params(steps, 25, 6.0)


def test_validate_generation_params_rejects_frames():
    with pytest.raises(ValueError, match="Frames"):
        validate_generation_params(20, 26, 6.0)


@pytest.mark.parametrize("guidance", [0.9, 12.1])
def test_validate_generation_params_rejects_guidance(guidance):
    with pytest.raises(ValueError, match="Guidance"):
        validate_generation_params(20, 25, guidance)
