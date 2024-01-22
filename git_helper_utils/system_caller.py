import logging
import os
import subprocess

from rich.console import Console

console = Console()


DEFAULT_VERBOSE = False


def execute_cmd(
    cmd: str,
    outdir: str = None,
    stdout_file: str = None,
    stderr_file: str = None,
    verbose: bool = DEFAULT_VERBOSE,
) -> str:
    """Execute a command via system call using the subprocess module.

    Args:
        cmd (str): The executable to be invoked.
        outdir (str): The output directory where STDOUT, STDERR and the shell script should be written to.
        stdout_file (str): The file to which STDOUT will be captured in.
        stderr_file (str): The file to which STDERR will be captured in.
    Returns:
        str: The STDOUT file.
    """
    if cmd is None:
        raise Exception("cmd was not specified")

    cmd = cmd.strip()

    logging.info(f"Will attempt to execute '{cmd}'")
    if verbose:
        console.print(f"Will attempt to execute '{cmd}'")

    if outdir is None:
        outdir = "/tmp"
        logging.info(
            f"outdir was not defined and therefore was set to default '{outdir}'"
        )

    if stdout_file is None:
        primary = cmd.split(" ")[0]
        basename = os.path.basename(primary)
        stdout_file = os.path.join(outdir, basename + ".stdout")
        logging.info(
            f"stdout_file was not specified and therefore was set to '{stdout_file}'"
        )

    if stderr_file is None:
        primary = cmd.split(" ")[0]
        basename = os.path.basename(primary)
        stderr_file = os.path.join(outdir, basename + ".stderr")
        logging.info(
            f"stderr_file was not specified and therefore was set to '{stderr_file}'"
        )

    if os.path.exists(stdout_file):
        logging.info(
            f"STDOUT file '{stdout_file}' already exists so will delete it now"
        )
        os.remove(stdout_file)

    if os.path.exists(stderr_file):
        logging.info(
            f"STDERR file '{stderr_file}' already exists so will delete it now"
        )
        os.remove(stderr_file)

    consolidated_cmd = cmd
    p = subprocess.Popen(consolidated_cmd, shell=True)

    (stdout, stderr) = p.communicate()

    pid = p.pid

    logging.info(f"The child process ID is '{pid}'")
    if verbose:
        print(f"The child process ID is '{pid}'")

    p_status = p.wait()

    p_returncode = p.returncode

    if p_returncode is not None:
        logging.info(f"The return code was '{p_returncode}'")
    else:
        logging.info("There was no return code")

    if p_status == 0:
        logging.info(f"Execution of cmd '{cmd}' has completed")
    else:
        raise Exception(f"Received status '{p_status}'")

    if stdout is not None:
        logging.info("stdout is: " + stdout_file)

    if stderr is not None:
        logging.info("stderr is: " + stderr_file)

    return stdout_file

