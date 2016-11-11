import math

def add_points(a, b):
    return (a[0] + b[0], a[1]+b[1], a[2]+ b[2])

def subtract_points(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def scale_point(p, c):
    return (c*p[0], c*p[1], c*p[2])

def intersect_ray_sphere(ray, sphere):
    (a, v) = ray
    (c, r) = sphere
    dim = 3

    ca = cb = cc = 0
    for i in range(dim):

        ca += v[i]*v[i]
        cb += 2*v[i]*(a[i]-c[i])
        cc += (a[i]-c[i])**2

    cc -= r * r

    discrim = cb*cb - 4*ca*cc

    if (discrim < 0):
        return None

    i1 = (-cb-math.sqrt(discrim))/(2*ca)
    i2 = (-cb+math.sqrt(discrim))/(2*ca)

    if (i1 >= 0 and i2 >= 0):
        i = min(i1,i2)
        return add_points(a, scale_point(v, i))

    return None


def dot_product(a, b):
    return a[0] * b[0] + a[1]* b[1] + a[2] * b[2]

def norm(v):
    return math.sqrt(dot_product(v, v))
def arange(start, stop, steps):
    step = (float(stop)-start)/steps
    for i in range(steps):
        yield start + i*step


def calculate_luminance(point, light, spheres):
    light_point, color = light
    v = subtract_points(point, light_point)
    intersect = False
    for sphere in spheres:
        if intersect_ray_sphere((light_point, v), sphere) is not None:
            intersect = True
            break
    if not intersect:
        return (0,0,0)

    else:
        dist = norm(v)
        return scale_point(color, 1/(dist**2))

#TODO use grid
def ray_cast_through_grid(grid, eye, light, sphere):
    n =800
    luminance_array = [[(0,0,0)]*n for i in range(n)]
    default_color = (0.0,0.0,0.0)
    for i in range(n):
        for j in range (n):
            x = -1 + (2.0/n) * i
            y = -1 + (2.0/n) * j
            v = subtract_points((x,y,0), eye)
            point = intersect_ray_sphere((eye,v), sphere)
            if point is not None:
                luminance_array[i][j] = gamma_encode(calculate_luminance(point, light, [sphere]))
            else:
                luminance_array[i][j] = default_color

    return luminance_array

def gamma_encode(color):
    return (color[0]**(1/2.2), color[1]**(1/2.2), color[2]**(1/2.2))

black = (0.0,0.0,0.0)
color = (0.0,1.0,0.2)

def main():
    array = ray_cast_through_grid(None, (0,0,-1), ((-1,5,0.0),color), ((0,0,4), 3.0))
    return array





