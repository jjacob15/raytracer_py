from dataclasses import dataclass, field
from raytracer.color import Color, WHITE
from raytracer.patterns import Pattern
from raytracer import NUMERIC_T


@dataclass(slots=True, frozen=True)
class Material:
    color: Color = WHITE
    pattern: Pattern | None = None
    ambient: NUMERIC_T = 0.1
    diffuse: NUMERIC_T = 0.9
    specular: NUMERIC_T = 0.9
    shininess: NUMERIC_T = 200
    reflective: NUMERIC_T = 0
    transparency: NUMERIC_T = 0
    refractive_index: NUMERIC_T = 1

    def __post_init__(self) -> None:
        if any((val < 0 for val in (
            self.ambient,
            self.diffuse,
            self.specular,
            self.shininess,
            self.reflective,
            self.transparency,
            self.refractive_index,
        ))):
            raise ValueError("reflection and refraction attributes must be non-negatives")
