from invoke import task


@task
def runtests(ctx):
    """
    Runs pytest, pyflakes, and pep8.
    """
    ctx.run('pytest -s', pty=True)
    ctx.run('pyflakes .', pty=True)
    ctx.run('pep8 --ignore E265,E266,E501 .', pty=True)
