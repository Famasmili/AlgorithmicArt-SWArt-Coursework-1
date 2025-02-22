Algorithmic Art: Attractors
This repository contains Python scripts that generate art pieces inspired by the Attractor algorithm.
Attractors are chaotic dynamical systems with stable states towards which the system tends to gravitate.
Among them, there are fixed attractors, whose state is a specific point, e.g., a pendulum, or strange or dynamic ones, whose stable state can be a whole set of points.
Most attractors can exhibit fractal behavior as well.
In our work, we implement four attractors: Clifford, De Jong, Lorentz and Aizawa attractors. The first two are discrete ones, while the last two are continuous.
Each attractor is defined by a system of equations that computes the change in coordinate values of each point over time.
They all have important parameters that control the output and the stable state observed. Small changes in these result in varying results overall.

Contents
Final Piece: Attractors_Art_animated.py

Running the Code
To run the code:

Ensure you have Python installed on your machine.
Install the necessary libraries (PyQt5, vispy, numpy, colorsys, random).
Open and run the code files using your favorite IDE.

Inspiration
For more inspiration, check out:

Important Libraries:
https://vispy.org/getting_started/index.html
https://github-wiki-see.page/m/vispy/vispy/wiki/Tech.-Visuals-and-scene-graph
https://www.pythonguis.com/pyqt5/

Art related - Algorithms:
https://blbadger.github.io/clifford-attractor.html
https://www.fxhash.xyz/generative/slug/attractors-and-circles
https://www.algosome.com/articles/strange-attractors-de-jong.html
https://www.algosome.com/articles/aizawa-attractor-chaos.html
https://en.wikipedia.org/wiki/Lorenz_system
https://www.mathforengineers.com/multivariable-calculus/Runge-Kutta-method-interactive-calculator.html