from cv_graph.trace_generator import TraceGenerator
from cv_graph.covisibility_graph_generator_multi_core import CovisibilityGraphGenerator
import glob
import argparse

from dataset.tartanair import TartanAir


def main():

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("--paths", type=str,
                        default="/database/tartanair/export/*/*/*/*")

    args = parser.parse_args()

    paths = args.paths
    paths = glob.glob(paths)

    image_size = [480, 640]

    for path in paths:

        dataset = TartanAir(path)

        trace_gen = TraceGenerator(False)

        result_path = trace_gen.calculate(dataset)

        cv_graph_gen = CovisibilityGraphGenerator(max_homography_agreement=0.9, scale=image_size)

        cv_graph_gen.calculate(result_path)


if __name__ == "__main__":
    main()
