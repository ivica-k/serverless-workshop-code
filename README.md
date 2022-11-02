# serverless-workshop-code

This repository contains a working example application built on the 
[Building serverless applications with Python](https://ivica-k.github.io/serverless_python_workshop/) workshop.

To follow the workshop in a live setting:

1. Clone this repository `git clone git@github.com:ivica-k/serverless-workshop-code.git`
2. Follow the workshop [setup page](https://ivica-k.github.io/serverless_python_workshop/20-prerequisites/100-setup.html).

## Using code examples

The workshop itself is split into chapters and pages:

```
1.0 Donor sign-up
    1.1 First function
    1.2 AWS Lambda 101
    1.3 Donor sign-up
    1.4 Testing
...
3.0 Donation event
    3.1 One idea...
```

Each number visible above corresponds to a Git branch in this repository. If you want to grab the code until and including
`Testing` you can perform `git checkout 1.4`.

If you would like to grab the code for the whole first chapter you can perform `git checkout 2.0` - this includes all
the code examples up until chapter 2.0.

**Note**

Please note that some pages in the workshop do not contain code samples (such as `1.2 AWS Lambda 101`) and there will
be no branches for that page.

## Discarding changes

It is possible that changing branches with `git checkout BRANCH_NAME` will fail. That happens if you changed a file 
that contains changes in the branch you want to switch to, so `git` is unclear what to keep. To get around this you can:

 - move your changes to a temporary storage (stash them) with `git stash push -m "these changes are important"`.
This will create entry `0` in the temporary stash storage
```bash
$ git stash list
stash@{0}: On master: these changes are important
```
if you would like to get your changes back, you may do so with `git stash pop N` where `N` is the entry number
 - discard your changes to the file by executing `git checkout PATH_TO_CHANGED_FILE`. For example `git checkout savealife/app.py`
 - discard all changes with `git reset`

All configuration files (`*.json`) are *excluded* from `git` and discarding changes **will not** discard changes in 
configuration files.