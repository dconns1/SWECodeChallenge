from my_module.models.HistoryFile.HistoryFileSection import HistoryFileSection
from typing import Optional


class HistoryFileSectionCollection():
    def __init__(self):
        self.__history_file_section_collection: list[HistoryFileSection] = []
        
    def append(self, history_file_section: HistoryFileSection):
        """Appends a HistoryFileSection to the collection

        Args:
            history_file_section (HistoryFileSection): An object containing data from the history file section
        """
        self.__history_file_section_collection.append( history_file_section )
        
    def get_history_file_section_collection(self) -> list[HistoryFileSection]:
        """Returns the collection of history file sections

        Returns:
            list[HistoryFileSection]: A list of objects containing history file sections data
        """
        return self.__history_file_section_collection
        
    def get_sections_packages(self) -> list[list]:
        """Iterates over the collection and returns a separate list of only 
        the section's packages.

        Returns:
            list[str]: A list of each sections packages as a list
        """
        sections_packages = []
        
        for section in self.__history_file_section_collection:
            for packages in section.packages:
                sections_packages.append( packages )
                
        return sections_packages
    
    def get_history_file_section_by_package(self, package: str) -> Optional[HistoryFileSection]:
        """Pulls the history file section if the package exists within that section

        Args:
            package (str): A string that defines a package

        Returns:
            Optional[HistoryFileSection]: Returns the matching package or None
        """
        for section in self.__history_file_section_collection:
            if package in section.packages:
                return section
            
        return None