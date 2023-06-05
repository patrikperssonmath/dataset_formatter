from cv_graph.trace_generator import TraceGenerator
from cv_graph.covisibility_graph_generator_multi_core import CovisibilityGraphGenerator
import glob
import os
import argparse
from generic_dataset import GenericDataset


def main(paths):

    # paths = "/database/data/EuRoCMavDatasets/*/"

    for path in glob.glob(paths):

        image_size = [480, 480]

        dataset = GenericDataset(os.path.join(path, "cam0"),
                                 os.path.join(path, "mav0/cam0/data/*.png"),
                                 os.path.join(path, "mav0/cam0/sensor.yaml"),
                                 image_size)

        trace_gen = TraceGenerator(True)

        result_path = trace_gen.calculate(dataset)

        cv_graph_gen = CovisibilityGraphGenerator(max_homography_agreement=0.9, scale=image_size)

        cv_graph_gen.calculate(result_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--path', type=str,
                        default="/database/mav/*")

    args = parser.parse_args()

    main(args.path)
