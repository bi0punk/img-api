"""Smoke tests para img-api: mapeo de filtros y aplicación sin eval()."""

from __future__ import annotations

import io
from pathlib import Path

import pytest
from PIL import Image

from bin.filters import FILTERS, apply_filter, get_filter

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_readme_exists():
    assert (REPO_ROOT / "README.md").exists()


def test_expected_filters_registered():
    for name in ("blur", "sharpen", "smooth", "emboss"):
        assert name in FILTERS


def test_get_filter_returns_pil_filter():
    assert get_filter("blur") is not None


def test_get_filter_rejects_unknown():
    with pytest.raises(ValueError):
        get_filter("does_not_exist")


def test_apply_filter_returns_jpeg_bytes():
    src = io.BytesIO()
    Image.new("RGB", (8, 8), color="red").save(src, format="PNG")
    src.seek(0)

    out = apply_filter(src, "blur")
    assert out.read(2) == b"\xff\xd8"  # JPEG magic bytes
