#!/usr/bin/env python3

import os
import subprocess
import sys
import urllib.request

from checkout import add_depot_tools_to_path

def main():
  add_depot_tools_to_path()

  subprocess.check_call([ sys.executable,
                          'src/build/util/lastchange.py',
                          '-o',
                          'src/build/util/LASTCHANGE' ])
  subprocess.check_call([ sys.executable,
                          'src/build/util/lastchange.py',
                          '-m', 'GPU_LISTS_VERSION',
                          '--revision-id-only',
                          '--header', 'src/gpu/config/gpu_lists_version.h' ])
  subprocess.check_call([ sys.executable,
                          'src/build/util/lastchange.py',
                          '-m', 'SKIA_COMMIT_HASH',
                          '-s', 'src/third_party/skia',
                          '--header', 'src/skia/ext/skia_commit_hash.h' ])
  subprocess.check_call([ sys.executable,
                          'src/build/util/lastchange.py',
                          '-s', 'src/third_party/dawn',
                          '--revision', 'src/gpu/webgpu/DAWN_VERSION' ])

if __name__ == '__main__':
  main()
