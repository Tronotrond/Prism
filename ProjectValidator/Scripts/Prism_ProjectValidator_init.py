# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


from Prism_ProjectValidator_Variables import Prism_ProjectValidator_Variables
from Prism_ProjectValidator_Functions import Prism_ProjectValidator_Functions
import os
import shutil
#import PrismInit
#import hou
'''
try:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
except:
    from PySide5.QtCore import *
    from PySide5.QtGui import *
    from PySide5.QtWidgets import *
'''

class Prism_ProjectValidator(Prism_ProjectValidator_Variables, Prism_ProjectValidator_Functions):
    # Class-level dictionary for directory definitions
    directories = {
        "drafts": "05_Drafts",
        "finals": "06_Deliveries",
    }

    def __init__(self, core):
        self.version = "v1.0.0"
        self.core = core
        
        Prism_ProjectValidator_Variables.__init__(self, core, self)
        Prism_ProjectValidator_Functions.__init__(self, core, self)
        
        # Setup callbacks
        #self.core.registerCallback("onProjectCreated", self.onProjectCreated, plugin=self)
        self.core.registerCallback("onProjectChanged", self.onProjectCreated, plugin=self)
        self.core.registerCallback("postSaveScene", self.onSceneChange, plugin=self)
        #self.core.registerCallback("sceneSaved", self.onSceneChange, plugin=self)
        self.core.registerCallback("onSceneOpen", self.onSceneChange, plugin=self)
        # Right click media version window
        self.core.registerCallback("openPBListContextMenu", self.openPBListContextMenu, plugin=self.plugin)
        # Right click media thumbnail/player
        self.core.registerCallback("mediaPlayerContextMenuRequested", self.openMediaPlayerContextMenu, plugin=self.plugin)
        # Project Created config callback
        self.core.registerCallback("onProjectCreated", self.onProjectCreated, plugin=self.plugin)


    
    # Media/versions right click context menu -- adding additional right click options
    def openPBListContextMenu(self, origin, menu, widget, item, path):
        if widget != origin.lw_version:
            return
 
        if not item:
            return

        #data = item.data(Qt.UserRole)
        data = item.text()
        
        # Add "Send to:" submenu
        send_to_menu = menu.addMenu("Send to:")
        drafts_action = send_to_menu.addAction("Drafts")
        finals_action = send_to_menu.addAction("Finals")
        
        drafts_action.triggered.connect(lambda: self.send_to_action_triggered(data, "drafts"))
        finals_action.triggered.connect(lambda: self.send_to_action_triggered(data, "finals"))
        
        #test_action = menu.addAction("Simple Test")
        #test_action.triggered.connect(lambda: self.core.popup("Simple Test action triggered"))
     
     
    def openMediaPlayerContextMenu(self, *args, **kwargs):
            
        #item = kwargs['item']
        #menu = kwargs['menu']
        if hasattr(args[0], 'getMediaFilesFromContext'):
            result = args[0].getMediaFilesFromContext
            import inspect
            if result:
                return
                #self.core.popup(dir(result))
                #self.core.popup(inspect.getdoc(result))

        '''       
        if hasattr(args[0], 'getMediaFilesFromContext'):
            path = args[0].getMediaFilesFromContext
            self.core.popup(path)
        if hasattr(args[0], 'getFilesFromContext'):
            path = args[0].getFilesFromContext
            self.core.popup(path)
        '''
        #self.core.popup(kwargs)
        #send_to_menu = menu.addMenu("Send to:")
        
        #data = item.text()
        
        # Add "Send to:" submenu
        #send_to_menu = menu.addMenu("Send to:")
        #drafts_action = send_to_menu.addAction("Drafts")
        #finals_action = send_to_menu.addAction("Finals")
     
     
        #drafts_action.triggered.connect(lambda: self.send_to_action_triggered(data, "drafts"))
        #finals_action.triggered.connect(lambda: self.send_to_action_triggered(data, "finals"))
        
       
    def send_to_action_triggered(self, data, destination):
        project_path = self.core.projectPath
        #self.core.popup(self.directories.get('drafts'))
         
        if destination == 'drafts':
            project_path += '\\' + self.directories.get('drafts') + '\\'
        elif destination == 'finals':
            project_path += '\\' + self.directories.get('finals') + '\\'
        else: 
            return
        
        prjdict = self.core.pb.mediaBrowser.getCurrentIdentifier()
        #self.core.popup(data)
        
        try:
            path = prjdict['path'] + r'\\' + data
        except:
            self.core.popup('An error occured in "send_to_action_triggered()')
            
        #self.core.popup(f"Sent '{path}' to {destination}")
        self.copy_files_with_subfolders(path, project_path, flat_hierarchy=True)

    
    def onProjectCreated(self, *args):
        #print('Project Validator Plugin Test')
        attr = dir(self.core)
        project_path = self.core.projectPath        
        
        # Set Project Config
        config = self.core.configs.getProjectConfigPath(project_path)
        #self.core.popup("Loading prj config")
        self.core.setConfig("houdini", "useRelativePaths", True, configPath=config)
        self.core.setConfig("usd", "createUsdLayers", False, configPath=config)
        self.core.setConfig("usd", "useRelativePaths", True, configPath=config)  
  
        
        #print(self.core.projectName)
        #print(self.core.projectPath)
        #projectSettings = self.core.GetProjectSettings()
        
        #if projectSettings["Paths"]["UseRelativePaths"] is not True:
        #    print('Project Relative Paths not enabled. Enabling now...')
        #    projectSettings["Paths"]["UseRelativePaths"] = True
        
        # Create each directory if it doesn't exist
        for key, dir_name in self.directories.items():
            dir_path = os.path.join(project_path, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"Created directory: {dir_path}")
            #else:
            #    print(f"Directory already exists: {dir_path}")
        
    def onSceneChange(self, *args):
        #core = PrismInit.pcore
        #core = self.core
        #print('onHoudiniSceneChange callback called')
        
        if self.core.appPlugin.pluginName == "Houdini":
            #print('File saved in Houdini!')
            import hou
            
            #prism_job = hou.getenv('PRISMJOB')
            prism_job = self.core.projectPath
            
            prism_job = prism_job.replace('\\\\', '/')
            prism_job = prism_job.replace('\\', '/')

            if prism_job[-1] == '/':
                prism_job = prism_job[:-1]
                
            
            if not prism_job:
                print('Prism Project not set up')
                return
       
            
            filename = self.core.getCurrentFileName()
            entity = self.core.getScenefileData(filename)
            
            if 'type' not in entity.keys():
                #Not a prism type file/shot
                return
                
            hou.unsetenv('JOB')
            hou.unsetenv('PRJ')
            hou.unsetenv('CACHE')
            
            hou.hscript('setenv JOB = replaceme')
            hou.hscript('setenv PRJ = replaceme')
            hou.hscript('setenv CACHE = replaceme')
            
            prj_path = entity['project_path']
            job_name = prj_path.split('\\')[-1]
            
            #print('Loading Prism project: ' + job_name)
            
            hou.putenv('PRJ', job_name)
            hou.putenv('JOB', prj_path)

            cache_dir = hou.getenv('SIM') + '/' + job_name
            hou.putenv('CACHE', cache_dir)
            
                
            # Lets make sure it's a shot before proceeding with the path mappings
            if entity['type'] != 'shot':
                return
            
            #job_name = prism_job.split('/')[-1]
            prism_type = entity['type']
            vers = entity['version']
            seq = entity['sequence']
            shot = entity['shot']
            
            
            
            #GENERATE VARIABLES IN SCENE - Required if they don't already exsists
            
            hou.hscript('setenv OUT = replaceme')
            hou.hscript('setenv USD = replaceme')

            #Build Prism specific OUT variable
            pre_path = r'03_Production/Shots'
            sc = hou.getenv('PRISM_SEQUENCE')
            sh = hou.getenv('PRISM_SHOT')
            
            # FIX THIS LATER
            if sc == None:
                sc = ""
            if sh == None:
                sh = ""
                
            
            #Build USD Cache Path
            usd_dir = cache_dir + '/usd/' + sc + '/' + sh
            hou.putenv('USD', usd_dir)
            
            # If sc is None, we're probably working on an asset - To be implemented better
            if sc == None:
                sc = ""
                sh = ""
                pre_path = r'03_Production'
                sc = "Assets"
                sh = hou.getenv('PRISM_ASSETPATH')
                if sh == None:
                    print('No PRISM_SEQUENCE or PRISM_ASSETPATH variables found...')
                    sh = ""
                    sc = ""
            
            post_path = r'Renders/3dRender/'
            
            # Identifier is what creates the media dropdown list in Prism
            identifier = 'beauty'
            
            out_path = prism_job + '/' + pre_path + '/' + sc + '/' + sh + '/' + post_path + seq + '_' + shot + '/' + vers + '/' + identifier + '/'
            out_img = out_path + seq + '_' + shot + '_' + vers + '.$F4.exr'
            #error checking to make sure we made the correct Prism path
            #if not os.path.isdir(out_path):
            #    print('$OUT path does not exist! Possible project config error...')
                
            # ADD HIPNAME to OUT path
            #out_path = out_path + hou.getenv('HIPNAME')
            hou.putenv('OUT', out_path) 
            
            hou.setContextOption("prism_render", out_img)
            hou.setContextOption("usd_asset", hou.getenv('ASSETS') + '/Models/USD/')
            hou.setContextOption("local_usd_asset", prism_job + '/3_Prod/Assets/2_USD/')
            hou.setContextOption("usd_scene", cache_dir + '/usd/render/')
        
        
    def copy_files_with_subfolders(self, source_dir, destination_dir, flat_hierarchy=False):
        """
        Copies files from the source to the destination directory, optionally flattening the hierarchy.
        Shows a popup confirmation with the number of files copied when done.
        Prompts the user before overwriting any files.
        """
        if not os.path.exists(source_dir):
            self.core.popup(f"Source directory does not exist: {source_dir}")
            return

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            print(f"Created destination directory: {destination_dir}")

        file_count = 0  # Counter for files copied

        try:
            # Traverse the source directory
            for root, _, files in os.walk(source_dir):
                for file_name in files:
                    src_file_path = os.path.join(root, file_name)
                    if flat_hierarchy:
                        # Flatten hierarchy: Place all files directly in the destination
                        dest_file_path = os.path.join(destination_dir, file_name)
                    else:
                        # Preserve hierarchy: Recreate folder structure in the destination
                        relative_path = os.path.relpath(root, source_dir)
                        dest_file_path = os.path.join(destination_dir, relative_path, file_name)

                        # Create destination subdirectory if necessary
                        dest_dir = os.path.dirname(dest_file_path)
                        if not os.path.exists(dest_dir):
                            os.makedirs(dest_dir)

                    # Check for overwriting
                    if os.path.exists(dest_file_path):
                        self.core.popup(f"File {file_name} already exists in the destination. Skipping...")
                        continue

                    # Copy the file
                    shutil.copy2(src_file_path, dest_file_path)  # Preserve metadata
                    #print(f"Copied: {src_file_path} -> {dest_file_path}")
                    file_count += 1

            # Show popup confirmation with the number of files copied
            self.core.popup(f"Copy completed successfully! Total files copied: {file_count}")

        except Exception as e:
            self.core.popup(f"An error occurred while copying: {str(e)}")