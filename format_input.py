"""
Processes the wikimedia elasticsearch dump and removes all data not needed by our search program
Operates on stdin and writes to stdout so it can be chained with other tools
"""

import sys
import json

# Each key in the set will be output, any key not present will be ignored.
document_keys = {"title", "page_id", "text"}


def main():
    line_number = 0
    for raw_line in sys.stdin:
        parsed_line = json.loads(raw_line)
        # expect even lines are for metadata
        if line_number % 2 == 0:
            print(json.dumps({"index": {"_id": parsed_line["index"]["_id"]}}))
        # expect odd lines are for documents
        else:
            print(json.dumps({key: parsed_line[key] for key in document_keys}))
        line_number += 1


if __name__ == "__main__":
    main()
