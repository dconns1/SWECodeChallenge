from abc import ABC, abstractmethod
from my_module.models.HistoryFile.HistoryFileSectionCollection import HistoryFileSectionCollection


class HistoryFileParserInterface(ABC):
    @abstractmethod
    def tokenize(self, file_contents: str) -> list:
        """
        Splits the file into sections only relevant to their package
        """
        pass
    
    @abstractmethod
    def parse(self, command_data: list) -> HistoryFileSectionCollection:
        """
        Parses the lines in the section to see if it includes any installed packages
        """
        pass
    