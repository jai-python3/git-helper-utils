"""Create a git branch."""
import click
import datetime
import logging
import os
import pathlib
import sys

from datetime import datetime

from rich.console import Console
from typing import Optional

from console_helper import print_green, print_yellow, print_red
from system_caller import execute_cmd


DEFAULT_PROJECT = "git-helper-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))

DEFAULT_VALID_TYPES = ["feature", "bugfix", "hotfix", "custom"]

DEFAULT_SOURCE_BRANCH = "development"

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.getenv('USER'),
    DEFAULT_PROJECT,
    os.path.splitext(os.path.basename(__file__))[0],
    DEFAULT_TIMESTAMP
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False

error_console = Console(stderr=True, style="bold red")

console = Console()


def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """

    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--desc', help="Required: A description to apply during the creation of the branch")
@click.option('--jira_id', help="Optional: The Jira ticket identifier")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--source_branch', help=f"Optional: The source branch to establish the new branch from - default is '{DEFAULT_SOURCE_BRANCH}'")
@click.option('--type', type=click.Choice(DEFAULT_VALID_TYPES), help="Required: The type of branch to establish")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'", callback=validate_verbose)
def main(desc: str, jira_id: Optional[str], logfile: Optional[str], outdir: Optional[str], source_branch: str, type: str, verbose: Optional[bool]):
    """Create a git branch.

    Args:
        desc (str): A description to apply during the creation of the branch.
        jira_id (Optional[str]): The Jira ticket identifier.
        logfile (Optional[str]): The log file.
        outdir (Optional[str]): The output directory.
        source_branch (str): The source branch to establish the new branch from.
        type (str): The type of branch to establish.
        verbose (Optional[bool]): Will print more info to STDOUT.
    """
    error_ctr = 0

    if desc is None:
        desc = click.prompt("Please enter a description for the branch", type=str)
        if desc is None or desc == "":
            print_red("--desc was not specified")
            error_ctr += 1

    while type is None or type not in DEFAULT_VALID_TYPES:
        type = click.prompt(f"Please enter the type of branch to establish (valid options: {DEFAULT_VALID_TYPES})", type=str)

    if error_ctr > 0:
        print_red("Required command-line arguments were not provided")
        click.echo(click.get_current_context().get_help())
        sys.exit(1)


    if source_branch is None:
        source_branch = input(f"Please provide the source branch (default is '{DEFAULT_SOURCE_BRANCH}'): ")
        if source_branch is None or source_branch == "":
            source_branch = DEFAULT_SOURCE_BRANCH
        source_branch = source_branch.strip()

    if jira_id is None:
        jira_id = input("Please enter the Jira ticket identifier or press ENTER to skip: ")
        if jira_id is None or jira_id == "":
            jira_id = None
        else:
            jira_id = jira_id.strip()

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        print_yellow(f"Created output directory '{outdir}'")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        print_yellow(f"--logfile was not specified and therefore was set to '{logfile}'")

    if verbose is None:
        verbose = DEFAULT_VERBOSE
        print_yellow(f"--verbose was not specified and therefore was set to '{verbose}'")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    timestamp = datetime.today().strftime('%Y-%m-%d-%H%M%S')

    new_branch = None

    if jira_id is None:
        new_branch = f"{type}/from-{source_branch}-on-{timestamp}-for-{desc.lower().replace(' ', '-')}"
    else:
        new_branch = f"{type}/{jira_id}-from-{source_branch}-on-{timestamp}-for-{desc.lower().replace(' ', '-')}"

    print(f"New branch: {new_branch}")

    execute_cmd(f"git checkout -b {new_branch}")

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")
    sys.exit(0)

if __name__ == "__main__":
    main()

