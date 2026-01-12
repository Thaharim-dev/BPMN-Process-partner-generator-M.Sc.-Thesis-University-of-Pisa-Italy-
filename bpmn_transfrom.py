import xml.etree.ElementTree as ET

def process_bpmn_file(input_file_name):
    tree = ET.parse(input_file_name)
    root = tree.getroot()

    # Create a dictionary to track the old-to-new element mapping
    element_mapping = {}

    # Step 1: Replace tasks
    for element in root.iter():
        if "sendTask" in element.tag:
            new_tag = element.tag.replace("sendTask", "receiveTask")
            element.tag = new_tag
            element_mapping[element.get("id")] = element
        elif "receiveTask" in element.tag:
            new_tag = element.tag.replace("receiveTask", "sendTask")
            element.tag = new_tag
            element_mapping[element.get("id")] = element

    # Step 2: Replace event-based gateways after task replacement
    for element in root.iter():
        if "eventBasedGateway" in element.tag:
            new_tag = element.tag.replace("eventBasedGateway", "exclusiveGateway")
            element.tag = new_tag
            element_mapping[element.get("id")] = element

    # Step 3: Replace message intermediate events
    for element in root.iter():
        if "intermediateCatchEvent" in element.tag:
            new_tag = element.tag.replace("intermediateCatchEvent", "intermediateThrowEvent")
            element.tag = new_tag
            element_mapping[element.get("id")] = element
        elif "intermediateThrowEvent" in element.tag:
            new_tag = element.tag.replace("intermediateThrowEvent", "intermediateCatchEvent")
            element.tag = new_tag
            element_mapping[element.get("id")] = element

    # Step 4: Remove DataObjectReference and DataStoreReference
    for data_object_ref in root.findall('.//{http://www.omg.org/spec/BPMN/20100524/MODEL}dataObjectReference'):
        parent_element = tree.find('.//{http://www.omg.org/spec/BPMN/20100524/MODEL}process')  # Assuming data objects are within the process
        if parent_element is not None and data_object_ref in parent_element:
            parent_element.remove(data_object_ref)

    for data_store_ref in root.findall('.//{http://www.omg.org/spec/BPMN/20100524/MODEL}dataStoreReference'):
        parent_element = tree.find('.//{http://www.omg.org/spec/BPMN/20100524/MODEL}process')  # Assuming data stores are within the process
        if parent_element is not None and data_store_ref in parent_element:
            parent_element.remove(data_store_ref)

    # Update sequence flows with the new references after replacements
    for element in root.iter():
        if element.tag == "sequenceFlow":
            source_ref = element.get("sourceRef")
            target_ref = element.get("targetRef")
            if source_ref in element_mapping and target_ref in element_mapping:
                element.set("sourceRef", element_mapping[source_ref].get("id"))
                element.set("targetRef", element_mapping[target_ref].get("id"))

    # Manually replace the namespaces in the root element's tag
    root.tag = root.tag.replace('ns0:', 'bpmn:').replace('ns2:', 'bpmndi:').replace('ns3:', 'dc:').replace('ns4:', 'di:')

    # Write the modified content to the output file
    tree.write(input_file_name.replace(".bpmn", "_modified.bpmn"), encoding='utf-8', xml_declaration=True)
