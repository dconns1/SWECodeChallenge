from datetime import datetime
from typing import Optional


class HistoryFileSection():
    def __init__(self):
        self._start_date = None
        self._requested_by = "undetermined"
        self._end_date = None
        self._packages = []
        self._reinstall = False
    
    @property
    def start_date(self) -> Optional[datetime]:
        """Gets the start date 

        Returns:
            Optional[datetime]: The start date specified for the commands that installed in the history.log file 
        """
        return self._start_date
    
    @start_date.setter
    def start_date(self, value):
        """Sets the start date if a valid value of date is sent

        Args:
            value: The start date specified for the commands that installed in the history.log file

        Raises:
            TypeError: If a value date value is not passed for start_date
        """
        if not isinstance( value, datetime ):
            raise TypeError("start_date must be an instance of datetime")
        
        self._start_date = value
        
    @property
    def end_date(self) -> Optional[datetime]:
        """Gets the end date 

        Returns:
            Optional[datetime]: The end date specified for the commands that installed in the history.log file 
        """
        return self._end_date
    
    @end_date.setter
    def end_date(self, value):
        """Sets the end date if a valid value of date is sent

        Args:
            value: The end date specified for the commands that installed in the history.log file

        Raises:
            TypeError: If a value date value is not passed for end_date
        """
        if not isinstance( value, datetime ):
            raise TypeError("end_date must be an instance of datetime")
        
        self._end_date = value
    
    @property
    def packages(self) -> list:
        """Gets the list of packages 

        Returns:
            list: A list of packages specified on the Commandline of the history file
        """
        return self._packages
    
    @packages.setter
    def packages(self, value):
        """Sets the list of packages if a value list is sent
        
        Args:
            value: A list of packages specified on the Commandline of the history file

        Raises:
            TypeError: If the value passed is not in a list
            ValueError: If the list provided is empty
        """
        if not isinstance( value, list ):
            raise TypeError("packages must be an instance of a list")
        
        if not len(value) > 0:
            raise ValueError("packages must contain value, list cannot be empty")
        
        self._packages = value
        
    @property
    def requested_by(self) -> str:
        """Gets the requested by user

        Returns:
            str: The requested by user
        """
        return self._requested_by
    
    @requested_by.setter
    def requested_by(self, value):
        """Sets the requested by user

        Args:
            value: The requested by user
        """
        if value:
            self._requested_by = value
            