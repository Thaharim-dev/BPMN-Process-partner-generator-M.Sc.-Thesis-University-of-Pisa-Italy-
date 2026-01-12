# BPMN-Process-partner-generator-M.Sc.-Thesis-University-of-Pisa-Italy-
Given a single BPMN process, the idea is to generate the skeleton of a "dual" partner for it.  The idea is to create the skeleton of a "dual" partner for it. Roughly, send activities will correspond to receive activities, and vice versa, XOR-splits to event-based gateways, and every other element will be preserved. The theoretical part would consist of defining the concept of "dual". The main practical difficulty is to find some libraries to parse and write .bpmn files, as otherwise they must be implemented 


# Motivation
The increasing adoption of BPMN for modelling collaborative business processes raises the problem of designing correct and compatible partner processes. Currently, partner processes are often constructed manually, which is error-prone and lacks formal guarantees of interaction correctness. This thesis addresses this issue by introducing the concept of a dual BPMN process, which can be automatically generated from a single BPMN model. The proposed approach ensures communication compatibility by construction and provides a formal foundation for partner process generation, while also tackling practical challenges related to BPMN model parsing and transformation.

**Given BPMN Diagram**

![Figure 14](https://github.com/user-attachments/assets/a958c0ba-ecc5-4ed7-834e-74df43f09f2a)

**Dual Partner of the Given BPMN Diagram**

![Figure 15](https://github.com/user-attachments/assets/ea168847-f072-4ab0-bf1b-e9abfd4646a9)



# Instructions for setting up the library (locally):
**1. Keep this "my_bpmn_library" folder in a feasible place where all the code can be easily managed** 
 
**2. Install setuptools and wheel (if not already installed):**
 
 ```command ``` 
 ```"pip install setuptools wheel"```

**3. Create a Source Distribution:**

Open a command prompt or terminal, navigate to the root directory of the project (my_bpmn_library),where the setup.py file is located. For example, if you have your project in the                               ``` "/path/to/development/my_bpmn_library/ "```
directory, use the   ```"cd"```  command to navigate to that directory, and run the following command to create a source distribution with the command :
 
```command ``` 
```"python setup.py sdist"```

This will generate a dist directory containing a source distribution of your package.


**4. Create a Wheel Distribution:**

To create a wheel distribution (a binary distribution that can be installed faster), run the following command:

```command``` 
```"python setup.py bdist_wheel"```


**5. Distribute Package:**

Install the package locally for testing by running the following command in the project's root directory:

```command``` 
```"pip install ."```


**6. open a Python script in the same directory where the library is** 

Then the following code should be used for parsing the library 

```code :```

```
from my_bpmn_package.bpmn_transform import process_bpmn_file
input_file_name = "path/to/your/diagram.bpmn"
process_bpmn_file(input_file_name)
```
