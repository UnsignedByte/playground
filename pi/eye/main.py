# Eye stuff
import os
import numpy as np
from draw import draw_message
import matplotlib.pyplot as plt

root = os.path.dirname(os.path.abspath(__file__))

# Read the eye data from the file
eyes: list[list[list[int]]] = []
with open(os.path.join(root, "eye.txt"), "r") as file:
    # loop through the lines
    cur = []
    for line in file:
        if line != "\n":
            cur.append([int(x) for x in list(line.strip()[:-1])])
        else:
            eyes.append(cur)
            cur = []

results = os.path.join(root, "results")
os.makedirs(results, exist_ok=True)
os.makedirs(os.path.join(results, "raw_messages"), exist_ok=True)

name_map = [
    "east1",
    "west1",
    "east2",
    "west2",
    "east3",
    "west3",
    "east4",
    "west4",
    "east5",
]

images = [draw_message(msg) for msg in eyes]

# Draw the eye images
for i in range(len(images)):
    # Save as black and white png
    plt.imsave(
        os.path.join(results, "raw_messages", f"{name_map[i]}.png"),
        images[i],
        cmap="binary",
    )

# Put all the eye images in one image

# Find the maximum width and height
max_width = max(image.shape[1] for image in images)
max_height = max(image.shape[0] for image in images)

# Create a blank image
padding = 10
full_image = np.zeros(
    (
        (max_height + padding) * ((len(images) + 1) // 2) - padding,
        max_width * 2 + padding,
    ),
    dtype=int,
)

# Draw the images
for i, image in enumerate(images):
    x = (i % 2) * (max_width + padding)
    y = (i // 2) * (max_height + padding)
    full_image[y : y + image.shape[0], x : x + image.shape[1]] = image

# Save the full image
plt.imsave(os.path.join(results, "raw_messages", "all.png"), full_image, cmap="binary")
