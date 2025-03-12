*Code adapted from Mesa Examples project*

# Flockers

An implementation of Craig Reynolds's Boids flocker model. Agents (simulated birds) try to fly towards the average position of their neighbors and in the same direction as them, while maintaining a minimum distance. This produces flocking behavior. In each round, agents calculate three vectors: coherence (moving towards neighbors), separation (moving away from neighbors that are too close), and matching (moving parallel to neighbors), each of which is weighted by an associated factor. From this simple decision rule, agents produce realistic-looking flocks of birds.

Unfortunately, I made some mistakes in the code here, so you will have to fix them.

## Your Task

When you try to launch the app, it's going to produce an error. Please help fix it! Once you fix the error and get the model running successfully, see how it looks. Are the birds flocking? Once the model is totally debugged, if you have extra time, try putting sliders for the three vector weighting factors in the app.py file.

## How to Run

BE SURE TO INSTALL REQUIREMENTS FIRST! If you don't see the visualization, check that you have the requirements installed in your virtual environment!
```
    pip install -r requirements.txt
```

Launch the model (note that this will produce an error, as described above):
```
    solara run app.py
```

## Files

* ``agents.py``: Contains the agent class
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.

## Further Reading
* See [NetLogo version of model here]. (https://ccl.northwestern.edu/netlogo/models/Flocking) 
  
