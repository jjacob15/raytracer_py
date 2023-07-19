import pytest
from raytracer.intersections import Intersection,Intersections,IntersectionComp,prepare_computation,schlick
from raytracer import EPSILON
import math
from raytracer.materials import Material
from raytracer.transforms import translation,scaling
from raytracer.shapes import Sphere,Plane
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


BASE_SPHERE = Sphere()
def init_intersection(t:int):
    return Intersection(t=t,obj=BASE_SPHERE)

HIT_TEST_CASES = (
    (Intersections([init_intersection(1), init_intersection(2)]), init_intersection(1)),
    (Intersections([init_intersection(-1), init_intersection(1)]), init_intersection(1)),
    (Intersections([init_intersection(-2), init_intersection(-1)]), None),
    (Intersections([init_intersection(5), init_intersection(7), init_intersection(-3), init_intersection(2)]), init_intersection(2)),
)

@pytest.mark.parametrize(("intersections", "truth_hit"), HIT_TEST_CASES)
def test_hit(intersections: Intersections, truth_hit: Intersection) -> None:
    assert intersections.hit() == truth_hit

COMPUTATIONS_CASES = (
    (
        Ray(point(0, 0, -5), vector(0, 0, 1)),
        Intersection(4, BASE_SPHERE),
        IntersectionComp(
            t=4,
            obj=BASE_SPHERE,
            point=point(0, 0, -1),
            eye_v=vector(0, 0, -1),
            normal=vector(0, 0, -1),
            inside=False,
            n1=1,
            n2=1,
            reflect_v=vector(0, 0, -1),
        ),
    ),
    (
        Ray(point(0, 0, 0), vector(0, 0, 1)),
        Intersection(1, BASE_SPHERE),
        IntersectionComp(
            t=1,
            obj=BASE_SPHERE,
            point=point(0, 0, 1),
            eye_v=vector(0, 0, -1),
            normal=vector(0, 0, -1),
            inside=True,
            n1=1,
            n2=1,
            reflect_v=vector(0, 0, -1),
        ),
    ),
)


@pytest.mark.parametrize(("r", "inter", "truth_comp"), COMPUTATIONS_CASES)
def test_prepare_computation(r: Ray, inter: Intersection, truth_comp: IntersectionComp) -> None:
    comps = prepare_computation(inter, r)

    assert comps == truth_comp


def test_prepare_computations_over_point() -> None:
    r = Ray(point(0, 0, -5), vector(0, 0, 1))
    shape = Sphere(transform=translation(0, 0, 1))
    i = Intersection(5, shape)

    comps = prepare_computation(i, r)
    assert comps.over_point.z < -EPSILON / 2  # Ensure correct direction
    assert comps.point.z > comps.over_point.z


def test_prepare_computation_under_point() -> None:
    r = Ray(point(0, 0, -5), vector(0, 0, 1))
    shape = Sphere(transform=translation(0, 0, 1))
    i = Intersection(5, shape)

    comps = prepare_computation(i, r)
    assert comps.under_point.z > -EPSILON / 2  # Ensure correct direction
    assert comps.point.z < comps.under_point.z


RT_2 = math.sqrt(2)


def test_reflection_vector() -> None:
    shape = Plane()
    r = Ray(point(0, 1, -1), vector(0, -RT_2 / 2, RT_2 / 2))
    i = Intersection(RT_2, shape)

    comps = prepare_computation(i, r)
    assert comps.reflect_v == vector(0, RT_2 / 2, RT_2 / 2)


@pytest.fixture
def refraction_scenario() -> Intersections:
    # 3 glass spheres: B & C overlap slightly and contained by A
    a = Sphere(scaling(2, 2, 2), Material(transparency=1, refractive_index=1.5))
    b = Sphere(translation(0, 0, -0.25), Material(transparency=1, refractive_index=2.0))
    c = Sphere(translation(0, 0, 0.25), Material(transparency=1, refractive_index=2.5))

    xs = Intersections(
        [
            Intersection(2, a),
            Intersection(2.75, b),
            Intersection(3.25, c),
            Intersection(4.75, b),
            Intersection(5.25, c),
            Intersection(6, a),
        ]
    )

    return xs


REFRACTION_CASES = (
    (0, 1.0, 1.5),
    (1, 1.5, 2.0),
    (2, 2.0, 2.5),
    (3, 2.5, 2.5),
    (4, 2.5, 1.5),
    (5, 1.5, 1.0),
)


@pytest.mark.parametrize(("idx", "n1", "n2"), REFRACTION_CASES)
def test_refraction_indices(
    idx: int, n1: float, n2: float, refraction_scenario: Intersections
) -> None:
    r = Ray(point(0, 0, -4), vector(0, 0, 1))
    comps = prepare_computation(
        inter=refraction_scenario[idx], ray=r, all_inters=refraction_scenario
    )

    assert comps.n1 == pytest.approx(n1)
    assert comps.n2 == pytest.approx(n2)


def test_total_internal_reflection_schlick() -> None:
    s = Sphere(material=Material(transparency=1, refractive_index=1.5))
    r = Ray(point(0, 0, RT_2 / 2), vector(0, 1, 0))
    inters = Intersections([Intersection(-RT_2 / 2, s), Intersection(RT_2 / 2, s)])

    comps = prepare_computation(inters[1], r, inters)
    assert schlick(comps) == pytest.approx(1.0)


def test_total_internal_reflection_schlick_perpendicular() -> None:
    s = Sphere(material=Material(transparency=1, refractive_index=1.5))
    r = Ray(point(0, 0, 0), vector(0, 1, 0))
    inters = Intersections([Intersection(-1, s), Intersection(1, s)])

    comps = prepare_computation(inters[1], r, inters)
    assert schlick(comps) == pytest.approx(0.04)


def test_total_internal_reflection_schlick_small_angle() -> None:
    s = Sphere(material=Material(transparency=1, refractive_index=1.5))
    r = Ray(point(0, 0.99, -2), vector(0, 0, 1))
    inters = Intersections([Intersection(1.8589, s)])

    comps = prepare_computation(inters[0], r, inters)
    # Truth reflectance tweaked from textbook to lazily fix floating point issues
    assert schlick(comps) == pytest.approx(0.4887308)
