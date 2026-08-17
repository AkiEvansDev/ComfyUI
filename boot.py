"""Launcher that stops CUDA from busy-waiting, then hands over to main.py.

A thread waiting on the GPU spins by default and burns a full core for the whole of a sampling run -
about 36 core-seconds per generation, producing nothing but heat. cudaDeviceScheduleBlockingSync makes
it sleep on an interrupt instead. Measured on this machine: large kernels get slightly faster and cost
no CPU at all, while a pathological pattern of tiny kernels synced one by one gets twice as slow, which
is not what a diffusion sampler does.

The flag has to be set before the CUDA context exists, which is why this runs ahead of main.py rather
than from a custom node. Nothing here may import torch: main.py deliberately probes the torch version
without importing it, so that cuda_malloc can set its allocator env vars first.
"""

import ctypes
import glob
import importlib.util
import os
import runpy
import sys

CUDA_DEVICE_SCHEDULE_BLOCKING_SYNC = 0x04
ROOT = os.path.dirname(os.path.realpath(__file__))


def main() -> None:
    _set_blocking_sync()

    # main.py reads sys.argv the way argparse expects, and wants to believe it was started directly.
    sys.argv[0] = os.path.join(ROOT, "main.py")
    runpy.run_path(sys.argv[0], run_name="__main__")


def _set_blocking_sync() -> None:
    """Never fatal: a machine without CUDA, or a torch that moved its runtime, just keeps the default."""
    library = _cuda_runtime_path()
    if library is None:
        print("[boot] cuda runtime not found, leaving the sync policy alone.")
        return

    try:
        result = ctypes.CDLL(library).cudaSetDeviceFlags(ctypes.c_uint(CUDA_DEVICE_SCHEDULE_BLOCKING_SYNC))
    except (OSError, AttributeError) as error:
        print(f"[boot] could not set the cuda sync policy: {error}")
        return

    name = os.path.basename(library)
    if result == 0:
        print(f"[boot] cuda blocking sync enabled through {name}, the sampler will not busy-wait.")
    else:
        print(f"[boot] {name} refused the blocking sync flag (cudaError {result}), keeping the default.")


def _cuda_runtime_path() -> str | None:
    # find_spec locates torch without executing it, which is the whole point of doing this here.
    spec = importlib.util.find_spec("torch")
    if spec is None or not spec.submodule_search_locations:
        return None

    found = glob.glob(os.path.join(spec.submodule_search_locations[0], "lib", "cudart64_*.dll"))
    return found[0] if found else None


if __name__ == "__main__":
    main()
