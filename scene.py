from manim import *
import random
from random import seed, uniform
import colorama
from collections import deque
import math

class GraphExample(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8))
        axes.add_coordinates()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        # Axes.get_graph will return the graph of a function
        sin_graph = axes.plot(
            lambda x: 2 * math.sin(x),
        )
        # By default, it draws it so as to somewhat smoothly interpolate
        # between sampled points (x, f(x)).  If the graph is meant to have
        # a corner, though, you can set use_smoothing to False
        relu_graph = axes.plot(
            lambda x: max(x, 0),
            use_smoothing=False,
        )
        # For discontinuous functions, you can specify the point of
        # discontinuity so that it does not try to draw over the gap.
        step_graph = axes.plot(
            lambda x: 2.0 if x > 3 else 1.0,
            discontinuities=[3],
        )

        # Axes.get_graph_label takes in either a string or a mobject.
        # If it's a string, it treats it as a LaTeX expression.  By default
        # it places the label next to the graph near the right side, and
        # has it match the color of the graph
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("ReLU"))
        step_label = axes.get_graph_label(step_graph, Text("Step"))

        self.play(
            Create(sin_graph),
            FadeIn(sin_label, shift=RIGHT),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(sin_graph, relu_graph),
            FadeTransform(sin_label, relu_label),
        )
        self.wait()
        self.play(
            ReplacementTransform(relu_graph, step_graph),
            FadeTransform(relu_label, step_label),
        )
        self.wait()

        parabola = axes.plot(lambda x: 0.25 * x**2)
        parabola.set_stroke(BLUE)
        self.play(
            FadeOut(step_graph),
            FadeOut(step_label),
            Create(parabola)
        )
        self.wait()

        # You can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(2, parabola))
        self.play(FadeIn(dot, scale=0.5))

        # A value tracker lets us animate a parameter, usually
        # with the intent of having other mobjects update based
        # on the parameter
        x_tracker = ValueTracker(2)
        f_always(
            dot.move_to,
            lambda: axes.i2gp(x_tracker.get_value(), parabola)
        )

        self.play(x_tracker.animate.set_value(4), run_time=3)
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.wait()

class NewtonExample(Scene):
    def func_f(x):
        return 0.25 * x**2

    def construct(self):
        axes = Axes((-3, 10), (-1, 8))
        axes.add_coordinates()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        parabola = axes.plot(lambda x: 0.25 * x**2)
        parabola.set_stroke(BLUE)
        self.play(
            Create(parabola)
        )
        self.wait()

        # You can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(2, parabola))
        self.play(FadeIn(dot, scale=0.5))

        # A value tracker lets us animate a parameter, usually
        # with the intent of having other mobjects update based
        # on the parameter
        x0 = 2
        eps=1e-5
        error=1e-5
        max_loop=10

        x_tracker = ValueTracker(x0)
        f_always(
            dot.move_to,
            lambda: axes.i2gp(x_tracker.get_value(), parabola)
        )
        num_calc = 0

        while True:
            func_df = (NewtonExample.func_f(x0+ eps) - NewtonExample.func_f(x0- eps))/(2*eps)
            if abs(func_df) <= eps:
                quit()

            x1 = x0 - NewtonExample.func_f(x0)/func_df
            num_calc += 1

            if(abs(x1-x0)<=error or max_loop<=num_calc):
                break
            self.play(x_tracker.animate.set_value(x1), run_time=3)
            x0 = x1

        self.wait()
