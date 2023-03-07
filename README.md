# Minecraft Stronghold Finder
Short python script, calculating the position of a minecraft stronghold (the end portal) from the trajectory direction of two ender-eye throws.
_(General Note: The code is rather old, and was not refurbished, so the code quality might be a bit meh.)_

Even though the calculation in code was more difficult than expected, the concept itself is incredibly simple. If one imagines the minecraft world seen from above, every endereye always points to the same point. If one captures two such vectors, the point of intersection can be calculated. This is where the stronghold is located.



## How to use
The script is a simple python 3 file. Inputs and outputs are given through the python terminal in a text-based format. The exact steps will be explained by the script, but the rough workflow is as follows:

- Throw an endereye from two positions
- For each throw, lock your crosshair on the floating position of the endereye (best **not** to be in F3-mode)
- Leave your crosshair in this exact location, open the F3-menu and check the horizonal angle you are looking at
- Give your current location (x and z coordinate) and said horizonal angle to the script


## Precision
The precision of the evaluated tests is decent. Most often the difference between the expected and actual intersection point was somewhere between 5-20 blocks.  The precision is highly dependent on the input, so following things should be considered for good results: 
- the crosshair should be placed precisely in the middle of the floating endereye
- the two throwing-locations should not be too close (50 blocks most often was okay, 100+ is better)
- **VERY IMPORTANT:** The vector between the two locations should at best be orthogonal to the flying-direction of the endereyes. In other words: when the first throw was executed, one should run to the left or right (when facing the thrown endereye), but **NOT** in the direction where the endereye flew   
