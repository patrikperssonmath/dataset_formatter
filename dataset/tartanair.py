""" loads scannet .sense datasets """
import os

import numpy as np
import torch
from scipy.spatial.transform import Rotation
from torch.nn.functional import interpolate
from torchvision.io.image import read_image

from dataset.dataset_reader import DatasetReader
from dataset.util.utility import normalize_calibration


def pos_quats2SE_matrice(quat):
    SO = Rotation.from_quat(quat[3:7]).as_matrix()
    SE = np.eye(4)
    SE[0:3, 0:3] = SO
    SE[0:3, 3] = quat[0:3]

    return SE


def SE2pos_quat(SE_data):
    pos_quat = np.zeros(7)
    pos_quat[3:] = SO2quat(SE_data[0:3, 0:3])
    pos_quat[:3] = SE_data[0:3, 3].T
    return pos_quat


def SO2quat(SO_data):
    rr = Rotation.from_matrix(SO_data)
    return rr.as_quat()


def ned2cam(traj):
    '''
    transfer a ned traj to camera frame traj
    '''
    T = np.array([[0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [1, 0, 0, 0],
                  [0, 0, 0, 1]], dtype=np.float32)

    T_inv = np.linalg.inv(T)

    tt = pos_quats2SE_matrice(np.array(traj))

    ttt = T.dot(tt).dot(T_inv)
    ttt = SE2pos_quat(ttt)

    return ttt


class TartanAir(DatasetReader):
    """ loads scannet .sense datasets """

    def __init__(self, dataset_path, **kwargs):
        super().__init__()

        self.dataset_path = dataset_path

        self.calibration = np.array([320.0, 320.0, 320.0, 240])

        self.images = []

        img_path = os.path.join(dataset_path, "image_left")

        for file in os.listdir(img_path):
            self.images.append(os.path.join(img_path, file))

        self.images.sort()

        depth_path = os.path.join(dataset_path, "depth_left")

        self.depths = []

        for file in os.listdir(depth_path):
            self.depths.append(os.path.join(depth_path, file))

        self.depths.sort()

        self.pose_left = np.loadtxt(
            os.path.join(dataset_path, "pose_left.txt"))

    def get_path(self):
        """ returns the dataset name """

        return self.dataset_path

    def get_name(self):

        return os.path.split(self.dataset_path)[-1]

    def __len__(self):
        return len(self.images)

    def get_image(self, idx):
        """ reads an image """

        image = read_image(self.images[idx]).float()/255.0

        return image, self.calibration

    def get_depth(self, idx):
        """ reads a depth map """

        depth = np.load(self.depths[idx])

        depth = torch.from_numpy(depth.astype(np.float32)).unsqueeze(0)

        return depth, self.calibration

    def get_pose(self, idx):
        """ returns pose T:4x4 (points in camera  are transformed to world) \n
            returns None if no pose is available
        """

        return ned2cam(self.pose_left[idx])
