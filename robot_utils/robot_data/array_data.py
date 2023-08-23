import numpy as np
from robot_utils.robot_data.robot_data import RobotData
    
class ArrayData(RobotData):
    """
    Class for easy access to generic numpy array robot data over time
    """
    
    def __init__(self, time_array, data_array, interp=False, time_tol=.1, t0=None): 
        """
        Class for easy access to object poses over time

        Args:
            time_array (np.array, shape=(n,)): one dimensional time array
            data_array (np.array, shape=(n,m)): two dimensional array of data
            interp (bool, optional): interpolate between closest times, else choose the closest 
                time. Defaults to False
            time_tol (float, optional): Tolerance used when finding a pose at a specific time. If 
                no pose is available within tolerance, None is returned. Defaults to .1.
            t0 (float, optional): Local time at the first msg. If not set, uses global time from 
                the data_file. Defaults to None.
        """
        self.times = np.array(time_array)
        self._data = np.array(data_array)
        super().__init__(time_tol=time_tol, t0=t0, interp=interp)
                
    def data(self, t):
        """
        Data at time t.

        Args:
            t (float): time

        Returns:
            np.array, shape(m,): single row of data array at time t
        """
        idx = self.idx(t)
        if idx is None:
            return None
        if self.interp:
            if np.allclose(*self.times[idx].tolist()):
                return self._data[idx[0],:]
            else:
                return self._data[idx[0]] + \
                    (self._data[idx[1],:] - self._data[idx[0],:]) * \
                    (t - self.times[idx[0]]) / (self.times[idx[1]] - self.times[idx[0]])
        else:
            return self._data[idx,:]