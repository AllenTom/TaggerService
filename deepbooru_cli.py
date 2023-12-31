import argparse
import base64

import PIL

from modules import deepbooru
import json
import os


def get_image_list_from_dir(dir):
    images = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file = file.lower()
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
                images.append(os.path.join(root, file))
    return images


def main():
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add a flag argument
    parser.add_argument('--image', action='store')
    parser.add_argument('--input_base64', action='store')
    parser.add_argument('--dir', action='store')
    parser.add_argument('--threshold', action='store', default=float(0.7), type=float)
    parser.add_argument('--with_rank', action='store_true')
    parser.add_argument('--per', action='store_true')
    parser.add_argument('--no_result', action='store_false')
    # Parse the arguments
    args = parser.parse_args()
    dbr = deepbooru.DeepDanbooru()
    dbr.load()
    dbr.start()
    srcs = []
    if args.dir:
        srcs = get_image_list_from_dir(args.dir)
    else:
        srcs = [args.image]
    if srcs is None:
        print("No images found")
        return
    result = []
    if args.input_base64:
        # decode
        decoded_bytes = base64.b64decode(args.input_base64)
        decoded_string = decoded_bytes.decode('utf-8')
        input_obj = json.loads(decoded_string)
        if "files" in input_obj:
            srcs = input_obj["files"]

    for src in srcs:
        testImage = PIL.Image.open(src)
        tag_str = dbr.tag_multi(testImage, threshold=args.threshold, include_ranks=args.with_rank)
        if not args.with_rank:
            tags = tag_str.split(",")
        else:
            tags = tag_str
        item = {
            "filename": os.path.basename(src),
        }
        if args.with_rank:
            item["tags"] = tags
        else:
            item["tags"] = [x.strip() for x in tags]
        result.append(item)
        if args.per:
            print(json.dumps(item))
    if args.no_result:
        print(json.dumps(result))


if __name__ == '__main__':
    main()
