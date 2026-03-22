#!/usr/bin/env python3
import logging
import os
import shutil
import tarfile
import tempfile
import zipfile

import py7zr
import rarfile

START_ARCHIVE = '00114021.tar'
OUTPUT_DIR = '/tmp/out'

# Supported archive extensions
ARCHIVE_EXTENSIONS = ('.zip', '.tar', '.rar', '.7z')

os.makedirs(OUTPUT_DIR, exist_ok=True)


def is_archive(filename):
    return filename.lower().endswith(ARCHIVE_EXTENSIONS)


def extract_archive(filepath, extract_to):
    if filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as zf:
            zf.extractall(extract_to)
    elif filepath.endswith('.tar'):
        with tarfile.open(filepath, 'r:*') as tf:
            tf.extractall(extract_to, filter='tar')
    elif filepath.endswith('.rar'):
        with rarfile.RarFile(filepath) as rf:
            rf.extractall(extract_to)
    elif filepath.endswith('.7z'):
        with py7zr.SevenZipFile(filepath, mode='r') as z:
            z.extractall(extract_to)
    else:
        raise ValueError(f'Unsupported archive: {filepath}')


processed_archives = set()


def process_archive(filepath):
    abs_path = os.path.abspath(filepath)
    if abs_path in processed_archives:
        logging.warning('Skipping already processed archive: %s', filepath)
    else:
        logging.debug('Extracting archive: %s', filepath)
    processed_archives.add(abs_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            extract_archive(filepath, tmpdir)
        except Exception:
            logging.exception(f'Failed to extract {filepath}')
            return

        for root, _, files in os.walk(tmpdir):
            for name in files:
                full_path = os.path.join(root, name)
                logging.debug('Found file: %s', full_path)
                if is_archive(name):
                    logging.debug('Recursing into nested archive: %s', full_path)
                    process_archive(full_path)
                    print('.', end='', flush=True)
                else:
                    rel_path = os.path.relpath(full_path, tmpdir)
                    out_path = os.path.join(OUTPUT_DIR, rel_path)
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    logging.debug('Copying non-archive file to output: %s', out_path)
                    shutil.copy2(full_path, out_path)
                    print('+', end='', flush=True)


if __name__ == '__main__':
    process_archive(START_ARCHIVE)
    print()
