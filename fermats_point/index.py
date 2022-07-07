from manim import *


class Index(Scene):
    def construct(self):
        triangle = (
            Polygon([5, -2, 0], [-1, 4, 0], [-3, -2, 0])
            .scale(0.5)
            .center()
            .shift(1.6 * UP)
        )

        p_coord = triangle.get_center()
        p = Dot(p_coord, color=RED)
        p_label = Tex("P").next_to(p, DOWN).set_color(RED)

        a_coord = triangle.get_boundary_point(LEFT)
        a = Dot(a_coord)
        a_label = Tex("A").next_to(a, DOWN)

        b_coord = triangle.get_boundary_point(RIGHT)
        b = Dot(b_coord)
        b_label = Tex("B").next_to(b, DOWN)

        c_coord = triangle.get_boundary_point(UP)
        c = Dot(c_coord)
        c_label = Tex("C").next_to(c, UP)

        ap = pa = DashedLine(a_coord, p_coord)
        bp = pb = DashedLine(b_coord, p_coord)
        cp = pc = DashedLine(c_coord, p_coord)

        dots = VGroup(a, b, c, p)
        d_labels = VGroup(a_label, b_label, c_label, p_label)
        lines = VGroup(ap, bp, cp)

        g = VGroup(triangle, dots, d_labels, lines)
        surr = SurroundingRectangle(g, color=WHITE)

        t = (
            MathTex(r"AP + BP + CP = min", substrings_to_isolate="P")
            .next_to(surr, DOWN)
            .shift(DOWN)
        )
        t.set_color_by_tex("P", RED)

        self.add(g, t)
        self.add_foreground_mobject(p)
