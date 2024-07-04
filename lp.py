import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline

def plot_bspline(control_points, k, knots, num_points=100):
    # Create a B-spline object
    spl = BSpline(knots, control_points, k)

    # Generate a fine grid of t values for smooth plotting
    t = np.linspace(knots[k], knots[-k-1], num_points)
    curve = spl(t)

    # Plot the B-spline curve
    plt.plot(curve[:, 0], curve[:, 1], label='B-Spline Curve')

    # Plot the control points
    plt.plot(control_points[:, 0], control_points[:, 1], 'o--', label='Control Points')

    # Plot the knot vector positions on the x-axis
    for kv in knots[k:-k]:
        plt.axvline(x=kv, color='r', linestyle='--', label='Knot Vector' if kv == knots[k] else "")

    plt.title('B-Spline Curve with Control Points and Knot Vectors')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example control points for an explanation
control_points = np.array([
    [0.0, 0.0],
    [0.2, 0.4],
    [0.4, 0.1],
    [0.6, 0.5],
    [0.8, 0.3],
    [1.0, 0.6]
])

# Degree of the B-spline (cubic in this case)
k = 3

# Number of control points
n = len(control_points) - 1

# Knot vector (uniform in this example)
knots = np.concatenate(([0] * k, np.arange(n - k + 2), [n - k + 1] * k))

# Plot the B-spline with explanations
plot_bspline(control_points, k, knots)
