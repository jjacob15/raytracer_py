from raytracer.rays import run

def test_basic():
    items = run()
    assert len(items) == 90

