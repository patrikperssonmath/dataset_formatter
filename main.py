from cv_graph.trace_generator import TraceGenerator
from cv_graph.covisibility_graph_generator_multi_core import CovisibilityGraphGenerator
import glob
import cv2
import os
import yaml
import numpy as np
import sys

from dataset.tartanair import TartanAir

def main():

    paths = "/database/tartanair/export/*/*/*/*"
    paths = glob.glob(paths)

    for path in paths:

        dataset = TartanAir(path)

        trace_gen = TraceGenerator(False)

        result_path = trace_gen.calculate(dataset)

        cv_graph_gen = CovisibilityGraphGenerator()

        cv_graph_gen.calculate(result_path)


if __name__ == "__main__":
    main()
