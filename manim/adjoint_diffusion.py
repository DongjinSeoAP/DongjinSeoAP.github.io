"""
Manim scenes for the blog post:
  "Designing Photonic Devices with Diffusion Models + Physics: AdjointDiffusion"

Render (uses the homebrew python3.11 manim, 0.18):
  manim -qm --format mp4 manim/adjoint_diffusion.py ReverseDiffusion AdjointGuidance MethodComparison

Three scenes:
  1. ReverseDiffusion   - noise condenses into a fabricable photonic structure
  2. AdjointGuidance    - the physics (adjoint) gradient steers each denoising step
  3. MethodComparison   - plain gradient ascent vs. AdjointDiffusion
"""

import numpy as np
from manim import *

# ---- palette (matches the site theme) -------------------------------------
BG       = ManimColor("#f7fafc")   # page-ish light background
SILICON  = ManimColor("#043361")   # high-index material (silicon)
AIR      = ManimColor("#eaf4fb")   # low-index material (air / SiO2)
ACCENT   = ManimColor("#3eb7f0")   # light blue accent
LIGHT    = ManimColor("#f4a23b")   # the "light" travelling through the device
INK      = ManimColor("#1b2733")   # text

config.background_color = BG

N = 24  # grid resolution


def target_device():
    """A hand-drawn 'wavelength splitter': one input port on the left that
    routes light into two output ports on the right through a freeform region."""
    g = np.zeros((N, N))
    # input waveguide (left, centred)
    g[10:14, 0:8] = 1
    # top output port (right)
    g[3:7, 16:N] = 1
    # bottom output port (right)
    g[17:21, 16:N] = 1
    # freeform coupling region in the middle
    g[7:17, 7:17] = 1
    # a couple of air holes that a real optimiser would carve out
    g[11:13, 10:12] = 0
    g[8:10, 13:15] = 0
    g[14:16, 13:15] = 0
    return g


def make_grid():
    """A VGroup of N*N unit squares, arranged in a grid, index = r*N + c."""
    sq = VGroup(*[
        Square(side_length=1.0, stroke_width=0).set_fill(AIR, 1.0)
        for _ in range(N * N)
    ])
    sq.arrange_in_grid(rows=N, cols=N, buff=0)
    sq.set(width=5.6)  # scale whole grid to a sensible size
    return sq


def paint(grid, values):
    """Colour every cell by its value in [0,1]: 0 = air, 1 = silicon."""
    for k, cell in enumerate(grid):
        r, c = divmod(k, N)
        v = float(np.clip(values[r, c], 0, 1))
        cell.set_fill(interpolate_color(AIR, SILICON, v), 1.0)


class ReverseDiffusion(Scene):
    def construct(self):
        target = target_device()
        rng = np.random.default_rng(7)
        noise = rng.random((N, N))

        grid = make_grid().shift(LEFT * 0.6)
        paint(grid, noise)
        self.add(grid)

        title = Text("Reverse diffusion: noise → structure",
                     color=INK, font_size=30).to_edge(UP, buff=0.45)
        self.add(title)

        # progress label on the right
        cap = Text("pure noise", color=ACCENT, font_size=26)
        cap.next_to(grid, RIGHT, buff=0.7)
        self.add(cap)

        t = ValueTracker(0.0)

        def updater(g):
            tv = t.get_value()
            # decreasing-noise denoising look + slight sharpening near the end
            field = tv * target + (1 - tv) * noise
            if tv > 0.6:
                k = (tv - 0.6) / 0.4
                field = (1 - k) * field + k * np.where(target > 0.5, 1.0, 0.0)
            paint(g, field)

        grid.add_updater(updater)

        self.play(t.animate.set_value(0.55), run_time=2.4, rate_func=linear)
        new_cap = Text("denoising…", color=ACCENT, font_size=26).move_to(cap)
        self.play(Transform(cap, new_cap), run_time=0.3)
        self.play(t.animate.set_value(1.0), run_time=2.4, rate_func=smooth)
        grid.remove_updater(updater)

        done = Text("fabricable device", color=SILICON, font_size=26).move_to(cap)
        self.play(Transform(cap, done), run_time=0.4)
        self.wait(1.4)


