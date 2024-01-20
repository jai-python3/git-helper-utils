# git-helper-utils
Collection of Python utility scripts to facilitate git related tasks.

- [git-helper-utils](#git-helper-utils)
  - [Motivation](#motivation)
  - [Improvements](#improvements)
  - [Use Cases](#use-cases)
  - [Installation](#installation)
  - [Generate shell wrapper scripts](#generate-shell-wrapper-scripts)
  - [Exported scripts](#exported-scripts)
    - [create-git-branch](#create-git-branch)
    - [create-git-commit-file](#create-git-commit-file)
  - [Contributing](#contributing)
  - [To-Do/Coming Next](#to-docoming-next)
  - [CHANGELOG](#changelog)
  - [License](#license)



## Motivation

Explain what the motivation was for developing this package OR<br>
explain how this package was improved after being forked.


## Improvements

Please see the [TODO](TODO.md) for a list of upcoming improvements.


## Use Cases

<img src="use_cases.png" width="400" height="300" alt="Use Cases diagram">

## Installation

Please see the [INSTALL](INSTALL.md) guide for instructions.

## Generate shell wrapper scripts

After executing `pip install git-helper-utils`, execute this exported script: `make-git-helper-utils`.<br>
This will create the wrapper shell scripts and a file containing aliases named `git-helper-utils-aliases.txt` in the current directory.<br><br>
You can then add this line to your .bashrc or .zshrc:<br>
`source dir/git-helper-utils-aliases.txt`<br>
where dir is the directory that contains the aliases file.

## Exported scripts

The following exported scripts are available:

- create-git-branch
- create-git-commit-file


### create-git-branch

Sample invocation:

```shell
create-git-branch 
Please enter a description for the branch: add gene masking support
Please enter the type of branch to establish (valid options: ['feature', 'bugfix', 'hotfix', 'custom']): feature
Please provide the source branch (default is 'development'): main
Please enter the Jira ticket identifier or press ENTER to skip: BIO-2323
--outdir was not specified and therefore was set to '/tmp/git-helper-utils/create_git_branch/2023-12-30-224322'
Created output directory '/tmp/git-helper-utils/create_git_branch/2023-12-30-224322'
--logfile was not specified and therefore was set to 
'/tmp/git-helper-utils/create_git_branch/2023-12-30-224322/create_git_branch.log'
New branch: feature/BIO-2323-from-main-on-2023-12-30-224335-for-add-gene-masking-support
Switched to a new branch 'feature/BIO-2323-from-main-on-2023-12-30-224335-for-add-gene-masking-support'
The log file is '/tmp/git-helper-utils/create_git_branch/2023-12-30-224322/create_git_branch.log'
Execution of '/home/sundaram/projects/git-helper-utils/venv/lib/python3.10/site-packages/git_utils/create_git_branch.py' 
completed


git branch -a
* feature/BIO-2323-from-main-on-2023-12-30-224335-for-add-gene-masking-support
  main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```

### create-git-commit-file

Sample invocation:

```shell
python git_helper_utils/create_git_commit_file.py
--outdir was not specified and therefore was set to '/tmp/git-utils/create_git_commit_file/2023-12-31-144521'
Created output directory '/tmp/git-utils/create_git_commit_file/2023-12-31-144521'
--logfile was not specified and therefore was set to '/tmp/git-utils/create_git_commit_file/2023-12-31-144521/create_git_commit_file.log'
--outfile was not specified and therefore was set to '/tmp/git-utils/create_git_commit_file/2023-12-31-144521/create_git_commit_file.txt'


feat - A new feature for the user.
fix - A bug fix.
chore - Routine tasks, maintenance, and other non-user-facing changes.
docs - Documentation changes.
style - Code style changes (formatting, indentation).
refactor - Code refactoring.
test - Adding or modifying tests.
ci - Changes to the project's CI/CD configuration.
Please enter the type of commit: fix
Please enter the scope of the commit [just press Enter if none]: 
Please enter a one-line comment: FIXES bug in synth-bio component
Please enter the issue identifier [Enter if none]: GNSB-1225
Do you want to provide more details? [Y/n]:n

Wrote commit comment file '/tmp/git-utils/create_git_commit_file/2023-12-31-144521/create_git_commit_file.txt'

The log file is '/tmp/git-utils/create_git_commit_file/2023-12-31-144521/create_git_commit_file.log'
Execution of '/home/sundaram/projects/git-utils/git_helper_utils/create_git_commit_file.py' completed


cat /tmp/git-utils/create_git_commit_file/2023-12-31-144521/create_git_commit_file.txt
fix: FIXES bug in synth-bio component

GNSB-1225
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## To-Do/Coming Next

Please view the listing of planned improvements [here](TODO.md).

## CHANGELOG

Please view the CHANGELOG [here](CHANGELOG.md).

## License

[GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE)
