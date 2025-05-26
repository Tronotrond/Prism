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


from Prism_PrismZiFlowIntegration_Variables import Prism_PrismZiFlowIntegration_Variables
from Prism_PrismZiFlowIntegration_Functions import Prism_PrismZiFlowIntegration_Functions


class PrismZiFlowIntegration(Prism_PrismZiFlowIntegration_Variables, Prism_PrismZiFlowIntegration_Functions):
    def __init__(self, core):
        Prism_PluginEmpty_Variables.__init__(self, core, self)
        Prism_PluginEmpty_Functions.__init__(self, core, self)
        
        self.ziflow_api_url = "https://api.ziflow.com/v1/proofs"
        self.ziflow_api_key = "your_api_key_here"  # Replace with your ZiFlow API key
        
        
        
    def send_to_ziflow(self, file_paths, project_name, file_version):
        """
        Sends files to ZiFlow for proof creation.
        
        :param file_paths: List of file paths to be sent.
        :param project_name: Name of the project (used for proof name).
        :param file_version: Version of the files.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.ziflow_api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare the payload
            payload = {
                "name": f"{project_name} - {file_version}",
                "description": f"Proof created for {project_name} version {file_version}.",
                "files": [
                    {"path": file_path} for file_path in file_paths
                ],
                "reviewers": [],  # Add reviewers if needed
            }

            # Send the request
            response = requests.post(self.ziflow_api_url, headers=headers, json=payload)
            response_data = response.json()

            if response.status_code == 201:  # Success
                self.core.popup(f"Proof created successfully in ZiFlow! Proof ID: {response_data['id']}")
            else:
                # Handle errors
                error_message = response_data.get("message", "Unknown error")
                self.core.popup(f"Error creating proof in ZiFlow: {error_message}")
        
        except Exception as e:
            self.core.popup(f"An error occurred while sending to ZiFlow: {str(e)}")