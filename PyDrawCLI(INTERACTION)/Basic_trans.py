import numpy as np
def translation(points,trans_X,trans_Y):
    new_points = []
############将得到新顶点的代码放在下方############
    translation_matrix = np.array([
        [1, 0, trans_X],
        [0, 1, trans_Y],
        [0, 0, 1]
    ])
    homogeneous_points = np.array([[x, y, 1] for x, y in points])
    transformed_points = homogeneous_points @ translation_matrix.T
    new_points = [(x, y) for x, y, _ in transformed_points]
################################################
    return new_points




def rotation(points,angle):
    new_points = []
############将得到新顶点的代码放在下方############
    radians = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(radians), -np.sin(radians), 0],
        [np.sin(radians), np.cos(radians), 0],
        [0, 0, 1]
    ])
    homogeneous_points = np.array([[x, y, 1] for x, y in points])
    transformed_points = homogeneous_points @ rotation_matrix.T
    new_points = [(x, y) for x, y, _ in transformed_points]
################################################
    return new_points





def scale(points,scale_X,scale_Y):
    new_points = []
############将得到新顶点的代码放在下方############
    scale_matrix = np.array([
        [scale_X, 0, 0],
        [0, scale_Y, 0],
        [0, 0, 1]
    ])
    homogeneous_points = np.array([[x, y, 1] for x, y in points])
    transformed_points = homogeneous_points @ scale_matrix.T
    new_points = [(x, y) for x, y, _ in transformed_points]
################################################
    return new_points
