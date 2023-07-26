import argparse
import os
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from bing_homepage_images import BingHomepageImages


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

    bing = BingHomepageImages()

    if args.list:

        print("Index | Date       | Title")
        print("=" * 80)

    output_path = Path(args.path)

    if not output_path.exists():
        os.makedirs(output_path)

    for idx, image in enumerate(bing.get_images()):

        if idx < args.index:
            continue

        if args.list:
            
            print(f"{idx:5} | {image.startdate:%Y-%m-%d} | {image.title}")
        
        else:

            split_url = urlsplit("file://example.com" + image.url)

            qs = parse_qs(split_url.query)

            output_filepath = output_path / qs.get("id", ["bing_image.jpg", ])[0]

            if not output_filepath.exists():

                with open(output_filepath, "wb") as save_image:
                    image.save_image(save_image)

        args.num_entries -= 1
        if args.num_entries <= 0:
            break

if __name__ == "__main__":
    main()
