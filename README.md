<b>Summary</b>:

The pyqtgraph based code simulates in a quick and dirty way the X-ray diffraction rings (qualititive) for a given crystal structure. One can define the structure based on lattice parameters and the space group.
Program constrains the detector to the plane normal to the X-ray beam.

<b>How to use</b>:

Copy the two files. Make sure mpxrd_libraries_.py is in the path. Run mpXRDSim_interactive_.py on a python console. Needs pyqtgraph, numpy and math with python v 3.7+ to run.

<b>Notes</b>:

Adding more space groups to the list is easy. Define the space group name and number in the dictionary in mpxrd_libraries_.py. Create a new function which checks for the conditions and returns True/False based on them. For the list of reflection conditions, refer to https://www.cryst.ehu.es/cryst/get_hkl.html.
Apologies for bugs, if any. Write to me for updates/help.
