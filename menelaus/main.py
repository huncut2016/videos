from manim import *
import numpy as np


class Define(MovingCameraScene):
    def introduction(self):
        title = Text("The proof of Menelaus's theorem").center()
        mname = Text("András Zoller").scale(0.5).next_to(title, DOWN)

        self.play(Write(title))
        self.play(Write(mname))
        self.wait()
        self.play(FadeOut(VGroup(title, mname)))
        self.wait()

    def demonsrtation(self):
        triangle = (
            Polygon([5, -2, 0], [-2, 1.5, 0], [-3, -2, 0])
            .scale(0.8)
            .center()
            .shift(LEFT)
        )

        a_coord = triangle.get_boundary_point(LEFT)
        a = Dot(a_coord)
        a_label = Tex("A").next_to(a, DOWN)

        b_coord = triangle.get_boundary_point(RIGHT)
        b = Dot(b_coord)
        b_label = Tex("B").next_to(b, DOWN)

        c_coord = triangle.get_boundary_point(UP)
        c = Dot(c_coord)
        c_label = Tex("C").next_to(c, UP)

        outline_coord = (b_coord, b_coord + RIGHT * 5)
        # Mobject 55

        intersection_coord = (c_coord + DOWN, b_coord + RIGHT * 3)
        intersection = Line(*intersection_coord, color=RED).scale(2)

        r_coord = line_intersection(intersection_coord, (a_coord, c_coord))
        r = Dot(r_coord)
        r_label = Tex("R").next_to(r, DOWN + RIGHT)

        q_coord = line_intersection(intersection_coord, (c_coord, b_coord))
        q = Dot(q_coord)
        q_label = Tex("Q").next_to(q, UP)

        p_coord = line_intersection(intersection_coord, outline_coord)
        p = Dot(p_coord)
        p_label = Tex("P").next_to(p, UP)

        triangle_dots = VGroup(a, b, c)
        triangle_labels = VGroup(a_label, b_label, c_label)

        intersection_dots = VGroup(r, q, p)
        intersection_labels = VGroup(r_label, q_label, p_label)

        dots = VGroup(
            p,
            q,
            r,
            a,
            b,
            c,
        )

        ba = ab = Line(b_coord, a_coord).set_color(BLUE)
        ap = pb = Line(a_coord, p_coord).set_color(BLUE)
        bp = bp = DashedLine(b_coord, p_coord, dashed_ratio=0.45).set_color(BLUE)
        bq = qb = Line(b_coord, q_coord).set_color(BLUE)
        qc = cq = Line(q_coord, c_coord).set_color(BLUE)
        cr = rc = Line(c_coord, r_coord).set_color(BLUE)
        ra = ar = Line(r_coord, a_coord).set_color(BLUE)

        ac = ca = Line(a_coord, c_coord).set_color(BLUE)
        cb = bc = Line(c_coord, b_coord).set_color(BLUE)

        outline = VGroup(bp, DashedLine(p_coord, p_coord + RIGHT * 3, color=BLUE))

        tri = VGroup(ba, ac, cb)
        dot_labels = VGroup(a_label, b_label, c_label, r_label, q_label, p_label)

        self.play(Create(tri))

        for d, l in zip(triangle_dots, triangle_labels):
            self.play(FadeIn(d), Write(l))
        self.add_foreground_mobjects(triangle_dots)

        self.wait()
        self.play(Create(outline))

        self.play(Create(intersection))

        for d, l in zip(intersection_dots, intersection_labels):
            self.play(FadeIn(d), Write(l))
        self.add_foreground_mobjects(intersection_dots)

        menelaosz = MathTex(
            r"{AP",
            r"\over",
            r"BP}",
            r"\cdot",
            r"{BQ",
            r"\over",
            r"QC}",
            r"\cdot",
            r"{CR",
            r"\over",
            r"RA}",
            r"= 1",
        ).move_to(UR * 3)

        for index, line in zip(range(0, 12, 2), VGroup(ap, bp, bq, qc, cr, ra)):
            text = menelaosz[index]
            if line == ap:
                line.set_color(YELLOW)
                self.play(FadeToColor(ab, color=YELLOW), FadeToColor(bp, color=YELLOW))
                self.play(ReplacementTransform(line, menelaosz[index], run_time=1.5))
            elif line != bp:
                self.play(FadeToColor(line, color=YELLOW), run_time=0.5)
                self.play(TransformFromCopy(line, menelaosz[index], run_time=1.5))
            else:
                self.play(TransformFromCopy(line, menelaosz[index], run_time=1.5))
            self.play(Write(menelaosz[index + 1]), run_time=0.5)
        self.wait(2)

        perp_coord = (b_coord, b_coord + slope(a_coord, c_coord))
        perp = Line(*perp_coord).scale(3)
        bd = bd = perp

        d = Dot(line_intersection(intersection_coord, perp_coord))
        d_label = Tex("D").next_to(d, UP).shift(UP * 0.2)
        dots.add(d)
        dot_labels.add(d_label)

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.move_to(d.get_center() + DL * 0.25).set(
                width=perp.width * 8
            ),
        )

        self.play(
            Create(perp),
            Create(d),
            Write(d_label),
        )
        self.add_foreground_mobjects(d)
        self.wait()

        self.play(Restore(self.camera.frame))

        self.wait()

        tri.remove(ab)
        self.remove(tri)
        tri = VGroup(ar, rc, cq, qb, ab, bp)
        base_scene = VGroup(dots, dot_labels, outline, intersection, perp, tri)
        first_scene_boundingbox = SurroundingRectangle(base_scene, color=WHITE)

        self.play(
            FadeOut(menelaosz),
            VGroup(first_scene_boundingbox, base_scene)
            .animate.scale(0.5)
            .move_to(UP * 2.5),
        )
        self.play(
            FadeToColor(tri, color=BLUE),
        )

        self.wait()

        perpeq = (
            MathTex("BD", "||", "AC", color=PINK)
            .next_to(first_scene_boundingbox, DOWN)
            .shift(DOWN)
        )
        helper = VGroup(ar, rc, bd)
        self.play(
            FadeToColor(helper[2], color=PINK),
        )
        self.play(
            TransformFromCopy(helper[2], perpeq[0]),
        )
        self.wait()

        self.play(Write(perpeq[1]))

        self.play(FadeToColor(helper[:2], color=PINK))
        self.play(
            TransformFromCopy(helper[:2], perpeq[2]),
        )

        self.play(perpeq.animate.to_edge(LEFT))

        self.wait()

        qdb = (
            Polygon(b.get_center(), d.get_center(), q.get_center())
            .set_fill(YELLOW, opacity=0.5)
            .set_stroke(width=0)
        )

        rcq = (
            Polygon(c.get_center(), q.get_center(), r.get_center())
            .set_fill(YELLOW, opacity=0.5)
            .set_stroke(width=0)
        )

        self.play(FadeIn(qdb))
        self.wait()

        qdb_sim_rcq = (
            MathTex(
                r"QDB",
                r"\sim",
                r"QCR",
            )
            .next_to(first_scene_boundingbox, DOWN)
            .shift(DOWN)
            .set_color(YELLOW)
        )

        self.play(TransformFromCopy(qdb, qdb_sim_rcq[0]))
        self.wait()
        self.play(Write(qdb_sim_rcq[1]))
        self.wait()

        self.play(FadeIn(rcq))
        self.wait()
        self.play(TransformFromCopy(rcq, qdb_sim_rcq[2]))
        self.wait()

        self.play(qdb_sim_rcq.animate.to_edge(RIGHT))
        self.wait()

        pdb = (
            Polygon(p.get_center(), b.get_center(), d.get_center())
            .set_fill(WHITE, opacity=1)
            .set_stroke(width=0)
        )

        pra = (
            Polygon(p.get_center(), r.get_center(), a.get_center())
            .set_fill(WHITE, opacity=0.5)
            .set_stroke(width=0)
        )

        pra_sim_pdb = (
            MathTex("PRA", r"\sim", "PDB")
            .next_to(first_scene_boundingbox, DOWN)
            .shift(DOWN)
            .set_color(WHITE)
        )

        self.play(FadeIn(pra))
        self.wait()
        self.play(TransformFromCopy(pra, pra_sim_pdb[0]))

        self.wait()
        self.play(Write(pra_sim_pdb[1]))

        self.play(FadeIn(pdb))
        self.wait()
        self.play(TransformFromCopy(pdb, pra_sim_pdb[2]))
        self.play(FadeOut(perpeq, shift=LEFT), pra_sim_pdb.animate.to_edge(LEFT))

        lemmas = VGroup(pra_sim_pdb, qdb_sim_rcq)

        self.play(lemmas.animate.shift(UP))
        self.wait()

        borderline = Underline(lemmas)
        self.play(Create(borderline))
        self.wait()

        e1 = (
            MathTex(r"{AP \over BP} = {AR \over DB}")
            .set_color(WHITE)
            .next_to(borderline, DOWN)
            .shift(DOWN)
        )
        e2 = (
            MathTex(r"{BQ \over QC} = {DB \over CR}")
            .set_color(YELLOW)
            .next_to(borderline, DOWN)
            .shift(DOWN)
        )

        self.play(Write(e1))
        self.wait()
        self.play(e1.animate.to_edge(LEFT))

        self.play(Write(e2))
        self.wait()
        self.play(e2.animate.to_edge(RIGHT))

        self.wait()

        e1_times_e2 = (
            MathTex(
                "{",
                "AP",
                r"\over",
                "BP",
                "}",
                r"\cdot",
                "{",  # 6
                "BQ",
                r"\over",
                "QC",
                "}",  # 10
                "=",
                "{",
                "AR",
                r"\over",
                "DB",
                "}",
                r"\cdot",
                "{",  # 18
                "DB",
                r"\over",
                "CR",
                "}",
            )
            .next_to(borderline, DOWN)
            .shift(DOWN)
        )

        e1_times_e2[6:11].set_color(YELLOW)
        e1_times_e2[18:].set_color(YELLOW)

        self.play(TransformFromCopy(e1, VGroup(e1_times_e2[0:5], e1_times_e2[12:17])))
        self.wait()

        self.play(Write(VGroup(e1_times_e2[5], e1_times_e2[11], e1_times_e2[17])))
        self.play(TransformFromCopy(e2, VGroup(e1_times_e2[6:11], e1_times_e2[18:])))
        self.wait(2)

        c1 = Cross(e1_times_e2[19])
        c2 = Cross(e1_times_e2[15])
        self.play(Create(VGroup(c1, c2)))
        self.wait()

        e3 = (
            MathTex(
                "{",
                "AP",
                r"\over",
                "BP",
                "}",
                r"\cdot",
                "{",  # 6
                "BQ",
                r"\over",
                "QC",
                "}",  # 10
                "=",
                "{",
                "AR",
                r"\over",
                "CR",
                "}",
            )
            .next_to(borderline, DOWN)
            .shift(DOWN)
        )

        e3[6:11].set_color(YELLOW)
        e3[15].set_color(YELLOW)

        self.play(TransformMatchingTex(e1_times_e2, e3), FadeOut(VGroup(c1, c2)))
        self.wait(1.5)

        e4 = (
            MathTex(
                "{",
                "AP",
                r"\over",
                "BP",
                "}",
                r"\cdot",
                "{",  # 6
                "BQ",
                r"\over",
                "QC",
                "}",  # 10
                r"\cdot" "{",
                "CR",
                r"\over",
                "AR",
                "}",
                "=",
                "1",
            )
            .next_to(borderline, DOWN)
            .shift(DOWN)
        )
        e4[7:11].set_color(YELLOW)
        e4[12].set_color(YELLOW)

        self.play(TransformMatchingTex(e3, e4))
        self.wait()
        self.play(Create(SurroundingRectangle(e4)))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()

    def ending(self):
        t = Tex("Thanks for watching!")
        self.play(Write(t))
        self.play(FocusOn(t))
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def construct(self):
        self.introduction()
        self.demonsrtation()
        self.ending()


