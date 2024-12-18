#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEPOT_TOOLS_PATH = os.path.join(ROOT_DIR, 'vendor', 'depot_tools')
SRC_URL = 'https://chromium.googlesource.com/chromium/src.git'

sys.path.append(DEPOT_TOOLS_PATH)
from gclient import GClient, OptionParser

def add_depot_tools_to_path():
  os.environ['DEPOT_TOOLS_UPDATE'] = '0'
  os.environ['PATH'] = DEPOT_TOOLS_PATH + os.pathsep + os.environ['PATH']

def main():
  parser = argparse.ArgumentParser(description='Checkout Chromium source code')
  parser.add_argument('--revision', help='The revision to checkout')
  args = parser.parse_args()

  if os.path.exists('src'):
    print('The src dir already exists.')
    return 1

  add_depot_tools_to_path()

  # Write .gclient file.
  if args.revision:
    src = f'{SRC_URL}@{args.revision}'
  else:
    src = SRC_URL
  subprocess.check_call([ 'gclient', 'config', '--name', 'src', src ])
  with open(os.path.join('.gclient'), 'a') as f:
    f.write('target_os = [ "linux", "mac", "win" ]\n')

  # The cipd/gcs deps do not work with multi-os sync.
  ignore_deps = [ 'cipd', 'gcs' ]

  # Parse options like gclient.
  parser = OptionParser()
  parser.add_option('--no-history', action='store_true', default=True)
  parser.add_option('--nohooks', action='store_true', default=True)
  parser.add_option('--patch-refs', action='append', default=[])
  parser.add_option('--ignore-dep-type', action='append', default=ignore_deps)
  options, remaining_args = parser.parse_args([])

  # Checkout code.
  client = GClient.LoadCurrentConfig(options)
  ret = client.RunOnDeps('update', remaining_args)

  # Execute some necessary hook steps.
  subprocess.check_call([ sys.executable,
                          os.path.join(ROOT_DIR, 'run_hooks.py') ])
  return ret

if __name__ == '__main__':
  sys.exit(main())
