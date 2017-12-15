# -*- coding: utf-8 -*-
"""
@author: Michalis Palaiokostas
"""
import pandas as pd


class SummaryFile:
    def __init__(self,name):
        self.name = name
        self.raw = pd.read_csv(self.name, sep='\t', header=0)

        # Clean any \# in front of header line and left whitespace
        if self.raw.columns.values[0][0] == '#':
            old_value = self.raw.columns.values[0]
            new_value = self.raw.columns.values[0].lstrip('#').lstrip()
            self.raw = self.raw.rename(columns={old_value: new_value})
            
    def raw_data(self):
        """
        Returns the raw data as read by the file. The header has been 
        modified to remove the comment character (#).        
        Output: A dataframe
        """
        return self.raw       

    def filter_columns(self, column_names):
        return self.raw[column_names]

    def filter_positions_columns(self,column_names=[]):
        """
        Returns the rows with non-negative positions and the columns of 
        interest.
        Input (optional): A list of columns. By default returns all.
        Output: A dataframe
        """
        if column_names == []:
            return self.raw.loc[self.raw['position'] >= 0.0]
        else:
            return self.raw.loc[self.raw['position'] >= 0.0][column_names]
        
        
class MoleculesFile:
    def __init__(self, name):
        """
        Reads a csv file and loads the properties of the molecules.
        It will sort based on molecular weight ('MolWeight') so this should 
        be the name of at least one column.
        """

        self.name = name
        self.raw = pd.read_csv(self.name, sep=',', header=0)

        # Clean any \# in front of header line and left whitespace
        if self.raw.columns.values[0][0] == '#':
            old_value = self.raw.columns.values[0]
            new_value = self.raw.columns.values[0].lstrip('#').lstrip()
            self.raw = self.raw.rename(columns={old_value:new_value})

        # Sort data based on molecular weight 
        self.raw.sort_values('MolWeight', axis='rows',
                             ascending=True, inplace=True)
        
    def raw_data(self):
        '''
        Returns the raw data as read by the file. The header has been 
        modified to remove the comment character (#). Dataframe was sorted
        based on molecular weight.
        Output: A dataframe
        '''
        return self.raw 