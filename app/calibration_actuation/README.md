### Here is a basic overview of the functionality related specifically to Calibration & Actuation

**Note:**
Up to date code for calibration and actuation can be found in:
```
cameraarm/app/modeling_gui/ModelingWindow/src/

calibration_actuation.cxx
calibration_actuation.h
move.py
```


### Supporting Tests

##### Printing additional Markers:
Markers that are saved and currently recognizable by the system are saved at
```
cameraarm/app/calibration_actuation/testing/aruco_markers/
```
**For proper analysis all markers must be .16m, or 16cm, when printed**

**Do not forget to update the code if more markers are added:**
In ```cameraarm/app/modeling_gui/ModelingWindow/src/calibration_actuation.cxx``` update to add ```Vec3d mki (x, y, z);``` for each marker ```i``` added with location in modeling world.


#### Saving images:
Run `save` within `calibration_actuation/`
with command: `$ ./save [fileName.png]`
