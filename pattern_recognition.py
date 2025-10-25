from scipy.spatial.distance import euclidean
import pygame, json, math, glob
from fastdtw import fastdtw
from sys import exit
import numpy as np


def preprocess(path: list, n=64) -> list:
    if len(path) < 2: return np.zeros((n, 2)) # Handling empty path
    xy = np.array(path).astype("float32") # (x, y)
    xy -= xy.mean(axis=0)               # Centering
    xy /= xy.max()                      # Scaling to [-1, 1]
    idx = np.linspace(0, len(xy) - 1, n).astype(int)
    return xy[idx]


def classify_dtw(points):
    test = preprocess(points)
    prediction, best_cost = None, math.inf # Saves prediction and cost
    for name, ref in templates.items():
        dist, _ = fastdtw(test, ref, dist=euclidean)
        if dist < best_cost:
            prediction, best_cost = name, dist
    
    return prediction if best_cost < 20 else None # 20 - empirical treshold


# Load patterns
templates = dict()
for file in glob.glob('template_*.json'):
    name = file.replace("template_", "").replace(".json", "")
    with open(file, 'r') as f:
        template = json.load(f)
        templates[name] = preprocess(template)
# =============================================================================
#                             PYGAME
# =============================================================================
pygame.init()
W, H = 500, 700

screen = pygame.display.set_mode((W, H))
font = pygame.font.SysFont("comicsans", 40)
clock = pygame.time.Clock()

drawing, points, gesture = False, list(), list() # Drawings
recognized_shape = None # Shape
start_drawing = 0 # For timer
duration = 2500 # Time in miliseconds

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                # For making files with gestures
                if gesture:
                    name = input("Name of this shape: ")
                    with open(f"template_{name}.json", "w") as f:
                        dump = json.dumps(gesture)
                        f.write(dump)
                    templates[name] = preprocess(gesture)
        
        if event.type == pygame.MOUSEMOTION and drawing: # One-time event
            pygame.draw.circle(screen, "white", event.pos, radius=5)
            points.append(event.pos)
            
        if event.type == pygame.MOUSEBUTTONUP: # One-time event
            gesture = points.copy()
            drawing = False

            recognized_shape = classify_dtw(points)
            points = list() # Reset

    # Left mouse button
    lmb_click = pygame.mouse.get_just_pressed()[0]
    lmb_pressed = pygame.mouse.get_pressed(3)[0]
    if lmb_pressed:
        start_drawing = pygame.time.get_ticks()
        drawing = True

    # Simple timer
    if pygame.time.get_ticks() - start_drawing >= duration or lmb_click:
        recognized_shape = None
        screen.fill("black")
    
    # Will display title with recognized shape
    if recognized_shape:
        text = font.render(f"Identified: {recognized_shape}", True, "white")
        rect = text.get_rect(center=(W / 2, H - 50))
        screen.blit(text, rect)
    
    pygame.display.flip()
    clock.tick(60)
