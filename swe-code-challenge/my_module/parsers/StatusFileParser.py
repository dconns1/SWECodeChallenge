import re
import logging
from .StatusFileParserInterface import StatusFileParserInterface
from my_module.models.StatusFile.StatusFileSection import StatusFileSection
from my_module.models.StatusFile.StatusFileSectionCollection import StatusFileSectionCollection
from typing import Optional


class StatusFileParser(StatusFileParserInterface):
    FILE_SECTION_REGEX = r"^Package: .*(?:\n(?!Package: ).*)*"
    DESCRIPTION_REGEX = r"^Description: (.+)(?:\n(?!\S).*.+)*"
    
    def __init__(self, logger: logging):
        self.__logger = logger
    
    def tokenize(self, file_contents: str) -> list:
        """Uses a regex to break out sections of the status file for each package

        Args:
            file_contents (str): The contents of the status file

        Returns:
            list: A list of segments of text specific to each package
        """
        return re.findall( self.FILE_SECTION_REGEX, file_contents, flags=re.MULTILINE )
    
    def parse(self, package_data: list) -> StatusFileSectionCollection:
        """Parses the status file

        Args:
            package_data (list): A list of sections based on the installed packages

        Returns:
            StatusFileParserInterface: A collection of objects storing the data for packages installed
        """
        status_file_section_collection = StatusFileSectionCollection()
        
        for section in package_data:
            status_file_section = self.__parse_section_lines( section )
            
            if status_file_section:
                status_file_section_collection.append( status_file_section )
                
        return status_file_section_collection
                
    def __parse_section_lines(self, section_contents: str) -> Optional[StatusFileSection]:
        """Iterates through each section line by line looking for relevant data and 
        storing it in a usable object

        Args:
            section_contents (str): A string of the current section as a whole

        Returns:
            Optional[StatusFileSection]: An object containing all relevant data or
            none if no package name was provided
        """
        # Creates a new instance of StatusFileSection to store the relevant data for that section
        status_file_data = StatusFileSection()
        
        # Pulls the section data first by regex since it will be ignored when iterating line by line
        status_file_data.description = self.__parse_description_text( section_contents )
        
        for line in section_contents.split( "\n" ):
            try:
                if line.startswith("Package:"):
                    status_file_data.package = self.__parse_line_for_parameter_value( line, "Package: " )
                
                if line.startswith("Section:"):
                    status_file_data.section = self.__parse_line_for_parameter_value( line, "Section: " )
                    
                if line.startswith("Version:"):
                    status_file_data.version = self.__parse_line_for_parameter_value( line, "Version: " )
                    
                if line.startswith("Installed-Size:"):
                    status_file_data.installed_size = self.__parse_line_for_parameter_value( line, "Installed-Size: " )
            except Exception as e:
                self.get_logger().warning(f"line skipped:\n{line}\nAn error occurred:\n{e.with_traceback()}")
                # If the line does not have functional data to store it continues to the next line
                continue
        
        if status_file_data.package:
            return status_file_data
        
        return None
    
    def __parse_description_text(self, section_contents: str) -> str:
        """Pulls the description section out of the contents and formats it

        Args:
            section_contents (str): The section contents for a package

        Returns:
            str: the description text formatted
        """
        description_text = ""
        
        description_text_raw = re.search( self.DESCRIPTION_REGEX, section_contents, re.MULTILINE )
        
        for line in description_text_raw[0].split( "\n" ):
            if line.startswith(" ."):
                description_text += "\n"
            elif line.startswith("Description: "):
                description_text += line.replace("Description: ", "")
                description_text += "\n"
            elif line.startswith("  *"):
                description_text += f"{line}\n"
            else:
                description_text += f"{line} "
        
        return description_text
    
    def __parse_line_for_parameter_value(self, line: str, parameter: str) -> str:
        """Pulls the parameter specified's value out of the section

        Args:
            line (str): The line beginning with the parameter
            parameter (str): The value the user wants from the line

        Returns:
            str: The parameter's value
        """
        return line.replace( parameter, "" )
    
    def get_logger(self) -> logging:
        """Gets the logger

        Returns:
            logging: Used to log
        """
        return self.__logger
    