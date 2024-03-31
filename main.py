import subprocess
import re
import xml.etree.ElementTree as ET
import difflib

import xml.dom.minidom
class Serializer:
    @staticmethod
    def serialize(command_manual, filename , option):

        # Create the CommandManual element
        command_element = ET.Element("CommandManual")

        # Create subelements for CommandName, CommandDescription, Version, Example, RelatedCommands, etc.
        ET.SubElement(command_element, 'CommandName').text = command_manual.command
        ET.SubElement(command_element, "CommandDescription").text = command_manual.description() or "No description found"
        ET.SubElement(command_element, "Version").text = command_manual.extract_version() or "No version found"
        ET.SubElement(command_element, "SyntaxAndUsagePatterns").text = command_manual.Syntax_Usage() or "No Syntax_Usage found"
        ET.SubElement(command_element, "Examples").text = command_manual.extract_examples() or 'No examples found'

        # Split the string of related commands into a list
       # related_commands_list = command_manual.related_commands().split(',') if command_manual.related_commands() else []
        # Convert the list of related commands to a string with each command enclosed in <>
       # related_commands_str = ', '.join(f'<{cmd.strip()}>' for cmd in related_commands_list) if related_commands_list else 'No Related Command'
        ET.SubElement(command_element, "RelatedCommand").text = command_manual.related_commands() or 'no related commad'
        #ET.SubElement(command_element, "RelatedCommand ").text=command_manual.related_commands()
        # related_command_element.text = self.related_commands() or 'No Related
        ET.SubElement(command_element, "OnlineDocumentationLink").text = command_manual.documentation_link()

        def prettify(element, indent='  '):# to make the xml more pretty
            queue = [(0, element)]  # (level, element)
            while queue:
                level, element = queue.pop(0)
                children = [(level + 1, child) for child in list(element)]
                if children:
                    element.text = '\n' + indent * (level + 1)  # for child open
                if queue:
                    element.tail = '\n' + indent * queue[0][0]  # for sibling open
                else:
                    element.tail = '\n' + indent * (level - 1)  # for parent close
                queue[0:0] = children  # prepend so children come before siblings

        prettify(command_element)
        # Create an ElementTree object
        tree = ET.ElementTree(command_element)

        if (option == 1):
            tree.write(f"{filename}_manual.xml", encoding='UTF-8', xml_declaration=True)
        else:
            tree.write(f"{filename}_Ver.xml", encoding='UTF-8', xml_declaration=True)


    @staticmethod
    def deserialize(filename):
        # Parse the XML file
        tree = ET.parse(filename)
        root = tree.getroot()

        # Extract data from XML and create a CommandManual object
        command_name = root.find('CommandName').text
        command_description = root.find('CommandDescription').text
        version = root.find('Version').text
        syntax_and_usage = root.find('SyntaxAndUsagePatterns').text
        examples = root.find('Examples').text
        related_commands = root.find('RelatedCommand').text
        online_doc_link = root.find('OnlineDocumentationLink').text

        # Create a CommandManual object
        command_manual = commandManual(command_name)
        command_manual.set_description(command_description)
        command_manual.set_version(version)
        command_manual.set_syntax_and_usage(syntax_and_usage)
        command_manual.set_examples(examples)
        command_manual.set_related_commands(related_commands)
        command_manual.set_doc(online_doc_link)

        return command_manual










