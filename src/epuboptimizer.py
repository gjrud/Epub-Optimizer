import argparse
import logging
import os
import sys
import zipfile
import shutil

from PIL import Image, ImageFile

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "--input",
    required=True,
    type=str,
    help="Input File",
)
parser.add_argument(
    "--output",
    required=True,
    type=str,
    help="Output folder",
)
parser.add_argument(
    "--debug",
    required=False,
    type=bool,
    help="Debug flag",
)
args = parser.parse_args()

if args.debug:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
logger = logging.getLogger("EPUB Optimizer")
output_path = ""
input_path = ""
input_files = []


def parse_arguments():
    global output_path, input_path, input_files
    output_path = args.output
    if not os.path.exists(args.input):
        logger.error("enter a valid file or folder path")
        sys.exit(1)
    if os.path.isfile(args.input):
        logger.debug(f"{args.input} is a file")
        input_path = os.path.dirname(args.input)
        input_files = [os.path.basename(args.input)]
    else:
        logger.debug(f"{args.input} is a path")
        input_path = args.input
        input_files = os.listdir(input_path)


def decompress():
    logger.info("Starting EPUB Extraction")
    for file in input_files:
        if not file.endswith(".epub"):
            logger.debug(f"{file} is not an EPUB, skipping")
            continue
        logger.debug(f"Extracting {file}")
        with zipfile.ZipFile(f"{input_path}\\{file}", "r") as zip_ref:
            zip_ref.extractall(f"{output_path}\\{file[:-5]}")


def optimize():
    logger.info("Starting EPUB's Images Optimization")
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    for dir_path, _, files in os.walk(output_path):
        for file in [
            f
            for f in files
            if (f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png"))
        ]:
            logger.debug(f"Optimizing {dir_path}\\{file}")
            image = Image.open(f"{dir_path}\\{file}")
            image.save(f"{dir_path}\\{file}", optimize=True)


def compress_and_clean():
    logger.info("Starting Optimized EPUB Export")
    for dir in os.listdir(output_path):
        with zipfile.ZipFile(
            f"{output_path}\\{dir}.epub", "w", zipfile.ZIP_DEFLATED
        ) as zipf:
            for root, _, files in os.walk(f"{output_path}\\{dir}"):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_path = os.path.relpath(file_path, f"{output_path}\\{dir}")
                    zipf.write(file_path, archive_path)
        logger.debug(f"Optimization completed, cleaning up {output_path}\\{dir}")
        shutil.rmtree(f"{output_path}\\{dir}")


parse_arguments()
decompress()
optimize()
compress_and_clean()