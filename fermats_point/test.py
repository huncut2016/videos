from manim import *


class Test(Scene):
    def construct(self):
        t = Tex(r"$A$, $B$ and $C'$ are fixed")

        self.play(Create(t))
        self.wait()