class commandManual:
    def __init__(self, command ):
        self.command = command
        self._description = ""
        self._Version = ""
        self._syntax_and_usage = ""
        self._examples = ""
        self._related_commands = ""
        self._documentationlink=""

    def display_info(self):
        print(f"Command: {self.command}")
        print(f"Description: {self._description}")
        print(f"Version: {self._Version}")
        print(f"Syntax and Usage: {self._syntax_and_usage}")
        print(f"Examples: {self._examples}")
        print(f"Related Commands: {self._related_commands}")
        print(f"Documentation Link: {self._documentationlink}")

    def description(self):
        # Run the man command to get the manual page
        command_output = subprocess.run(['man', self.command], capture_output=True, text=True)

        # Check if the command was successful
        if command_output.returncode == 0:
            # Extract Name and Description from the manual page

            # Use simple patterns to find NAME and DESCRIPTION
            name_match = re.search(r'NAME\n\s*([\w-]+)', command_output.stdout)
            description_match = re.search(r'DESCRIPTION\n\s*([\s\S]+?)(?=\n\w|\Z)', command_output.stdout)
            name = name_match.group(1) if name_match else 'Name not found'
            description = description_match.group(1).strip() if description_match else 'Description not found'

            first_2_lines = '\n'.join(description.split('\n')[:2])

            # Format the output
            _description = f"\n\t{first_2_lines} \n"
        return _description

    def set_description(self, description):
        self._description = description

    # *
    def extract_version(self):

        # Try to get the version using '--version'
        version_command = subprocess.run([self.command, '--version'], capture_output=True, text=True)
        if version_command.returncode == 0:
            version = version_command.stdout.strip().split('\n')[0]
        else:
            # Try to get the version from the manual page
            version_command = subprocess.run(['man', self.command], capture_output=True, text=True)
            version_match = re.search(r'^VERSIONS\n\s*([\s\S]+?)(?=\n\w|\Z)',
                                      version_command.stdout) if version_command.returncode == 0 else None

            if version_match:
                version = version_match.group(1).strip()
            else:
                # Try to get the version using 'uname -r'
                version_command = subprocess.run(['uname', '-r'], capture_output=True, text=True)
                version = version_command.stdout.strip()

        _Version = f"\n\t{version}\n"
        return _Version

    def set_version(self, version):
        self._Version = version
    # *
    def Syntax_Usage(self):
        # Try to get synopsis using man command
        man_command = subprocess.run(['man', self.command], capture_output=True, text=True)
        man_output = man_command.stdout.strip() if man_command.returncode == 0 else ''

        # Extract only the first line from synopsis
        synopsis_match = re.search(r'SYNOPSIS\n\s*([\s\S]+?)(?=\n\w|\Z)', man_output)
        synopsis = synopsis_match.group(1).strip().splitlines()[0] if synopsis_match else 'Synopsis not found'

        _syntax_and_usage = f"\n\n\t\t{synopsis}\t\t"
        return _syntax_and_usage

    def set_syntax_and_usage(self, syus):
        self._syntax_and_usage = syus
    # *

    def related_commands(self):

        last_three_chars = self.command[-3:]
        first_three_chars = self.command[:3]
        last_four_chars = self.command[-4:]

        related_commands_command = subprocess.run(
            ['bash', '-i', '-c',
             f'compgen -A function -abck | grep "{self.command}" | grep -v "{self.command}" | head -15'],
            capture_output=True, text=True)
        related_commands = [cmd.strip() for cmd in related_commands_command.stdout.split('\n') if cmd]

        related_commands_command = subprocess.run(['bash', '-i', '-c',
                                                   f'compgen -A function -abck | grep "{last_four_chars}" | grep -v "{self.command}" | head -15'],
                                                  capture_output=True, text=True)
        related_commands += [cmd.strip() for cmd in related_commands_command.stdout.split('\n') if cmd]



        related_commands_command = subprocess.run(['bash', '-i', '-c',
                                                   f'compgen -A function -abck | grep -o "[^[:space:]]{self.command}[^[:space:]]" | grep -v "^{self.command}$" | head -15'],
                                                  capture_output=True, text=True)
        related_commands += [cmd.strip() for cmd in related_commands_command.stdout.split('\n') if cmd]



        related_commands_command = subprocess.run(['bash', '-i', '-c',
                                                   f'compgen -A function -abck | grep "{last_three_chars}" | grep -v "{self.command}" | head -15'],
                                                  capture_output=True, text=True)
        related_commands += [cmd.strip() for cmd in related_commands_command.stdout.split('\n') if cmd]



        related_commands_command = subprocess.run(['bash', '-i', '-c',
                                                   f'compgen -A function -abck | grep "{first_three_chars}" | grep -v "{self.command}" | head -15'],
                                                  capture_output=True, text=True)
        related_commands += [cmd.strip() for cmd in related_commands_command.stdout.split('\n') if cmd]







        rrelated_commands = list(set(related_commands))
        _related_commands = f"\n\t{', '.join(rrelated_commands)}\n"
        return _related_commands

    def set_related_commands(self, related_commands):
        self._related_commands = related_commands
    # *

    def extract_examples(self):



        help_command = subprocess.run([self.command, '--help'], capture_output=True, text=True)
        help_output = help_command.stdout.strip() if help_command.returncode == 0 else ''

        # Extract the line that starts with "Example" from --help output
        example_line_match = re.search(r'^\s*Example.*$', help_output, re.MULTILINE)
        example_line = example_line_match.group(0).strip() if example_line_match else ''

        # If no example in --help, try to find in man page
        if (example_line == ''):
            try:
                command_output = subprocess.run(['man', self.command], capture_output=True, text=True)

                example_line_match = re.search(r'^\s*EXAMPLES\s*$(.*?)(?=\n\w|\Z)', command_output.stdout,
                                               re.MULTILINE | re.DOTALL)
                # Extract the captured block
                example_block = example_line_match.group(1) if example_line_match else ''

                # Split the block into lines
                example_lines = example_block.split('\n')

                # Take the first 5 lines
                example_line = '\n'.join(example_lines[:5])

            except AttributeError:
                # If "EXAMPLES" section is not found in man page, retry searching in --help
                try:
                    # Execute command --help and extract the part that starts with "Example"
                    help_command_retry = subprocess.run([self.command, '--help'], capture_output=True, text=True)
                    help_output_retry = help_command_retry.stdout.strip() if help_command_retry.returncode == 0 else ''

                    # Extract the line that starts with "Example" from --help output
                    example_line_match = re.search(r'Example[^\n]\n(.?)(?=\n\w|\Z)', help_output_retry,
                                                   re.MULTILINE | re.DOTALL)
                    example_line = example_line_match.group(1).strip() if example_line_match else ''
                except AttributeError:
                    example_line = 'Example line not found'
        if (example_line == ''):
            if (self.command == 'cp'):

                example_line = 'cp file.txt copied_file.txt'
            elif (self.command == 'printf'):
                example_line = ' printf  %s Hello World!'


            elif (self.command == 'wc'):
                example_line = 'wc filename'

            elif (self.command == 'ss' or self.command == 'lspci'  or self.command == 'vmstat'):
                result = subprocess.run([self.command,'-t'], capture_output=True, text=True)

                # Check if the command was successful
                if result.returncode == 0:
                    example_line = result.stdout.strip()

                else:
                    # Print an error message
                    result = subprocess.run([self.command], capture_output=True, text=True)
                    if result.returncode == 0:
                        example_line = result.stdout.strip()

        if (self.command == 'cat'):
            example_line = ' cat  file name '

        _examples = f"\n\n\t{example_line}\n"

        return _examples


    def set_examples(self, example_lines):
        self._examples = example_lines
    # **
    def documentation_link(self):

        documentation_link = f"https://man7.org/linux/man-pages/man1/{self.command}.1.html"
        documentationlink = f"\n\t\n {documentation_link}\n"

        # Run the command 'man' and capture the output
        man_command = subprocess.run(['man', self.command], capture_output=True, text=True)
        man_output = man_command.stdout

        # Extract the "SEE ALSO" section using awk and grep
        # see_also_match = re.search(r'^\s*SEE ALSO\s*(.*?)(?=\n\w|\Z)', man_output, re.MULTILINE | re.DOTALL)
        see_also_match = re.search(r'^\s*Full documentation\s*(.*?)(?=\n\w|\Z)', man_output, re.MULTILINE | re.DOTALL)
        if see_also_match and see_also_match.group(1).strip():
            see_also_section = see_also_match.group(1).strip()
            documentationlink += f"\t{see_also_section}"
        return documentationlink



    def set_doc(self, documentation_lines):
        self._documentationlink = documentation_lines
    # //////////////////////////////////////////////////////////////////////////


