'''
This is the CLI for the mlpath package. Includes commands to create a new project
'''
# pylint: skip-file

import zipfile
import click
import os
import shutil
import pkg_resources

# if a name is provided make the directory with that name
@click.command()
@click.option('--name', default='Project', help='The name of the project')
@click.option('--full', default=False, is_flag=True, help='A simpler project directory will be created if this flag is set')
@click.option('--example', default=False, is_flag=True, help='A simple example project will be created if this flag is set')
def main(name, full, example):
    if example:
        zip_name = 'example-project'
    elif full:
        zip_name = 'project'
    else:
        zip_name = 'simple-project'

    try:
        zip_path = pkg_resources.resource_filename(__name__, f"/{zip_name}.zip")
        with zipfile.ZipFile(zip_path,"r") as zip_ref:
            zip_ref.extractall(name)
        click.echo('Project created successfully')
        
    except Exception as e:
        click.echo('Project creation failed')
        click.echo(e)


@click.command()
def web():
    try:
        zip_path = pkg_resources.resource_filename(__name__, f"/web.zip")
        with zipfile.ZipFile(zip_path,"r") as zip_ref:
            zip_ref.extractall('Quests-Web')
        # run the command to go into the directory 'Quest-Web' and run 'python app.py
        os.system('cd Quests-Web && python app.py')
        click.echo('Web interface created successfully')
    except Exception as e:
        click.echo('Quests-Web creation failed')
        click.echo(e)
