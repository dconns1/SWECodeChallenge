import os
import logging
from my_module.parsers.HistoryFileParser import HistoryFileParser
from my_module.parsers.StatusFileParser import StatusFileParser
from my_module.parsers.HistoryFileParserInterface import HistoryFileParserInterface
from my_module.parsers.StatusFileParserInterface import StatusFileParserInterface


class SWECodeChallenge():
    # I created constants for these values because I have the runtime occurring 
    # in the same script.
    # I would traditionally have these values as constants in something like a 
    # CLI or even a configuration file so their locations could be adjusted later 
    # if needed.
    STATUS_FILE = "/var/lib/dpkg/status"
    HISTORY_LOG = "/var/log/apt/history.log"
    
    def __init__(self, history_file_parser: HistoryFileParserInterface, status_file_parser: StatusFileParserInterface):
        # Allows the user to inject the parser for the history.log file
        # This is type hinted as a HistoryFileParserInterface so that any HistoryFileParser 
        # can be injected if at a later time if a larger refactor would be done.  
        # This removes implicit dependency.
        self.__history_file_parser = history_file_parser
            
        # Allows the user to inject the parser for the status file
        # This is type hinted as a StatusFileParserInterface so that any StatusFileParser 
        # can be injected if at a later time if a larger refactor would be done.
        # This removes implicit dependency.
        self.__status_file_parser = status_file_parser # Make this status file parser
        
    def parse_for_package_list(self):
        # Check to see if status file exists
        if( not os.path.exists( self.STATUS_FILE ) ):
            raise FileNotFoundError( self.STATUS_FILE )
        
        # Checks to see if history log exists
        if( not os.path.exists( self.HISTORY_LOG ) ):
            raise FileNotFoundError( self.HISTORY_LOG )
        
        # Pulls the history log's data and breaks it out into sections
        with open( self.HISTORY_LOG, "r" ) as history_file:
            history_file_tokens = self.get_history_file_parser().tokenize( history_file.read() ) 
            
        # Parses the history log and passes back a collection of objects with the relevant data
        history_file_section_collection = self.get_history_file_parser().parse( history_file_tokens )
        
        # Pulls the status file data and breaks it out into sections
        with open( self.STATUS_FILE, "r" ) as status_file:
            status_file_tokens = self.get_status_file_parser().tokenize( status_file.read() )
        
        # Parses the history log and passes back a collection of objects with the relevant data
        status_file_section_collection = self.get_status_file_parser().parse( status_file_tokens )
        
        # Uses the collections to format output
        for data in status_file_section_collection.get_user_installed_packages( history_file_section_collection ):
            # Output to console
            print(data)
            
    def get_history_file_parser(self) -> HistoryFileParser:
        """Gets the history file parser injected into the class

        Returns:
            HistoryFileParser: A parser created for the history file
        """
        return self.__history_file_parser
    
    def get_status_file_parser(self) -> StatusFileParser:
        """Gets the status file parser injected into the class

        Returns:
            StatusFileParser: A parser created for the status file
        """
        return self.__status_file_parser

def main():
    try:
        logger = logging.getLogger( __name__ )
        logging.basicConfig( filename="SWECodeChallenge.log", encoding="utf-8", level=logging.INFO )
        
        # Creates instances of parsers
        hf_parser = HistoryFileParser( logger )
        sf_parser = StatusFileParser( logger )
        
        # Creates instance of SWECodeChallenge
        # Injects the parsers
        instance = SWECodeChallenge( hf_parser, sf_parser )
    
        instance.parse_for_package_list()
    except FileNotFoundError as fe:
        # Normally I would just raise the exception again with the formatting
        # For the instance where this could be relevant immediately to the reviewer
        # I wanted to print this here also
        print( f"An error has occurred '{fe}' does not exist." )
        raise Exception( f"An error has occurred '{fe}' does not exist." )
    except Exception as e:
        logger.error( f"An error has occurred:\n{e.with_traceback(e.__traceback__)}" )
        print( f"Please check SWECodeChallenge.log to see errors" )
        
if __name__ == "__main__":
    main()