class AdjointGuidance(Scene):
    def construct(self):
        target = target_device()
        grid = make_grid().shift(LEFT * 2.6)
        paint(grid, target)
        self.add(grid)

        title = Text("Each denoising step is nudged by the physics gradient",
                     color=INK, font_size=27).to_edge(UP, buff=0.4)
        self.add(title)

        # light flowing in from the left, out to two ports on the right
        left_edge = grid.get_left()
        in_y = grid.get_center()[1]
        src = Dot(color=LIGHT).move_to([left_edge[0] - 0.8, in_y, 0])
        in_arrow = Arrow(src.get_center(), [left_edge[0] + 0.1, in_y, 0],
                         color=LIGHT, buff=0, stroke_width=6)
        in_lbl = Text("light in", color=LIGHT, font_size=22).next_to(in_arrow, UP, buff=0.15)
        self.play(GrowArrow(in_arrow), FadeIn(in_lbl), run_time=0.6)

        right_edge = grid.get_right()
        top_y = right_edge[1] + 1.6
        bot_y = right_edge[1] - 1.6
        out_top = Arrow([right_edge[0] - 0.1, top_y, 0], [right_edge[0] + 1.0, top_y, 0],
                        color=LIGHT, buff=0, stroke_width=4)
        out_bot = Arrow([right_edge[0] - 0.1, bot_y, 0], [right_edge[0] + 1.0, bot_y, 0],
                        color=LIGHT, buff=0, stroke_width=4)
        self.play(GrowArrow(out_top), GrowArrow(out_bot), run_time=0.5)

        # figure-of-merit bar
        bar_bg = Rectangle(width=0.5, height=3.2, stroke_color=INK, stroke_width=2,
                           fill_opacity=0).to_edge(RIGHT, buff=0.9)
        fom = ValueTracker(0.32)
        fom_fill = always_redraw(lambda: Rectangle(
            width=0.5, height=3.2 * fom.get_value(),
            stroke_width=0, fill_color=ACCENT, fill_opacity=1
        ).align_to(bar_bg, DOWN).move_to(bar_bg, aligned_edge=DOWN))
        fom_lbl = Text("efficiency", color=INK, font_size=22).next_to(bar_bg, UP, buff=0.2)
        self.add(bar_bg, fom_fill, fom_lbl)

        # three guidance steps: gradient arrows flash, structure refines, FOM rises
        rng = np.random.default_rng(3)
        boundary = [k for k in range(N * N)
                    if 6 <= divmod(k, N)[0] < 18 and 6 <= divmod(k, N)[1] < 18]
        for step, target_fom in enumerate([0.55, 0.74, 0.9]):
            picks = rng.choice(boundary, size=10, replace=False)
            arrows = VGroup()
            for k in picks:
                cell = grid[k]
                a = Arrow(cell.get_center(), cell.get_center() + UP * 0.45 + RIGHT * 0.12,
                          color=LIGHT, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.4)
                arrows.add(a)
            step_lbl = Text(f"adjoint gradient  ∇ FoM   (step {step+1})",
                            color=LIGHT, font_size=22).next_to(grid, DOWN, buff=0.35)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05),
                      FadeIn(step_lbl), run_time=0.7)
            # a few cells "flip" toward the optimum + FOM climbs
            flips = rng.choice(boundary, size=6, replace=False)
            anims = [grid[k].animate.set_fill(SILICON, 1.0) for k in flips]
            self.play(*anims, fom.animate.set_value(target_fom),
                      FadeOut(arrows), run_time=0.8)
            self.play(FadeOut(step_lbl), run_time=0.2)

        result = Text("high-performance & fabricable", color=SILICON, font_size=24)
        result.next_to(grid, DOWN, buff=0.35)
        self.play(Write(result), run_time=0.6)
        self.wait(1.4)


class MethodComparison(Scene):
    def construct(self):
        title = Text("Plain gradient ascent vs. AdjointDiffusion",
                     color=INK, font_size=30).to_edge(UP, buff=0.45)
        self.add(title)

        ax = Axes(
            x_range=[0, 100, 25], y_range=[0, 1, 0.25],
            x_length=7.2, y_length=4.2,
            axis_config={"color": INK, "stroke_width": 2,
                         "include_ticks": True, "font_size": 20},
            tips=False,
        ).shift(LEFT * 1.6 + DOWN * 0.3)
        x_lbl = Text("optimization steps", color=INK, font_size=22).next_to(ax, DOWN, buff=0.3)
        y_lbl = Text("efficiency", color=INK, font_size=22).rotate(PI / 2).next_to(ax, LEFT, buff=0.3)
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)

        # gradient ascent: rises then plateaus low, slightly jagged
        def ga(x):
            base = 0.58 * (1 - np.exp(-x / 12))
            return base + 0.02 * np.sin(x / 2.5) * np.exp(-x / 60)
        # adjoint diffusion: climbs higher and keeps improving
        def ad(x):
            return 0.9 * (1 - np.exp(-x / 22))

        ga_curve = ax.plot(ga, x_range=[0, 100], color=ManimColor("#9aa7b3"), stroke_width=5)
        ad_curve = ax.plot(ad, x_range=[0, 100], color=ACCENT, stroke_width=5)

        ga_tag = Text("gradient ascent", color=ManimColor("#7d8a96"), font_size=22)
        ga_tag.next_to(ax.c2p(100, ga(100)), RIGHT, buff=0.15)
        ad_tag = Text("AdjointDiffusion", color=ACCENT, font_size=22)
        ad_tag.next_to(ax.c2p(100, ad(100)), RIGHT, buff=0.15)

        self.play(Create(ga_curve), run_time=1.6)
        self.play(FadeIn(ga_tag), run_time=0.3)
        self.play(Create(ad_curve), run_time=1.8)
        self.play(FadeIn(ad_tag), run_time=0.3)

        gap = DoubleArrow(ax.c2p(100, ga(100)), ax.c2p(100, ad(100)),
                          color=LIGHT, buff=0.05, stroke_width=3,
                          max_tip_length_to_length_ratio=0.15)
        gap_lbl = Text("+ better optima", color=LIGHT, font_size=20).next_to(gap, RIGHT, buff=0.1)
        self.play(GrowFromCenter(gap), FadeIn(gap_lbl), run_time=0.6)
        self.wait(1.6)
