!pip install svgwrite cairosvg
test_cases_borders = ['frag0.csv','frag01_sol.csv','frag1.csv','frag2.csv','frag2_sol.csv','isolated.csv','isolated_sol.csv','occlusion1_rec.png','occlusion1_sol_rec.png','occlusion2_rec.png','occlusion2_sol_rec.png']
test_cases_polygons = ['occlusion1.csv','occlusion1_sol.csv','occlusion2.csv','occlusion2_sol.csv']
import numpy as np
import matplotlib.pyplot as plt
import svgwrite
import cairosvg
from PIL import Image
from google.colab import files
import re
import matplotlib.image as mpimg

# Function to read CSV files
def read_csv(csv_path):
  np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
  path_XYs = []
  for i in np.unique(np_path_XYs[:, 0]):
    npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
    XYs = []
    for j in np.unique(npXYs[:, 0]):
      XY = npXYs[npXYs[:, 0] == j][:, 1:]
      XYs.append(XY)
    path_XYs.append(XYs)
  return path_XYs

# Function 1: Polygon color filling
def polygon_color_filling(csv_filename, colours):

  # Function to plot the paths and fill them with colors
  def plot(paths_XYs, colours):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for i, XYs in enumerate(paths_XYs):
      c = colours[i % len(colours)]
      for XY in XYs:
        ax.fill(XY[:, 0], XY[:, 1], c=c, edgecolor='black', linewidth=2)  # Fill the polygon with color
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()  # Invert the y-axis to match the SVG coordinate system
    plt.show() #displays the plot

  # Function to convert paths to SVG and rasterize to PNG
  def polylines2svg(paths_XYs, svg_path, colours): # fun which converts polygons to an svg file and then into png file.
    W, H = 0, 0
    for path_XYs in paths_XYs:
      for XY in path_XYs:
        W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))
    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)
    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges') #creates an svg drawing object.
    group = dwg.g()
    for i, path in enumerate(paths_XYs):
      path_data = ""
      c = colours[i % len(colours)]
      for XY in path:
        path_data += f"M {XY[0, 0]} {XY[0, 1]} "
        for j in range(1, len(XY)):
            path_data += f"L {XY[j, 0]} {XY[j, 1]} "
        path_data += "Z"  # Ensure the path is closed
      group.add(dwg.path(d=path_data.strip(), fill=c, stroke='black', stroke_width=2))  # Fill the SVG shape with color
    dwg.add(group)
    dwg.save()
    png_path = svg_path.replace('.svg', '.png')
    fact = max(1, 1024 // min(H, W))
    cairosvg.svg2png(url=svg_path, write_to=png_path, parent_width=W, parent_height=H, output_width=fact*W, output_height=fact*H, background_color='white') #converts svg to png format with scaling.

  # Read the CSV file
  paths_XYs = read_csv(csv_filename)

  # Plot the paths and fill them with colors
  plot(paths_XYs, colours)

  # Rasterize and save as SVG and PNG
  output_svg_path = csv_filename.replace('.csv', '.svg')
  polylines2svg(paths_XYs, output_svg_path, colours)

  # Download the output files
  # files.download(output_svg_path)
  # files.download(output_svg_path.replace('.svg', '.png'))

# Function 2: Border color filling and quarter extraction
def border_color_filling(csv_filename, colours):

  # Function to plot the paths
  def plot(paths_XYs, colours):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for i, XYs in enumerate(paths_XYs):
      c = colours[i % len(colours)]
      for XY in XYs:
        ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()  # Invert the y-axis to match the SVG coordinate system
    plt.show()

  # Function to convert paths to SVG and rasterize to PNG
  def polylines2svg(paths_XYs, svg_path, colours):
    W, H = 0, 0
    for path_XYs in paths_XYs:
      for XY in path_XYs:
        W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))
    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)
    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')
    group = dwg.g()
    for i, path in enumerate(paths_XYs):
      path_data = ""
      c = colours[i % len(colours)]
      for XY in path:
        path_data += f"M {XY[0, 0]} {XY[0, 1]} "
        for j in range(1, len(XY)):
          path_data += f"L {XY[j, 0]} {XY[j, 1]} "
        if not np.allclose(XY[0], XY[-1]):
          path_data += "Z"
      group.add(dwg.path(d=path_data.strip(), fill=c, stroke='none', stroke_width=2))
    dwg.add(group)
    dwg.save()
    png_path = svg_path.replace('.svg', '.png')
    fact = max(1, 1024 // min(H, W))
    cairosvg.svg2png(url=svg_path, write_to=png_path, parent_width=W, parent_height=H, output_width=fact*W, output_height=fact*H, background_color='blue')

  # Read the CSV file
  paths_XYs = read_csv(csv_filename)

  # Plot the paths
  plot(paths_XYs, colours)

  # Rasterize and save as SVG and PNG
  output_svg_path = csv_filename.replace('.csv', '.svg')
  polylines2svg(paths_XYs, output_svg_path, colours)

uploaded = files.upload()
print(uploaded.keys())
for filename in uploaded.keys():
  formatted_filename = re.sub(r'\s\(\d+\)', '', filename)
  print(formatted_filename)
  if formatted_filename in test_cases_borders:
    if formatted_filename == 'frag0.csv' or formatted_filename == 'frag1.csv' or formatted_filename == 'frag2.csv' or formatted_filename == 'frag2_sol.csv' or formatted_filename == 'isolated.csv':
      colors = ['black']
      border_color_filling(filename,colors)
    elif formatted_filename == 'isolated_sol.csv':
      colors = ['red']
      border_color_filling(filename,colors)
    elif formatted_filename == 'frag01_sol.csv':
      colors = ['yellow']
      border_color_filling(filename,colors)
    elif formatted_filename == 'occlusion1_rec.png' or formatted_filename == 'occlusion1_sol_rec.png' or formatted_filename == 'occlusion2_rec.png' or formatted_filename == 'occlusion2_sol_rec.png':
      img = mpimg.imread(formatted_filename)
      plt.imshow(img)
      plt.axis('off')  # Hide the axes
      plt.show()
  elif formatted_filename in test_cases_polygons:
    if formatted_filename == 'occlusion1.csv' or formatted_filename == 'occlusion1_sol.csv':
      colors = ['yellow','lightgreen']
      polygon_color_filling(filename, colors)
    elif formatted_filename == 'occlusion2.csv' or formatted_filename == 'occlusion2_sol.csv':
      colors = ['white']
      polygon_color_filling(filename, colors)

  else:
    print(f"Unknown file type: {filename}. No processing performed.")
