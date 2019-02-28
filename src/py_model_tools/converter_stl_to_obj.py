#! /usr/bin/python

from os import path
import os
import argparse
import subprocess
import time
import rospkg
import glob


def run_process_and_wait(cmd):
    """
    Create an instance of the geptto-gui
    """
    process = subprocess.Popen(cmd, shell=True)
    process.wait()


def convert_stl_to_obj(stl_file, obj_file):
    """
    Prepare the instruction to convert 1 stl file into 1 obj+mtl
    """
    cmd = "blender --background --python "
    cmd += path.join( rospkg.RosPack().get_path("model_tools"),
                      "src", "py_model_tools", "stl_to_obj_blender.py")
    cmd += " -- "
    cmd += stl_file
    cmd += " "
    cmd += obj_file
    print (cmd)
    run_process_and_wait(cmd)


def mkdir_recursive(path):
    sub_path = os.path.dirname(path)
    if not os.path.isdir(sub_path):
        if sub_path != '':
            mkdir_recursive(sub_path)
    if not os.path.isdir(path):
        os.mkdir(path)


def get_the_files(input_stl_dir, output_obj_dir):
    stl_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".stl"):
                stl_file = os.path.abspath(os.path.join(root, file))
                assert os.path.exists(stl_file)
                stl_files += [stl_file]
    
    current_folder = os.getcwd()
    os.chdir(input_stl_dir)
    obj_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".stl"):
                obj_file = os.path.join(output_obj_dir, root, file)
                obj_file = os.path.splitext(obj_file)[0]+'.obj'
                obj_files += [obj_file]
    os.chdir(current_folder)

    if stl_files:
        print ("detected stl files.")
        for stl_file in stl_files:
            print ("    - " , stl_file)
    else:
        print ("No stl files detected.")

    if obj_files:
        print ("ouput obj files.")
        for obj_file in obj_files:
            print ("    - " , obj_file)
    else:
        print ("No obj files output.")

    assert len(stl_files) == len(obj_files)

    return stl_files, obj_files


def manage_arguments(args):
    """
    Extract the names of the stl files from the input dir. And recreate the
    architecture of folder in the destination folder.
    """
    
    if not os.path.isdir(args.input_stl_dir):
        raise IOError("Wrong path given for the stl folder:",
                      args.input_stl_dir)

    if args.output_obj_dir is not None:
        if args.output_obj_dir.startswith('/'):
            raise IOError("Wrong path given for the obj folder, it *MUST* a "
                          "local path. Path given: ", args.output_obj_dir)

    return (args.input_stl_dir, args.output_obj_dir)

def launcher(sys_args):
    """
    Function to convert a bunch of stl files in obj+mtl files
    """

    parser = argparse.ArgumentParser(description="Convert stl files in obj+mtl")
    requiredNamed = parser.add_argument_group('required named arguments')
    
    requiredNamed.add_argument(
      '-i', '--input_stl_dir', metavar='input_stl_dir', type=str,
      help='local path to the stl folder you want to convert', required=True)

    parser.add_argument(
      '-o', '--output_obj_dir', metavar='output_obj_dir',
      type=str, help='local path to the destination folder, this has to be an '
      'existing folder')

    args = parser.parse_args(sys_args)

    # manage the argument
    input_stl_dir, output_obj_dir = manage_arguments(args)

    # get the different paths
    stl_files, obj_files = get_the_files(input_stl_dir, output_obj_dir)

    # let us create the output dir
    mkdir_recursive(output_obj_dir)

    # now for each obj file we create the containing folder
    for obj_file in obj_files:
        mkdir_recursive(os.path.dirname(obj_file))

    # We then convert all stl in obj files
    for stl_file, obj_file in zip(stl_files, obj_files):
        convert_stl_to_obj(stl_file, obj_file)

    return True
