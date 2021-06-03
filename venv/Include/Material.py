from __future__ import annotations
import typing

from Include.Tuple import *
from Include.Light import PointLight

if typing.TYPE_CHECKING:
    from Include.Pattern import Pattern
    from Include.Shape import Shape

class Material:
    def __init__(self, color: Color = Color(1, 1, 1), ambient: float = 0.1, diffuse: float = 0.9, specular: float = 0.9,
                 shininess: float = 200.0, pattern: Pattern = None, reflective: float = 0.0, transparency: float = 0.0, refractive_index: float = 1.0):
        self.color = color                          # Color of the material
        self.ambient = ambient                      # Light reflected from other objects in the environment -> constant
        self.diffuse = diffuse                      # Light reflected from a dull and flat surface dependant on the angle between te light source and the surface normal
        self.specular = specular                    # Reflection of the light source itself on the surface
        self.shininess = shininess                  #
        self.pattern = pattern                      # Pattern of the material (optional)
        self.reflective = reflective                # 0.0 -> surface is nonreflective | 1.0 -> surface is a perfect mirror
        self.transparency = transparency            # 0.0 -> surface is opaque
        self.refractive_index = refractive_index    # A number to determine to which degree light will bend when entering or exiting a material

    def lighting(self, object: Shape, light: PointLight, point: Tuple, eyev: Tuple, normalv: Tuple, in_shadow: bool):
        # Determines color dependant on a existing pattern
        color = self.pattern.pattern_at_object(object, point) if self.pattern != None else self.color

        # Combine the surface color with the light source's color/intensity (the intensity is a field of type Color)
        effective_color = color * light.intensity

        # Find the direction vector to the light source
        lightv = (light.position - point).normalize()

        # Compute the ambient contribution
        ambient = effective_color * self.ambient

        # Represents the cosine of the angle between the light vector and the normal vector.
        # A negative number means the light is on the other side of the surface.
        light_dot_normal = lightv.dot(normalv)

        if (in_shadow != True):
            # If light_dot_normal is less then 0, light source is on the other side of the surface, thus making diffuse and specular black
            if light_dot_normal < 0:
                diffuse = Color(0, 0, 0)
                specular = Color(0, 0, 0)
            else:
                # Compute the diffuse contribution
                diffuse = effective_color * self.diffuse * light_dot_normal

                # Reflect_dot_eye represents the cosine of the angle between the light vector and the normal vector. A negative number means the light reflects away from the eye.
                reflectv = (-lightv).reflect(normalv)
                reflect_dot_eye = reflectv.dot(eyev)

                if reflect_dot_eye < 0:
                    specular = Color(0, 0, 0)
                else:
                    # Compute the specular contribution
                    factor = pow(reflect_dot_eye, self.shininess)
                    specular = light.intensity * self.specular * factor
        else:
            diffuse = Color(0, 0, 0)
            specular = Color(0, 0, 0)

            if light_dot_normal > 0:
                reflectv = (-lightv).reflect(normalv)
                reflect_dot_eye = reflectv.dot(eyev)

                if reflect_dot_eye > 0:
                    factor = pow(reflect_dot_eye, self.shininess)

        # Add the three contributions together to get the final result
        return ambient + diffuse + specular

    def __eq__(self, other):
        return self.color == other.color and self.ambient == other.ambient and self.diffuse == other.diffuse \
               and self.specular == other.specular and self.shininess == other.shininess and self.pattern == other.pattern and self.reflective == other.reflective