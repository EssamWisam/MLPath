'''
This is the CLI for the mlpath package. Includes commands to create a new project
'''
# pylint: skip-file

import click
import os
import shutil
import pkg_resources
from mlpath.mldir_cli.web.app import run_server

# if a name is provided make the directory with that name
@click.command()
@click.option('--name', default='Project', help='The name of the project')
@click.option('--full', default=False, is_flag=True, help='A simpler project directory will be created if this flag is set')
@click.option('--example', default=False, is_flag=True, help='A simple example project will be created if this flag is set')
@click.option('--force', default=False, is_flag=True, help='If a project with the same name exists it will be deleted and a new one will be created')
def main(name, full, example, force):
    if example:
        folder_name = 'example-project'
    elif full:
        folder_name = 'project'
    else:
        folder_name = 'simple-project'

    try:
        folder_path = pkg_resources.resource_filename(__name__, f"/{folder_name}")
        if os.path.exists(name):
            if force:
                shutil.rmtree(name)
            else:
                click.echo("Couldn't create project. A project with that name already exists. Use the --force flag to overwrite the existing project")
                return
            
        # copy the folder 
        shutil.copytree(folder_path, f'./{folder_name}')
        click.echo('Project created successfully')
        
    except Exception as e:
        click.echo('Project creation failed')
        click.echo(e)


@click.command()
def web():
    try:         
        # run the command to go into the directory 'Quest-Web' and run 'python app.py
        #os.system('cd Quests-Web && python -m flask run')
        run_server()
        click.echo('Web interface created successfully')
    except Exception as e:
        click.echo('Quests-Web creation failed')
        click.echo(e)
