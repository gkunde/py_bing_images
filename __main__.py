"""
MIT License

Copyright (c) 2023 Garrett Kunde

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

If LICENSE file is not included, please visit :
    https://github.com/gkunde/py_bing_images
"""
import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import SplitResult, parse_qs, parse_qsl, urlsplit

from bing import Bing


def parse_date(date: str) -> datetime:
    """
    """

    if not date:
        return None

    return datetime.strptime(date, "%Y%m%d")


def parse_datetime(fulldate: str) -> datetime:
    """
    """

    if not fulldate:
        return None

    return datetime.strptime(fulldate, "%Y%m%d%H%M")


class StoreIntInRange(argparse._StoreAction):

    MIN_RANGE: int = None
    MAX_RANGE: int = None

    def __call__(self, parser, namespace, values, option_string) -> None:

        error = None

        if self.MIN_RANGE is not None and values < self.MIN_RANGE:
            error = f"greater than or equal to {self.MIN_RANGE}"

        if self.MAX_RANGE is not None and values > self.MAX_RANGE:
            error = f"lesser than or equal to {self.MAX_RANGE}"

        if error:
            parser.error(
                f"Value for `{'` or `'.join(self.option_strings)}` must be {error}")

        return super().__call__(parser, namespace, values, option_string)


class StoreNumberOfEntries(StoreIntInRange):

    MIN_RANGE = 1
    MAX_RANGE = 15


class StoreImageIndex(StoreIntInRange):

    MIN_RANGE = 0
    MAX_RANGE = 14


class StoreOutputPath(argparse._StoreAction):

    def __call__(self, parser, namespace, values, option_string) -> None:

        values = Path(values)

        if values.exists() and not values.is_dir():
            parser.error(
                f"Value for `{'` or `'.join(self.option_strings)}` must be a directory.")

        return super().__call__(parser, namespace, values, option_string)


def main():

    arg_parser = argparse.ArgumentParser(
        description="Capture and download Microsoft's Bing Image of the Day")

    arg_parser.add_argument(
        "-n",
        "--num-entries",
        help="""\
            Download the specified number of images available, starting with
            the most recent image available. Default is 1 image.""",
        action=StoreNumberOfEntries,
        type=int,
        default=1)

    arg_parser.add_argument(
        "-x",
        "--index",
        help="Specifies the image index in the list of images to download.",
        action=StoreImageIndex,
        type=int,
        default=0)
    
    arg_parser.add_argument(
        "-m",
        "--metadata",
        help="""\
            Save a metadata JSON file containing the image's metadata.""",
        action="store_true")

    arg_parser.add_argument(
        "-l",
        "--list",
        help="List the available images with their index.",
        action="store_true")

    arg_parser.add_argument(
        "-p",
        "--path",
        help="""\
            The path were images are to be downloaded to. If the path does not
            exist, it will be created.""",
        action=StoreOutputPath,
        default=os.getcwd())

    args = arg_parser.parse_args()

    bing = Bing()

    if args.list:

        print("Date       | Title")
        print("=" * 80)

    output_path = Path(args.path)

    if not output_path.exists():
        os.makedirs(output_path)

    feed_response = bing.hp_image_archive.get_feed(
        args.num_entries,
        args.index)

    if feed_response.status_code != 200:
        raise RuntimeError(
            f"Unable to retrieve feed, server responded: {feed_response.status_code}")

    feed = json.loads(feed_response.content)

    for image in feed["images"]:

        startdate = parse_date(image["startdate"])

        if args.list:
            print(f"{startdate:%Y-%m-%d} | {image['title']}")

        else:

            split_url = urlsplit(image["url"])

            qs = parse_qsl(split_url.query)
            qs.append(("id", "bing_image.jpg", ))

            filename = [entry[1] for entry in qs if entry[0].strip().lower() == "id"][0]

            output_filepath: Path = output_path / filename

            if not output_filepath.exists():

                with open(output_filepath, "wb") as save_image:
                    bing.hp_image_archive.get_image(image["url"], save_image)

                if args.metadata:

                    metadata_filepath = output_path / f"{output_filepath.stem}.json"

                    if not metadata_filepath.exists():

                        with open(metadata_filepath, "w") as save_meta:
                            save_meta.write(json.dumps(image, indent=2))

        args.num_entries -= 1
        if args.num_entries <= 0:
            break


if __name__ == "__main__":
    main()
