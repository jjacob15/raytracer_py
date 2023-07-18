import pytest
from raytracer.intersections import Intersection,Intersections
from raytracer.shapes import Sphere
from raytracer.rays import Ray
from raytracer.tuple import point,vector


def test_intersections_container() -> None:
    s = Sphere()
    intersections = Intersections([Intersection(1, s), Intersection(2, s)])

    assert len(intersections) == 2
    assert intersections[0].t == 1
    assert intersections[1].t == 2


def test_intersections_sorted() -> None:
    s = Sphere()
    intersections = Intersections([Intersection(2, s), Intersection(1, s)])

    assert intersections[0].t == 1


# P_INT = partial(Intersection, obj=Sphere())

def init_intersection(t:int):
    return Intersection(t=t,obj=Sphere())

HIT_TEST_CASES = (
    (Intersections([init_intersection(1), init_intersection(2)]), init_intersection(1)),
    # (Intersections([init_intersection(-1), init_intersection(1)]), init_intersection(1)),
    # (Intersections([init_intersection(-2), init_intersection(-1)]), None),
    # (Intersections([init_intersection(5), init_intersection(7), init_intersection(-3), init_intersection(2)]), init_intersection(2)),
)


@pytest.mark.parametrize(("intersections", "truth_hit"), HIT_TEST_CASES)
def test_hit(intersections: Intersections, truth_hit: Intersection) -> None:
    print(intersections.hit())
    print(truth_hit)
    assert intersections.hit() == truth_hit


# BASE_SHAPE = Sphere()
# COMPUTATIONS_CASES = (
#     (
#         Ray(point(0, 0, -5), vector(0, 0, 1)),
#         Intersection(4, BASE_SHAPE),
#         Comps(
#             t=4,
#             obj=BASE_SHAPE,
#             point=point(0, 0, -1),
#             eye_v=vector(0, 0, -1),
#             normal=vector(0, 0, -1),
#             inside=False,
#             n1=1,
#             n2=1,
#             reflect_v=vector(0, 0, -1),
#         ),
#     ),
#     (
#         Ray(point(0, 0, 0), vector(0, 0, 1)),
#         Intersection(1, BASE_SHAPE),
#         Comps(
#             t=1,
#             obj=BASE_SHAPE,
#             point=point(0, 0, 1),
#             eye_v=vector(0, 0, -1),
#             normal=vector(0, 0, -1),
#             inside=True,
#             n1=1,
#             n2=1,
#             reflect_v=vector(0, 0, -1),
#         ),
#     ),
# )    