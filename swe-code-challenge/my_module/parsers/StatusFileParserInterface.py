from abc import ABC, abstractmethod
from my_module.models.StatusFile.StatusFileSectionCollection import StatusFileSectionCollection


class StatusFileParserInterface(ABC):
    @abstractmethod
    def tokenize(self, file_contents: str) -> list:
        """
        Splits the file into sections only relevant to their package
        """
        pass
    
    @abstractmethod
    def parse(self, package_data: list) -> StatusFileSectionCollection:
        """
        Parses the data in the section to see if it matches any installed packages
        """
        pass