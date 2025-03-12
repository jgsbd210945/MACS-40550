*Code adapted from Mesa Examples project*

# Demographic Prisoner's Dilemma

This directory contains an implementation of Epstein's (1998) model of agents playing an imitative Prisoner's Dilemma (PD) on a grid. In the model, agents begin with a randomized strategy in a modified PD game (note that varying the payoff structure can change outcomes significantly). They determine payoffs by looking at their eight neighbors and deriving results based on their strategies in a given round. They then see who their neighbor with the highest payoff is (including themselves) and imitate that agent. The results generally show that cooperation can spread across a grid over time.

However, as you will see, this result depends on the order in which agents act! Here, you will explore the effects of activation regimes on model outcomes and brainstorm reasons why this might be the case. I will circulate a paper explaining it at the end of class.

## Your task

Using the model GUI in the code here, try to figure out what the relationship between activation regime and outcomes are. Try a variety different seeds, and remember ones that produce striking outcomes. If you want to get a bit ahead, feel free to try running batch experiments (we'll get to that formally later in the course). Once you have a guess about why the activation regimes have these effects, try to form a guess about why they do so. We'll discuss ideas at the end of class.

## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.
