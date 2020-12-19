import pandas as pd
from overloading import overload

from src.SonetTrajectoryFilter import SonetTrajectoryFilter
from src.SonetUtils import SpacecraftType, TripType, sonet_log, SonetLogType


class SonetSpacecraft:
    """
    Sonet spacecraft class.
    The spacecrafts can be:
     - Cargo/crewed.
     - One way/two way.

    A correct form to build a SonetSpacecraft object would be to declare an empty SonetSpacecraft() and then call to
    the constructing methods:
     - set_spacecraft_type()
     - set_has_return_trajectory()
     - set_filters()

    A correct form to work with the spacecraft filter would be:
     - Get a filter, with get_filter() or directly modifying the desired filter (e.g. _pcp_filter1, _pcp_filter1, or
     _pcp_filter).
     - Modify the filter's internal dataframe using the SonetTrajectoryFilter's set_data method.
     -  Get a filtered porkchop plot table with SonetTrajectoryFilter's get_filtered_pcp method.
    """
    def __init__(self, a_spacecraft_type_crew=None, a_spacecraft_type_return=None):
        sonet_log(SonetLogType.INFO, 'SonetSpacecraft.__init__')

        # Instance members
        self._spacecraft_type = None  # Enum
        self._has_return_trajectory = None

        self.set_spacecraft_type(a_spacecraft_type_crew)
        self.set_has_return_trajectory(a_spacecraft_type_return)
        self.set_filters()
        # dir_path = '/Users/Jorialand/code/tfm/sonet/sonet_tfm_horia/src/'
        # _ = self.get_spacecraft_type()
        #
        # # Crewed spacecrafts travel to and from Mars. Cargo ones travel only once to Mars and remain there.
        # if _ is SpacecraftType.CREWED:
        #     # Earth - Mars (outgoing) and Mars - Earth (incoming) porkchop plots (pcp).
        #     self._df_outgoing = database.pcp_outgoing#pd.read_csv(dir_path + '10kPCP_Earth2Mars.txt')
        #     self._df_incoming = database.pcp_incoming#pd.read_csv(dir_path + '10kPCP_Mars2Earth.txt')
        #     self._filter_outgoing = SonetTrajectoryFilter()
        #     self._filter_incoming = SonetTrajectoryFilter()
        #
        #     # Draft [POSSIBLE COPY WARNING]
        #     ini = random.randint(0, 10)
        #     fin = random.randint(11, 22)
        #     self._df_outgoing = self._df_outgoing.iloc[ini:fin]
        #
        #     ini = random.randint(0, 10)
        #     fin = random.randint(11, 22)
        #     self._df_incoming = self._df_incoming.iloc[ini:fin]
        #
        # elif _ is SpacecraftType.CARGO:
        #     self._df_outgoing = pd.read_csv(dir_path + '10kPCP_Earth2Mars.txt')
        #
        #     # Draft [POSSIBLE COPY WARNING]
        #     ini = random.randint(0, 10)
        #     fin = random.randint(11, 22)
        #     self._df_outgoing = self._df_outgoing.iloc[ini:fin]
        #
        # else:
        #     print('Error in SonetSpacecraft constructor, wrong SpacecraftType.')
        #     return False

    # Public methods
    def get_filter(self, a_trip_type=None):
        """
        Getter method, overload with a more specific functionality. It returns a concrete SonetTrajectoryFilter, based
        on the input a_trip_type.
        :param a_trip_type: TripType enum.
        :return: SonetTrajectoryFilter.
        """
        # If no trip type specified, return all the filters.
        if a_trip_type is None:
            try:
                return self._pcp_filter
            except AttributeError:
                return [self._pcp_filter1, self._pcp_filter2]
            except TypeError:
                return False

        # Type check.
        if not isinstance(self._has_return_trajectory, bool):
            sonet_log(SonetLogType.ERROR, 'SonetSpacecraft.get_filter."Bad constructed S/C"')
            return False  # _has_return_trajectory should be bool, if not, there's some error.

        if not isinstance(a_trip_type, TripType):
            sonet_log(SonetLogType.ERROR, 'SonetSpacecraft.get_filter."Wrong TripType"')
            return False

        if self._has_return_trajectory:
            if a_trip_type is TripType.OUTGOING:
                return self._pcp_filter1
            elif a_trip_type is TripType.INCOMING:
                return self._pcp_filter2
        else:
            if a_trip_type is TripType.OUTGOING:
                return self._pcp_filter
            elif a_trip_type is TripType.INCOMING:
                sonet_log(SonetLogType.ERROR, 'SonetSpacecraft.get_filter."Asked for incoming filter to an one-way S/C"')
                return False

    def get_filter_data(self, get_dataframe_copy=False):
        """
        Getter method.
        It's not the same to return a dataframe and a dataframe.copy(). get_dataframe_copy controls if we are getting
        the pointers to the original dataframes or copies of them.
         - If I return a dataframe, I am returning a pointer to the original dataframe, so all modifications are going
         to affect to the original dataframe.
         - If I return a dataframe copy, I am returning a new dataframe, so all modifications are not going to affect to
         the original dataframe.
         :param get_dataframe_copy: bool representing if we want original dataframes or copies.
        :return: a pandas dataframe or a list of them.
        """
        # Type check.
        if not isinstance(self._has_return_trajectory, bool):
            sonet_log(SonetLogType.ERROR, 'SonetSpacecraft.get_filter_data."Bad constructed S/C"')
            return False  # _has_return_trajectory should be bool, if not, there's some error.

        if self._has_return_trajectory:
            # If there are both outgoing and incoming trajectories, we return a list with both filter's dataframes.
            if get_dataframe_copy:
                return [self._pcp_filter1.get_data().copy(), self._pcp_filter2.get_data().copy()]
            else:
                return [self._pcp_filter1.get_data(), self._pcp_filter2.get_data()]

        else:
            # In case the spacecraft has no return trajectory, we just get the filter dataframe of the outgoing one.
            if get_dataframe_copy:
                return self._pcp_filter.get_data().copy()
            else:
                return self._pcp_filter.get_data()

    def get_has_return_trajectory(self):
        """
        Getter method.
        :return: bool. If the variable hasn't been setted, then it will return the default value,
        None, which is considered a boolean False.
        """
        return self._has_return_trajectory

    def get_spacecraft_type(self):
        """
        Getter method.
        :return: Enum (SpacecraftType). If the variable hasn't been setted, then it will return the default value,
        None, which is considered a boolean False.
        """
        return self._spacecraft_type

    def set_filter(self, a_the_filter, dataframe=False):
        """
        Setter method.
        Sets the argument filter as current SonetSpacecraft's filter. If the input is a list of filters, then the
        spacecraft has outgoing and return trajectories and has two filters, otherwise only has outgoing trajectory and
        has only one filter.
        :return: bool true if everything was ok, false otherwise.
        """
        if dataframe is True:
            if isinstance(a_the_filter, list):
                self._pcp_filter1.set_data(a_the_filter[0].copy())
                self._pcp_filter2.set_data(a_the_filter[1].copy())
            elif isinstance(a_the_filter, pd.DataFrame):
                self._pcp_filter.set_data(a_the_filter.copy())
        else:
            if isinstance(a_the_filter, list):
                self._pcp_filter1.set_data(a_the_filter[0].get_data().copy())
                self._pcp_filter2.set_data(a_the_filter[1].get_data().copy())
            elif isinstance(a_the_filter, SonetTrajectoryFilter):
                self._pcp_filter.set_data(a_the_filter.get_data().copy())

    def set_filters(self):
        """
        Method for constructing a SonetSpacecraft object. The spacecraft has one filter per trajectory.
        TODO: Bad practice - defining instance attributes outside the class constructor.
        :return: True if everything was ok, false otherwise.
        """
        has_return_trajectory = self._has_return_trajectory

        # Type check.
        if not isinstance(has_return_trajectory, bool):
            return False

        if has_return_trajectory:
            # Two way trip.
            self._pcp_filter1 = SonetTrajectoryFilter(TripType.OUTGOING)
            self._pcp_filter2 = SonetTrajectoryFilter(TripType.INCOMING)
        else:
            # One way trip.
            self._pcp_filter = SonetTrajectoryFilter(TripType.OUTGOING)
        return True

    def set_has_return_trajectory(self, a_has_return_trajectory=None):
        """
        Method for constructing a SonetSpacecraft object.
        :param a_has_return_trajectory: bool
        :return: True if everything was ok, false otherwise.

        """
        # Convert string input to bool.
        if isinstance(a_has_return_trajectory, str):
            if a_has_return_trajectory == 'One way':
                a_has_return_trajectory = False
            elif a_has_return_trajectory == 'Two way':
                a_has_return_trajectory = True

        # Type check.
        if not isinstance(a_has_return_trajectory, bool):
            return False

        self._has_return_trajectory = a_has_return_trajectory
        return True

    def set_spacecraft_type(self, a_spacecraft_type=None):
        """
        Method for constructing a SonetSpacecraft object.
        :param a_spacecraft_type: Enum (SpacecraftType)
        :return: True if everything was ok, false otherwise.

        """
        # Convert string input to SpacecraftType enum.
        if isinstance(a_spacecraft_type, str):
            if a_spacecraft_type == 'Crewed':
                a_spacecraft_type = SpacecraftType.CREWED
            elif a_spacecraft_type == 'Cargo':
                a_spacecraft_type = SpacecraftType.CARGO

        # Check.
        if not SpacecraftType.is_valid(a_spacecraft_type):
            return False

        self._spacecraft_type = a_spacecraft_type
        return True

    # Private methods

# TODO: Convert DepDates column to readable date (e.g. YYYY-MM-DD)
# TODO: Convert theta column to readable angle (e.g. degrees)
