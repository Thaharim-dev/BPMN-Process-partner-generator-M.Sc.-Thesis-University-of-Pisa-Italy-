#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import xml.etree.ElementTree as ET
import argparse
import zipfile
import os

def process_bpmn_file(input_file_name, output_zip_file):
    tree = ET.parse(input_file_name)
    root = tree.getroot()

    # Create a dictionary to track the old-to-new element mapping
    element_mapping = {}

    for element in root.iter():
        # Check if the element is a task (sendTask or receiveTask) or a gateway
        if "sendTask" in element.tag or "receiveTask" in element.tag:
            # Handle task element replacement
            new_tag = element.tag.replace("sendTask", "receiveTask").replace("receiveTask", "sendTask")
            element.tag = new_tag
            element_mapping[element.get("id")] = element

        elif "exclusiveGateway" in element.tag or "eventBasedGateway" in element.tag:
            # Handle gateway element replacement
            new_tag = element.tag.replace("exclusiveGateway", "eventBasedGateway").replace("eventBasedGateway", "exclusiveGateway")
            element.tag = new_tag
            element_mapping[element.get("id")] = element

    # Update sequence flows with the new references
    for element in root.iter():
        if element.tag == "sequenceFlow":
            source_ref = element.get("sourceRef")
            target_ref = element.get("targetRef")
            if source_ref in element_mapping and target_ref in element_mapping:
                element.set("sourceRef", element_mapping[source_ref].get("id"))
                element.set("targetRef", element_mapping[target_ref].get("id"))

    # Manually replace the namespaces in the root element's tag
    root.tag = root.tag.replace('ns0:', 'bpmn:').replace('ns2:', 'bpmndi:').replace('ns3:', 'dc:').replace('ns4:', 'di:')

    # Write the modified content to a new file
    output_file_name = input_file_name.replace(".bpmn", "_modified.bpmn")
    tree.write(output_file_name, encoding='utf-8', xml_declaration=True)

    # Add the modified file to the output zip file
    output_zip_file.write(output_file_name, os.path.basename(output_file_name))
    
    # Clean up the temporary modified file
    os.remove(output_file_name)

def process_zip_files(zip_file_name, output_zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'r') as input_zip_file:
        with zipfile.ZipFile(output_zip_file_name, 'w') as output_zip_file:
            for file_name in input_zip_file.namelist():
                with input_zip_file.open(file_name) as input_file:
                    # Process each BPMN file in the zip
                    process_bpmn_file(input_file, output_zip_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process BPMN files in a zip archive and generate new zip archive.")
    parser.add_argument("input_zip", help="Input zip file containing BPMN files")
    parser.add_argument("output_zip", help="Output zip file for modified BPMN files")
    args = parser.parse_args()

    process_zip_files(args.input_zip, args.output_zip)

