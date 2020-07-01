# ViralDiffusionVisualizationTool
This tool uses quantum computing to create a visualization of viral diffusion, building on a concept discussed in this paper (https://onlinelibrary.wiley.com/doi/full/10.1002/que2.29). Each Qubit in the visualization corresponds to a population with a chance of being infected and is represented by a circle with its infection probability represented by its shade of red. As the infection probability increases in a Qubit, its corresponding node darkens. With more time, we would also allow for the implementation of social distancing and mask wearing which would help decrease the spread of the virus.

The python code makes use of IBM's qiskit package, as well as matplotlib, xlrd, and xlwt. The user should make sure access to these packages are available before running the code.

To run the code, navigate to the directory where all 3 files (run.py, simulation.py, visualization.py) are located using the command shell.

With a population size of `n`, the user should run the command `python run.py n`.

Once the figure is generated, the user can adjust the initial probability of each node being infected with the sliders found at the bottom of the figure.

To adjust the transmission rates between nodes, an Excel file is generated in the same directory as the files. The Excel file labels the rows and columns with the node numbers such that (row, column) corresponds to the transmission rate from the row node to the column node.

Ex. (Node 0, Node 4) contains the probability that Node 0 will infect Node 4.

The Excel file must be saved once changes are made.

Once all inputs are made, the user can press the `Timestep` button found on the figure to watch how the virus diffuses among the population. 

The `Timestep` button can be pressed multiple times to simulate the passage of time in the model.

Additionally, the transmission rates can be adjusted after any timestep by making changes to the Excel file and saving.