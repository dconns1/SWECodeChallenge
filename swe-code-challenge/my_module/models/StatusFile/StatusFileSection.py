class StatusFileSection():
    def __init__(self):
        self._package = ""
        self._section = ""
        self._version = ""
        self._description = ""
        self._installed_size = ""
        
    @property
    def package(self) -> str:
        """Gets the package specified in the section of the status file

        Returns:
            str: The package's package 
        """
        return self._package
    
    @package.setter
    def package(self, value):
        """Sets the value extracted from the package line of the section in the status file

        Args:
            value: The package's package
        """
        if value:
            self._package = value
            
    @property
    def section(self) -> str:
        """Gets the section specified for the package in the section of the status file

        Returns:
            str: The package's section
        """
        return self._section
    
    @section.setter
    def section(self, value):
        """Sets the value extracted from the section line of the section in the status file

        Args:
            value: The package's section
        """
        if value:
            self._section = value
            
    @property
    def version(self) -> str:
        """Gets the version specified for the package in the section of the status file

        Returns:
            str: The package's version
        """
        return self._version
    
    @version.setter
    def version(self, value):
        """Sets the version value specified for the package in the section of the status file

        Args:
            value: The package's version
        """
        if value:
            self._version = value
            
    @property
    def description(self) -> str:
        """Gets the description for the package in the section of the status file

        Returns:
            str: The package's description
        """
        return self._description
    
    @description.setter
    def description(self, value):
        """Sets the description for the package in the section of the status file

        Args:
            value: The package's description
        """
        if value:
            self._description = value
            
    @property
    def installed_size(self) -> str:
        """Gets the installed size for the package in the section of the status file

        Returns:
            str: The package's installed size
        """
        return self._installed_size
    
    @installed_size.setter
    def installed_size(self, value):
        """Sets the installed size for the package in the section of the status file

        Args:
            value: The package's installed size
        """
        if value:
            self._installed_size = value