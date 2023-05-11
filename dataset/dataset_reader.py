

class DatasetReader:

    def __init__(self) -> None:
        pass

    def get_path(self):
        """ returns the dataset name """
        raise NotImplementedError

    def get_name(self):
        """ returns the dataset name """
        raise NotImplementedError

    def get_pose(self, idx):
        return None

    def get_depth(self, idx):
        return None, None

    def get_image(self, idx):
        raise NotImplementedError

    def get_3d_points(self, idx):
        return None

    def __len__(self):
        """ length of the dataset """
        raise NotImplementedError

    def get_neighbours(self, idx):
        raise NotImplementedError
