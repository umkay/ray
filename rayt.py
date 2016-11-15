import math
import matplotlib.pyplot as plt

def add_points(a, b):
    return (a[0] + b[0], a[1]+b[1], a[2]+ b[2])

def subtract_points(b, a):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def scale_point(p, c):
    return (c*p[0], c*p[1], c*p[2])

def dot_product(a, b):
    return a[0] * b[0] + a[1]* b[1] + a[2] * b[2]

def cross_product():
    pass

def vector_norm(v):
    return math.sqrt(dot_product(v, v))

def normalize(v):
    return scale_point(v, 1 / vector_norm(v))

def arange(start, stop, steps):
    step = (float(stop)-start)/steps
    for i in range(steps):
        yield start + i*step

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
        intersection = add_points(a, scale_point(v, i))

        # calculate normal vector
        n = subtract_points(c, intersection)

        return intersection, normalize(n)

    return None

def calculate_luminance(point, norm, light, spheres, skip_index, eye):
    light_point, color = light
    v = subtract_points(light_point, point)
    intersect = False
    for i, sphere in enumerate(spheres):
        if i != skip_index and intersect_ray_sphere((light_point, v), sphere) is not None:
            intersect = True
            break
    if intersect:
        return (0,0,0)
    else:
        dist = vector_norm(v)

        # add Phong specular term
        v_hat = normalize(v)
        dist = 1/(dist**2)
        reflection_exp = 3

        ambient_constant = .005
        diff_constant = 1
        reflection_constant = 50

        phong_vector =subtract_points(v_hat, 2*(scale_point(norm, dot_product(norm, v_hat))))
        phong_term = max(dot_product(phong_vector, normalize(eye)), 0)**reflection_exp
        diff = max(-dot_product(v_hat, norm), 0)

        # use phong reflection
        x = scale_point(color, dist * (ambient_constant + diff_constant * diff + phong_term*reflection_constant))

         # add ambient light
        return x

        # diffuse luminance
        # return scale_point(color, max(-dot_product(norm, v_hat)*dist, 0))

def clamp(color):
    return (min(color[0], 1), min(color[1], 1), min(color[2], 1))

#TODO use grid
def ray_cast_through_grid(grid, eye, lights, spheres):
    n =400
    luminance_array = [[(0,0,0)]*n for i in range(n)]
    default_color = (0.0,0.0,0.0)
    for i in range(n):
        for j in range (n):
            x = -1 + (2.0/n) * i
            y = -1 + (2.0/n) * j
            eye_vector = subtract_points(eye, (x, y, 0))
            intersection_points = []
            test = intersect_ray_sphere((eye, eye_vector), spheres[0])
            print test, "TEST"

            for i, sphere in enumerate(spheres):
                print i, sphere
                pair = intersect_ray_sphere((eye, eye_vector), sphere)
                if pair is not None:
                    intersection_points.append((i, pair))
            if len(intersection_points) > 0:
                min_eye = (10000000000, -1)
                for i, pair in intersection_points:
                    point, norm = pair
                    # calculate min dist from eye
                    eye_dist = vector_norm(subtract_points(eye_vector, point))
                    if eye_dist < min_eye[0]:
                        min_eye = (eye_dist , i)

                print "HEY", min_eye
                point, norm = intersection_points[min_eye[1]]

                luminance_array[i][j] = (0, 0, 0)
                for light in lights:
                    luminance_array[i][j] = add_points(luminance_array[i][j],
                                                       calculate_luminance(point, norm, light, spheres, min_eye[1], eye_vector))
                luminance_array[i][j] = gamma_encode(clamp(luminance_array[i][j]))
            else:
                luminance_array[i][j] = default_color

    return luminance_array
def gamma_encode(color):
    return (color[0]**(1/2.2), color[1]**(1/2.2), color[2]**(1/2.2))

black = (0.0,0.0,0.0)
white = (1.0, 1.0, 1.0)
red = (0.25,0.0, 0.0)
blue = (0.05, 0.0, 0.5)
green = (0.0,1.0,0.0)

fart = [((0.5,2,0.5),blue), ((0.5,-2,0.5),blue),
       ((-0.5, 2, -0.5),red), ((0.5,-2,-0.5),red),
        ((-0.5,-2, 0.5),green), ((-0.5,-2,-0.5),green)]

single = [((0,0,-1), scale_point(white, 1.0))]

def main():
    array = ray_cast_through_grid(None, (0,0,-1), [((0.5, -2, 0), white)], [((0,0,4), 3.0)])
    plt.imshow(array)
    plt.show()

if __name__ == '__main__':
    main()