def slope(p1, p2):
    vector = p2 - p1
    return vector / np.linalg.norm(vector)


class Index(Scene):
    def construct(self):
        triangle = (
            Polygon([5, -2, 0], [-2, 1.5, 0], [-3, -2, 0])
            .scale(0.8)
            .center()
            .shift(LEFT)
        )

        a_coord = triangle.get_boundary_point(LEFT)
        a = Dot(a_coord)
        a_label = Tex("A").next_to(a, DOWN)

        b_coord = triangle.get_boundary_point(RIGHT)
        b = Dot(b_coord)
        b_label = Tex("B").next_to(b, DOWN)

        c_coord = triangle.get_boundary_point(UP)
        c = Dot(c_coord)
        c_label = Tex("C").next_to(c, UP)

        outline_coord = (b_coord, b_coord + RIGHT * 5)
        # Mobject 55

        intersection_coord = (c_coord + DOWN, b_coord + RIGHT * 3)
        intersection = Line(*intersection_coord, color=RED).scale(2)

        r_coord = line_intersection(intersection_coord, (a_coord, c_coord))
        r = Dot(r_coord)
        r_label = Tex("R").next_to(r, DOWN + RIGHT)

        q_coord = line_intersection(intersection_coord, (c_coord, b_coord))
        q = Dot(q_coord)
        q_label = Tex("Q").next_to(q, UP)

        p_coord = line_intersection(intersection_coord, outline_coord)
        p = Dot(p_coord)
        p_label = Tex("P").next_to(p, UP)

        triangle_dots = VGroup(a, b, c)
        triangle_labels = VGroup(a_label, b_label, c_label)

        intersection_dots = VGroup(r, q, p)
        intersection_labels = VGroup(r_label, q_label, p_label)

        dots = VGroup(
            p,
            q,
            r,
            a,
            b,
            c,
        )

        ba = ab = Line(b_coord, a_coord).set_color(BLUE)
        ap = pb = Line(a_coord, p_coord).set_color(BLUE)
        bp = bp = DashedLine(b_coord, p_coord, dashed_ratio=0.45).set_color(BLUE)
        bq = qb = Line(b_coord, q_coord).set_color(BLUE)
        qc = cq = Line(q_coord, c_coord).set_color(BLUE)
        cr = rc = Line(c_coord, r_coord).set_color(BLUE)
        ra = ar = Line(r_coord, a_coord).set_color(BLUE)

        ac = ca = Line(a_coord, c_coord).set_color(BLUE)
        cb = bc = Line(c_coord, b_coord).set_color(BLUE)

        outline = VGroup(bp, DashedLine(p_coord, p_coord + RIGHT * 3, color=BLUE))

        tri = VGroup(ba, ac, cb)
        dot_labels = VGroup(a_label, b_label, c_label, r_label, q_label, p_label)

        self.add(tri)

        for d, l in zip(triangle_dots, triangle_labels):
            self.add(d, l)
        self.add_foreground_mobjects(triangle_dots)

        self.add(outline)
        self.add(intersection)

        for d, l in zip(intersection_dots, intersection_labels):
            self.add(d, l)
        self.add_foreground_mobjects(intersection_dots)

        base_scene = VGroup(dots, dot_labels, outline, intersection, tri)
        first_scene_boundingbox = SurroundingRectangle(base_scene, color=WHITE)

        self.add(first_scene_boundingbox)

        VGroup(base_scene, first_scene_boundingbox).scale(0.5).center().shift(UP * 0.5)

        menelaosz = (
            MathTex(
                r"{AP",
                r"\over",
                r"BP}",
                r"\cdot",
                r"{BQ",
                r"\over",
                r"QC}",
                r"\cdot",
                r"{CR",
                r"\over",
                r"RA}",
                r"= 1",
            )
            .center()
            .shift(DOWN * 2)
        )
        self.add(menelaosz)

        t = Tex("The proof of Menelaus's theorem").to_edge(UP)
        self.add(t, Underline(t))
