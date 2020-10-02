import random

import pandas as pd

SONET_DEBUG = True
def PrintDict(ar_dict):
    """
    Convenience function for printing a dictionary to console.
    Useful for debugging.
    :param ar_dict:
    """
    print("Keys> ", [x for x in ar_dict.keys()])
    print("Values> ", [x for x in ar_dict.values()])


from enum import Enum, unique


@unique
class ObjectType(Enum):
    """
    Enum representing the variety of artifacts appearing in sonet app.
    """
    NA = 0  # NA stands for Not Assigned
    SPACECRAFT = 1

@unique
class ObjectState(Enum):
    """
    Enum representing the state of the objects, useful to find errors. if(ObjectState==Error)...
    """
    NA = 0
    OK = 1
    ERROR = 2

@unique
class SpacecraftType(Enum):
    """
    Enum representing the kind of spacecrafts.
    """
    NA = 0  # NA stands for Not Assigned
    CREWED = 1
    CARGO = 2

@unique
class FilterType(Enum):
    """
    Enum representing the type of filter applied to the spacecrafts trajectories.
    """
    NA = 0
    ENERGY = 1  # ['dvt', '<', '4', 'km/s']
    TOF = 2  # ['Time of flight', '<', '200', 'days']
    DATES = 3  # ['Departs', 'Earth', 'Before', '20/07/2021']
    DATES_2 = 4  # ['Departs', 'Mars', 'At the same time', 'Spacecraft 1', 'Leaves Earth']

def build_mock_DataFrame(num_rows=5, num_columns=8, min=0, max=10):
    # Build columns
    num_rows = random.randint(1,1e2)
    _ = ['col'+str(i) for i in range(num_columns)]
    result = pd.DataFrame(columns=_)
    build_row = lambda: [random.randint(min,max) for _ in range(num_columns)]
    for i in range(num_rows):
        result.loc[len(result)] = build_row()
    return result


if __name__ == "__main__":
    d = {'key1': 'value1', 'key2': 'value1'}
    PrintDict(d)
