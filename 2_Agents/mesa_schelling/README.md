# Schelling Segregation Model

## Summary

The Schelling segregation model is a classic agent-based model, demonstrating how even a mild preference for similar neighbors can lead to a much higher degree of segregation than we would intuitively expect. The model consists of agents on a square grid, where each grid cell can contain at most one agent. Agents come in two colors: red and blue. They are happy if a certain share of their eight possible neighbors are of the same color, and unhappy otherwise. Unhappy agents will pick a random empty cell to move to each step, until they are happy. The model keeps running until there are no unhappy agents.

Even in runs where the agents would be perfectly happy with a majority of their neighbors being of a different color (e.g. a Blue agent would be happy with five Red neighbors and three Blue ones), the model consistently leads to a high degree of segregation, with most agents ending up with no neighbors of a different color.

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```
## Your Task

You will note that the agent file in this directory is full of blanks, and if you compile the model as is, it willnot work. Your task is to fix it! The comments in the code describe what you should try to do in filling blanks, and each blank represents a bit of code in my complete version (i.e. you can do this successfully with the number of lines in the current file). That said, feel free to be creative in your implementations; there is always more than one way to do it!

## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``run.py``: Launches a model visualization server.
* ``run_ascii.py``: Run the model in text mode.
* ``schelling.py``: Contains the agent class, and the overall model class.
* ``server.py``: Defines classes for visualizing the model in the browser via Mesa's modular server, and instantiates a visualization server.
* ``analysis.ipynb``: Notebook demonstrating how to run experiments and parameter sweeps on the model.

## Further Reading

Schelling's original paper describing the model:

[Schelling, Thomas C. Dynamic Models of Segregation. Journal of Mathematical Sociology. 1971, Vol. 1, pp 143-186.](https://www.stat.berkeley.edu/~aldous/157/Papers/Schelling_Seg_Models.pdf)

An interactive, browser-based explanation and implementation:

[Parable of the Polygons](http://ncase.me/polygons/), by Vi Hart and Nicky Case.
