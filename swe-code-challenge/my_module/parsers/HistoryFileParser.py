import re
import logging
from .HistoryFileParserInterface import HistoryFileParserInterface
from my_module.models.HistoryFile.HistoryFileSection import HistoryFileSection
from my_module.models.HistoryFile.HistoryFileSectionCollection import HistoryFileSectionCollection
from datetime import datetime
from typing import Optional


class HistoryFileParser(HistoryFileParserInterface):
    FILE_SECTION_REGEX = r"Start-Date: .*?End-Date: .*?(?=\nStart-Date:|\Z)"
    DATE_REGEX = r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}"
    
    def __init__(self, logger: logging):
        self.__logger = logger
        
    def tokenize(self, file_contents: str) -> list:
        """Uses a regex to break out sections of the history.log file for each command

        Args:
            file_contents (str): The contents of the history.log file

        Returns:
            list: A list of segments of text specific to each command ran 
        """
        regex_pattern = re.compile( self.FILE_SECTION_REGEX, re.DOTALL )
        return re.findall( regex_pattern, file_contents )
    
    def parse(self, command_data: list) -> HistoryFileSectionCollection:
        """Parses the history file

        Args:
            command_data (list): A list of sections based on installs start times and end times

        Returns:
            HistoryFileSectionCollection: A collection of objects storing the data for packages installed
        """
        history_file_section_collection = HistoryFileSectionCollection()
        
        for section in command_data:
            # Iterates through each section parsing it for installed packages
            history_file_section = self.__parse_section_lines( section )
            
            if history_file_section:
                # If a section is returned it stores it in the list for later use
                history_file_section_collection.append( history_file_section )
                
        return history_file_section_collection
        
    def __parse_section_lines(self, section_contents: str) -> Optional[HistoryFileSection]:
        """Iterates through each section line by line looking for relevant data and 
        storing it in a usable object

        Args:
            section_contents (str): A string of the current section as a whole

        Returns:
            Optional[HistoryFileSection]: An object containing all relevant data or
            none if there was no installed packages in 
            this section
        """
        # Creates a new instance of HistoryFileSection to store the relevant data for that section
        history_file_data = HistoryFileSection()
        
        # Iterates through the lines in the section to pull specific data and stores it in HistoryFileSection
        for line in section_contents.split( "\n" ):
            try:
                if line.startswith( "Start-Date:" ):
                    # Pulls the start date and converts it to a datetime
                    start_date_value = self.__parse_line_for_datetime( line )
                    
                    # If the data present could not convert to a datetime returns null and doesn't store a start date
                    if start_date_value:
                        history_file_data.start_date = start_date_value 
                
                if line.startswith( "Commandline:" ):
                    # Pulls the list of commands
                    history_file_data.packages = self.__parse_for_command_line_arguments( line ) 
                
                if line.startswith( "Requested-By:" ):
                    # Pulls the requested by user
                    requested_by = self.__parser_for_requested_by( line )
                    
                    if requested_by:
                        history_file_data.requested_by = requested_by
                
                if line.startswith( "End-Date:" ):
                    # Pulls the end date and converts it to a datetime
                    end_date_value =  self.__parse_line_for_datetime( line )
                    
                    # If the data present could not convert to a datetime returns null and doesn't store a end date
                    if end_date_value:
                        history_file_data.end_date = end_date_value
            except Exception as e:
                self.get_logger().warning(f"line skipped:\n{line}\nAn error occurred:\n{e.with_traceback(e.__traceback__)}")
                # If the line does not have functional data to store it continues to the next line
                continue
            
        # If there were packages installed in this section then return it
        if len(history_file_data.packages) > 0:
            return history_file_data
        
        # If no packages were installed in this section return None
        return None
                
    def __parse_line_for_datetime(self, line) -> Optional[datetime]:
        """Parses the line for the date in string form and converts it to a datetime

        Args:
            line (str): The line for either the start date or end date of the section

        Returns:
            Optional[datetime]: Either the datetime of the string pulled from the regex or None since
            a datetime could not be created
        """
        datetime_string = re.search( self.DATE_REGEX, line )
        
        if datetime_string:
            try:
                # Returns the datetime
                return datetime.strptime( datetime_string.group(), "%Y-%m-%d  %H:%M:%S" )
            except:
                # Returns None since the string could not be converted
                return None
                
        # Returns None since the datetime could not be pulled out of the string
        return None
    
    def __parse_for_command_line_arguments(self, line: str) -> list:
        """Parses the line for a list of packages specified by an install command
        If a install command was not provided an empty list is sent back

        Args:
            line (str): The line starting with Commandline

        Returns:
            list: A list of packages installed.  If not packages were installed it returns an empty list.
        """
        packages = []
        # Pulls only values after the install command
        command_items = line.split( " install ", 1 )[1].strip().split( " " )
        
        # Iterates over the command items and ignores anything with a - in it
        # This ignores items like -y or --reinstall
        for command in command_items:
            if not command.startswith("-"):
                packages.append( command )
                
        return packages
    
    def __parser_for_requested_by(self, line: str) -> str:
        """Pulls the requested by user out of the line

        Args:
            line (str): The line starting with Requested-By

        Returns:
            str: The user who requested the install of the package
        """
        requested_by_items = line.strip().split( " " )
        
        # Takes the second value in the list since thats where the user's name is located
        return requested_by_items[1]
    
    def get_logger(self) -> logging:
        """Gets the logger

        Returns:
            logging: Used to log
        """
        return self.__logger