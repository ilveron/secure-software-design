import dataclasses
from dataclasses import InitVar
from pathlib import Path
from typing import Any
from unittest.mock import patch, mock_open, Mock, call

import pytest
import typeguard

from dealer.app import App, main


@pytest.fixture
def mock_path():
    Path.exists = Mock()
    Path.exists.return_value = True
    return Path


@pytest.fixture
def data():
    data = [
        ['Car', 'CA220NE', 'Fiat', 'Punto', '199.99'],
        ['Moto', 'CA220NI', 'Kawasaki', 'Ninja', '99.99'],
    ]
    return '\n'.join(['\t'.join(d) for d in data])


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_main(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exists:
        mocked_path_exists.return_value = False
        with patch('builtins.open', mock_open()):
            main('__main__')
            mocked_print.assert_any_call('*** LaRusso Auto Group ***')
            mocked_print.assert_any_call('0:\tExit')
            mocked_print.assert_any_call('Bye!')
            mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_load_datafile(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)):
        App().run()
    mock_path.exists.assert_called_once()
    assert list(filter(lambda x: 'CA220NE' in str(x), mocked_print.mock_calls))
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_handles_corrupted_datafile(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open(read_data='xyz')):
        App().run()
    mocked_print.assert_any_call('Continuing with an empty list of vehicles...')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_handles_unknown_type_in_datafile(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open(read_data='Airplane\tCA220NE\tFiat\tPunto\t199.99')):
        App().run()
    mocked_print.assert_any_call('Continuing with an empty list of vehicles...')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', 'CA220NE', 'Fiat', 'Punto', '199.99', '0'])
@patch('builtins.print')
def test_app_add_car(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'CA220NE' in str(x), mocked_print.mock_calls))

    handle = mocked_open()
    handle.write.assert_called_once_with('Car\tCA220NE\tFiat\tPunto\t199.99\n')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', 'ca220ne', 'CA220NE', 'Fiat', 'Punto', '199.99', '0'])
@patch('builtins.print')
def test_app_add_car_resists_to_wrong_plate(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'CA220NE' in str(x), mocked_print.mock_calls))
    mocked_input.assert_called()

    handle = mocked_open()
    handle.write.assert_called_once_with('Car\tCA220NE\tFiat\tPunto\t199.99\n')


@patch('builtins.input', side_effect=['2', 'CA220NI', 'Kawasaki', 'Ninja', '1000.00', '0'])
@patch('builtins.print')
def test_app_add_moto(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'CA220NI' in str(x), mocked_print.mock_calls))
    mocked_input.assert_called()

    handle = mocked_open()
    handle.write.assert_called_once_with('Moto\tCA220NI\tKawasaki\tNinja\t1000.00\n')


@patch('builtins.input', side_effect=['3', '1', '0'])
@patch('builtins.print')
def test_app_remove_vehicle(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)) as mocked_open:
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_called()

    handle = mocked_open()
    handle.write.assert_called_once_with('Moto\tCA220NI\tKawasaki\tNinja\t99.99\n')


@patch('builtins.input', side_effect=['3', '0', '0'])
@patch('builtins.print')
def test_app_remove_vehicle_can_be_cancelled(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Cancelled!')


@patch('builtins.input', side_effect=['5', '0'])
@patch('builtins.print')
def test_app_sort_by_price(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)) as mocked_open:
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_called()

    handle = mocked_open()
    assert handle.write.mock_calls == [
        call('Moto\tCA220NI\tKawasaki\tNinja\t99.99\n'),
        call('Car\tCA220NE\tFiat\tPunto\t199.99\n'),
    ]


@patch('builtins.input', side_effect=['5', '4', '0'])
@patch('builtins.print')
def test_app_sort_by_producer(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)) as mocked_open:
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_called()

    handle = mocked_open()
    assert handle.write.mock_calls == [
        call('Moto\tCA220NI\tKawasaki\tNinja\t99.99\n'),
        call('Car\tCA220NE\tFiat\tPunto\t199.99\n'),
        call('Car\tCA220NE\tFiat\tPunto\t199.99\n'),
        call('Moto\tCA220NI\tKawasaki\tNinja\t99.99\n'),
    ]


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_global_exception_handler(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exits:
        mocked_path_exits.side_effect = Mock(side_effect=Exception('Test'))
        App().run()
    assert mocked_input.mock_calls == []
    assert list(filter(lambda x: 'Panic error!' in str(x), mocked_print.mock_calls))
