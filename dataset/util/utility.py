import numpy as np
import torch
from scipy.spatial.transform import Rotation

from collections import Counter


def read_ply(filename):
    """ reads a ply file assuming that the header is 11 rows long """

    points = np.genfromtxt(filename, skip_header=11)

    return np.stack(points[:, 0:3])


def normalize_calibration(calibration, H, W):
    fx, fy, cx, cy = calibration.tolist()

    return np.array([fx/(W-1.0), fy/(H-1.0), cx/(W-1.0), cy/(H-1.0)])


def pose_matrix_to_quaternion(pose):
    """ convert 4x4 pose matrix to (t, q) """
    q = Rotation.from_matrix(pose[:3, :3]).as_quat()
    return np.concatenate([pose[:3, 3], q], axis=0)


def to_K(calibration):
    """ converts between vector and corresponding K matrix"""
    K = np.eye(4)

    K[0, 0] = calibration[0]
    K[1, 1] = calibration[1]
    K[0, 2] = calibration[2]
    K[1, 2] = calibration[3]

    return K


def to_vec(K):
    """ converts between K matrix and corresponding vector"""
    return np.array([K[0, 0], K[1, 1], K[0, 2], K[1, 2]])


def project(calibration, T, X):
    """ projects 3d points """

    _, nbr_points = X.shape

    X = np.concatenate((X, np.ones((1, nbr_points), dtype=X.dtype)))

    K = to_K(calibration)

    point_cam0 = (K @ np.linalg.inv(T)).dot(X)

    point_cam0 = point_cam0[:, point_cam0[2, :] > 0]

    point_cam0[0:2, :] = point_cam0[0:2, :]/point_cam0[2:3, :]

    return point_cam0


def sub2ind(matrix_size, row_sub, col_sub):
    """ calculates the index from row and col """
    _, cols = matrix_size
    return row_sub * (cols-1) + col_sub - 1


def generate_depth_map(point_cam0, im_shape):
    """ creates a depth map from projections """

    point_cam0 = point_cam0[:, point_cam0[0, :] > 0]

    point_cam0 = point_cam0[:, point_cam0[1, :] > 0]

    point_cam0 = point_cam0[:, point_cam0[0, :] < im_shape[1]]

    point_cam0 = point_cam0[:, point_cam0[1, :] < im_shape[0]]

    x = np.round(point_cam0[0, :]-0.5).astype(np.int32)

    y = np.round(point_cam0[1, :]-0.5).astype(np.int32)

    depth = np.zeros((im_shape[:2]))

    depth[y, x] = point_cam0[2, :]

    # select the closest point from duplicates
    inds = sub2ind(depth.shape, point_cam0[1, :], point_cam0[0, :])

    dupe_inds = [item for item, count in Counter(
        inds).items() if count > 1]

    for dup_point in dupe_inds:
        pts = np.where(inds == dup_point)[0]
        x_loc = int(point_cam0[0, pts[0]])
        y_loc = int(point_cam0[1, pts[0]])
        depth[y_loc, x_loc] = point_cam0[2, pts].min()

    depth[depth < 0] = 0

    return depth


def stack_maps(li):

    out_dict = {}

    for dict in li:

        for k, v in dict.items():

            if k not in out_dict:
                out_dict[k] = []

            if not torch.is_tensor(v):
                v = torch.tensor(v)

            out_dict[k].append(v)

    for k, v in out_dict.items():

        out_dict[k] = torch.stack(v)

    return out_dict