"""Test for the function generate_gaussian_dfl(...) from ocelot.optics.wave"""

import copy
import os
import sys
import time

import numpy as np
from generate_gaussian_dfl_conf import *

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
REF_RES_DIR = FILE_DIR + os.path.sep + 'ref_results' + os.path.sep
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(FILE_DIR))))

from params import *
import ocelot.optics.wave as wave


@pytest.mark.parametrize('parameter', range(3))
def test_generate_gaussian_dfl(args_array_ref, parameter, update_ref_values=False):
    """generate_gaussian_dfl() function testing"""

    (args_ref, kwargs_ref) = args_array_ref[parameter]
    dfl = wave.generate_gaussian_dfl(*args_ref, **kwargs_ref).fld

    if update_ref_values:
        return dfl
    else:
        dfl_array_ref = np.load(REF_RES_DIR + sys._getframe().f_code.co_name + str(parameter) + '.npy')
        
        dfl_ref = dfl_array_ref

    result = check_matrix(dfl, dfl_ref, TOL, tolerance_type='relative',
                          assert_info='- generate_gaussian_dfl(){parameter}'.format(parameter))
    assert check_result(result)


def setup_module(module):
    f = open(pytest.TEST_RESULTS_FILE, 'a')
    f.write('### GENERATE_GAUSSIAN_DFL START ###\n\n')
    f.close()


def teardown_module(module):
    f = open(pytest.TEST_RESULTS_FILE, 'a')
    f.write('### GENERATE_GAUSSIAN_DFL END ###\n\n\n')
    f.close()


def setup_function(function):
    f = open(pytest.TEST_RESULTS_FILE, 'a')
    f.write(function.__name__)
    f.close()

    pytest.t_start = time.time()


def teardown_function(function):
    f = open(pytest.TEST_RESULTS_FILE, 'a')
    f.write(' execution time is ' + '{:.3f}'.format(time.time() - pytest.t_start) + ' sec\n\n')
    f.close()


@pytest.mark.update
def test_update_ref_values(args_array_ref, cmdopt):
    update_functions = []
    update_functions.append('test_generate_gaussian_dfl')

    update_function_parameters = {}
    update_function_parameters['test_generate_gaussian_dfl'] = range(3)

    parameter = update_function_parameters[cmdopt] if cmdopt in update_function_parameters.keys() else ['']

    if cmdopt in update_functions:
        for p in parameter:
            args_array = copy.deepcopy(args_array_ref)
            result = eval(cmdopt)(args_array, p, True)

            if os.path.isfile(REF_RES_DIR + cmdopt + str(p) + '.npy'):
                os.rename(REF_RES_DIR + cmdopt + str(p) + '.npy', REF_RES_DIR + cmdopt + str(p) + '.old')

            np.save(REF_RES_DIR + cmdopt + str(p) + '.npy', result)
