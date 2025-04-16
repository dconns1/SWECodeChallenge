from my_module.models.StatusFile.StatusFileSection import StatusFileSection
from my_module.models.HistoryFile.HistoryFileSectionCollection import HistoryFileSectionCollection


class StatusFileSectionCollection():
    def __init__(self):
        self.__status_file_section_collection: list[StatusFileSection] = []
        
    def append(self, status_file_section: StatusFileSection):
        """Appends a StatusFileSection to the collection

        Args:
            status_file_section (StatusFileSection): An object containing data from the status file section
        """
        self.__status_file_section_collection.append( status_file_section )
        
    def get_status_file_section_collection(self) -> list[StatusFileSection]:
        """Returns the collection of status file sections

        Returns:
            list[StatusFileSection]: A list of objects containing status file section data
        """
        return self.__status_file_section_collection
    
    def get_status_file_packages(self) -> list:
        """Creates a list of the package names from the status file and returns them as a list

        Returns:
            list: Returns a list of package names
        """
        package_list = []
        
        for section in self.__status_file_section_collection:
            if section.package:
                package_list.append( section.package )
                
        return package_list
    
    def get_user_installed_packages(self, history_file_section_collection: HistoryFileSectionCollection) -> list:
        """Creates and returns a list of packages that overlap with packages from the history file

        Args:
            packages_list (list): List of packages pulled as installed

        Returns:
            list: List of packages that overlap between status file and the installed package list
        """
        overlapping_packages = []
        
        for section in self.__status_file_section_collection:
            reinstalled = ""
            # Checks to see if the package exists in the history file
            if section.package in history_file_section_collection.get_sections_packages():
                # Pulls the data for the history file that matches the package
                history_file_section = history_file_section_collection.get_history_file_section_by_package( section.package )
                # Creates output using both status file data and history file data for the user
                overlapping_packages.append(f"{section.package} ({section.version})::{history_file_section.requested_by} {section.installed_size} KiB")
                
        return overlapping_packages