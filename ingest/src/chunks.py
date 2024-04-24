import logging
import os
import json


logger = logging.getLogger(__name__)


def chunk_dump_file(src_file_path: str, dest_dir: str, keys: dict):
    """Splits a wikiquote dump file into many separate chunk files"""
    if os.path.isdir("chunks"):
        logger.info("Skipping dump file chunking, chunk directory already exists.")
        return
    logger.info("Splitting dump file into chunks")
    lines_per_chunk = 500
    num_chunks = 1
    current_chunk_file = None
    # ensure chunks dir exists before attempt to write to it.
    os.makedirs(dest_dir, exist_ok=True)
    with open(src_file_path) as dump_file:
        line_num = 0
        # read every two lines from the file
        while True:
            raw_metadata = dump_file.readline()
            raw_data = dump_file.readline()
            # eof
            if not raw_metadata or not raw_data:
                break
            # attempt to write out current chunk file and start a new one.
            if line_num % lines_per_chunk == 0:
                # finish with current chunk file.
                if current_chunk_file:
                    num_chunks += 1
                    current_chunk_file.close()
                # start new chunk file.
                new_chunk_file_path = os.path.join(dest_dir, f"chunk_{num_chunks}")
                current_chunk_file = open(new_chunk_file_path, "w")
            # write out the metadata and data lines to the chunk file
            try:
                # generate the metadata line and write to the current chunk file
                metadata = json.dumps(
                    {"index": {"_id": json.loads(raw_metadata)["index"]["_id"]}}
                )
                current_chunk_file.write(metadata + "\n")
                # generate the data line and write to the current chunk file
                data_json = json.loads(raw_data)
                data = json.dumps({key: data_json[key] for key in keys})
                current_chunk_file.write(data + "\n")
            except KeyError:
                logger.warn(f"Failed to parse document at line: {line_num}")
            line_num += 2
    # ensure final chunk in progress in closed
    if current_chunk_file:
        current_chunk_file.close()
    logger.info(f"Split dump file into {num_chunks} chunk file(s).")
