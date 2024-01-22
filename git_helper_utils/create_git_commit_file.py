"""Create a git commit file."""
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


# https://www.conventionalcommits.org/en/v1.0.0/
commit_type_lookup = {
    "feat": "A new feature for the user.",
    "fix": "A bug fix.",
    "chore": "Routine tasks, maintenance, and other non-user-facing changes.",
    "docs": "Documentation changes.",
    "style": "Code style changes (formatting, indentation).",
    "refactor": "Code refactoring.",
    "test": "Adding or modifying tests.",
    "ci": "Changes to the project's CI/CD configuration."
}

DEFAULT_PROJECT = "git-helper-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))

DEFAULT_COMMIT_TYPES = [commit_type for commit_type in commit_type_lookup.keys()]

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


def get_desc_from_user() -> str:
    """Prompt the user for a description.

    Returns:
        str: The description.
    """
    desc = input("Please provide a description for the commit (type 'done' when finished)\n")
    return desc


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
@click.option('--comment', help="Optional: A one line comment.")
@click.option('--issue_id', help="Optional: The issue identifier.")
@click.option('--logfile', help="Optional: The log file.")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'.")
@click.option('--outfile', help="Optional: The output commit comment file.")
@click.option('--scope', help="Optional: Describes the module, component, or section of the project that is affected by the commit.")
@click.option('--commit_type', type=click.Choice(DEFAULT_COMMIT_TYPES), help="Optional: Describes the purpose of the commit.")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(comment: Optional[str], issue_id: Optional[str], logfile: Optional[str], outdir: Optional[str], outfile: Optional[str], scope: Optional[str], commit_type: Optional[str], verbose: Optional[bool]):
    """Create a git commit file.

    Args:
        comment (Optional[str]): A one line comment.
        issue_id (Optional[str]): The issue identifier.
        logfile (Optional[str]): The log file.
        outdir (Optional[str]): The output directory.
        outfile (Optional[str]): The output commit comment file.
        scope (Optional[str]): Describes the module, component, or section of the project that is affected by the commit.
        commit_type (Optional[str]): Describes the purpose of the commit.
        verbose (Optional[bool]): Will print more info to STDOUT.
    """
    error_ctr = 0

    if error_ctr > 0:
        print_red("Required command-line arguments were not provided")
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

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

    if outfile is None:
        outfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.txt'
        )
        print_yellow(f"--outfile was not specified and therefore was set to '{outfile}'")

    if verbose is None:
        verbose = DEFAULT_VERBOSE
        print_yellow(f"--verbose was not specified and therefore was set to '{verbose}'")


    while commit_type is None or commit_type == "" or commit_type.lower().strip() not in DEFAULT_COMMIT_TYPES:
        print("\n")
        for commit_type in DEFAULT_COMMIT_TYPES:
            console.print(f"[bold blue]{commit_type}[/] - {commit_type_lookup[commit_type]}")
        commit_type = click.prompt("Please enter the type of commit", type=str)

    if scope is None or scope == "":
        scope = input("Please enter the scope of the commit [just press Enter if none]: ")
        if scope is None or scope == "":
            scope = None

    while comment is None or comment == "":
        comment = click.prompt("Please enter a one-line comment", type=str)

    if issue_id is None or issue_id == "":
        issue_id = click.prompt("Please enter the issue identifier [Enter if none]", type=str)
        if issue_id is None or issue_id == "":
            issue_id = None
        else:
            issue_id = issue_id.strip()
    else:
        issue_id = issue_id.strip()

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    ans = input("Do you want to provide more details? [Y/n]:")
    desc = None
    if ans is None or ans == "" or ans.lower() == "y":
        desc = get_desc_from_user()

    outline = None
    if scope is not None:
        outline = f"{commit_type}({scope}): {comment}"
    else:
        outline = f"{commit_type}: {comment}"

    with open(outfile, 'w') as of:

        of.write(f"{outline}\n\n")
        if desc is not None and desc != "":
            of.write(f"{desc}\n\n")
        if issue_id is not None and issue_id != "":
            of.write(f"{issue_id}\n")

    logging.info(f"Wrote commit comment file '{outfile}'")


    if verbose:
        console.print(f"\nWrote commit comment file '{outfile}'")
        console.print(f"\nThe log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")
    sys.exit(0)

if __name__ == "__main__":
    main()

