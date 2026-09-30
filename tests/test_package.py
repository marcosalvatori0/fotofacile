import fotofacile


def test_version_esposta():
    assert fotofacile.__version__ == "0.2.0"


def test_core_importabile():
    import fotofacile.core  # noqa: F401
