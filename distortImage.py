import cv2
import numpy as np
import math
from vcam import vcam,meshGen
import random
p = "/Users/xuhuan/CaptchaProject/archive/_test/cat/"
paths = ["cat_0082.jpg"]

mode = random.randint(0, 7)
for i, path in enumerate(paths):
	# Reading the input image
	img = cv2.imread(p + path)
	img = cv2.resize(img,(300,300))
	H,W = img.shape[:2]

	# Creating the virtual camera object
	c1 = vcam(H=H,W=W)

	# Creating the surface object
	plane = meshGen(H,W)

	# We generate a mirror where for each 3D point, its Z coordinate is defined as Z = F(X,Y)

	if mode == 0:
		plane.Z += 20*np.exp(-0.5*((plane.X*1.0/plane.W)/0.1)**2)/(0.1*np.sqrt(2*np.pi))
	elif mode == 1:
		plane.Z += 20*np.exp(-0.5*((plane.Y*1.0/plane.H)/0.1)**2)/(0.1*np.sqrt(2*np.pi))
	elif mode == 2:
		plane.Z -= 10*np.exp(-0.5*((plane.X*1.0/plane.W)/0.1)**2)/(0.1*np.sqrt(2*np.pi))
	elif mode == 3:
		plane.Z -= 10*np.exp(-0.5*((plane.Y*1.0/plane.W)/0.1)**2)/(0.1*np.sqrt(2*np.pi))
	elif mode == 4:
		plane.Z += 20*np.sin(2*np.pi*((plane.X-plane.W/4.0)/plane.W)) + 20*np.sin(2*np.pi*((plane.Y-plane.H/4.0)/plane.H))
	elif mode == 5:
		plane.Z -= 20*np.sin(2*np.pi*((plane.X-plane.W/4.0)/plane.W)) - 20*np.sin(2*np.pi*((plane.Y-plane.H/4.0)/plane.H))
	elif mode == 6:
		plane.Z += 100*np.sqrt((plane.X*1.0/plane.W)**2+(plane.Y*1.0/plane.H)**2)
	elif mode == 7:
		plane.Z -= 100*np.sqrt((plane.X*1.0/plane.W)**2+(plane.Y*1.0/plane.H)**2)
	else:
		print("Wrong mode selected")
		exit(-1)

	# Extracting the generated 3D plane
	pts3d = plane.getPlane()

	# Projecting (Capturing) the plane in the virtual camera
	pts2d = c1.project(pts3d)

	# Deriving mapping functions for mesh based warping.
	map_x,map_y = c1.getMaps(pts2d)

	# Generating the output
	output = cv2.remap(img,map_x,map_y,interpolation=cv2.INTER_LINEAR)
	output = cv2.flip(output,1)
	output = output[60:240, 60:240]
	cv2.imwrite(p + "distorted_" + str(mode) + path, output)
