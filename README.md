# Post-Wiring Pre-Routing .Rect File Design Checker

Rectcheck.py is a tool created by Sophia DeVito and Tanya Shibu as a final project for Silicon Compilation (EENG 426). It is a python script that is designed to identify elements in a .rect file that may be difficult for the router to handle, and will therefore cause DRC violations once the cell is routed using the interact tool. Once it identifies these possible problem areas, it generates a magic script to label them, so that the user can easily edit the cell and avoid the error. To decide which elements might cause issues, the tool takes into account the design strategies we discovered through trial and error in Lab 4. It is editible so that it is useful for different design rules and requirements.

---
Specifically, this tool identifies three key problems that may lead to DRC errors when a cell is routed:
1. It ensures that all of the elements that the router might choose as connection ports are a minimum distance of **port_distance** away from each other. This is in order to avoid ports being so close to each other that the routed connections connect to more than one accidentally. The minimum distance value can be changed depending on the design rules or routing expectations for the cell. 
2. It checks the distance between the outer edge of the routable ports and the perimeter of the cell, using a distance of **VARIABLE HERE**. If the router is trying to connect to a port that is too close to the center of the cell, it again may accidentally connected to more than the intended metal. This variable is also editable.
3. It ensures that there is a m2 connection for Vdd and GND. If there is not, the router will have trouble making these connections.
---
To use this tool, follow these steps in the docker container:
1. Generate a file example.rect that has already gone through manual wiring and routing using `mag2rect_sky130.py example.mag > example.rect`
2. Run `python rectcheck.py example.rect` to generate a new magic script, labels.scr
3. Generate a .tcl file from that .rect file using `mag.pl example.rect > example.tcl`
4. Open magic and run the command `source example.tcl`
5. Run the command `select` to select the topmost cell in the window. (Optional step: run `erase label` to remove exsisting labels in order to see the ones gerenated by rectcheck.py clearly)
6. Manually select the bottom left corner of the selection window
7. Run `source labels.tcl` to generate the suggested edits to your cell
---
This repo includes a few example .rect files to demonstrate the capabilities of this tool.