#--------------------------------------------------------------------------


class commandMnaualGenerator:

    def __init__(self, input_file):
        self.input_file = input_file
        self.manuals = []

    def read_from_file(self):
        # Read commands from command.txt
        with open(self.input_file, "r") as file:
            self.manuals = file.read().splitlines()

    def generate_manuals(self , option):
        # Generate manuals for each command
        for command in self.manuals:
            generator2 = commandManual(command)
            Serializer.serialize(generator2, command , option)

    def show_manual_from_xml(self):
        command_name = input("Enter the command name: ").lower()
        deserialized_manual =Serializer.deserialize(f"{command_name}_manual.xml")
        deserialized_manual.display_info()



generator = commandMnaualGenerator("Commands.txt")


class CommandManualVerification:
    def __init__(self):
        pass

    def compare_xml_files(self, file1, file2):
        # Parse XML files
        tree1 = ET.parse(file1)
        tree2 = ET.parse(file2)

        # Get root elements
        root1 = tree1.getroot()
        root2 = tree2.getroot()

        # Convert elements to strings
        xml_str1 = ET.tostring(root1, encoding="unicode")
        xml_str2 = ET.tostring(root2,encoding="unicode")

        # Compare strings using unified diff
        diff = difflib.unified_diff(xml_str1.splitlines(), xml_str2.splitlines())

        # Check if there are differences
        differences = list(diff)
        if differences:
            print("Differences found in:")
            for line in differences:
                print(line)
        else:
            print("Manual are verified. No differences found.")




while True:
    print("Menu:")
    print("1. Generate Manuals")
    print("2. Search Manual for Specific Command")
    print("3. Command Recommendation System")
    print("4. Verification")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        generator.read_from_file()
        generator.generate_manuals(1)

        print("Manuals generated successfully!")

    elif choice == "2":
        generator.show_manual_from_xml()

    elif choice == "3":

        ommand_name = input("Enter  command name for recomandation: ").lower()
        generator2 = commandManual(ommand_name)
        rela = generator2.related_commands()
        print("Related command :" + rela)


    elif choice == "4":
        generator.read_from_file()
        generator.generate_manuals(4)
        verification = CommandManualVerification()
        command_name = input("Enter  command name you want to verify: ").lower()
        verification.compare_xml_files(f"{command_name}_manual.xml", f"{command_name}_Ver.xml")

    elif choice == "5":
        break

    else:
        print("Invalid choice. Please enter a valid option.")