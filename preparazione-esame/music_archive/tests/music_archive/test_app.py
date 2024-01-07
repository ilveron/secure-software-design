from unittest.mock import patch, Mock, mock_open

import pytest

import utils.constants
from music_archive.app import *


@pytest.fixture(scope='module')
def mock_path():
    Path.exists = Mock()
    Path.exists.return_value = True
    return Path


@pytest.fixture(scope='module')
def data():
    data = [
        ['The Police', 'Murder by Numbers', 'New Wave', '4:36'],
        ['Coldplay', 'Paradise', 'Pop Rock', '4:39'],
        ['Stone Temple Pilots', 'Plush', 'Grunge', '5:13']
    ]
    return '\n'.join(['\t'.join(d) for d in data])


@patch('builtins.print')
def test_print_sep(mocked_print):
    print_sep()
    mocked_print.assert_any_call('-' * 95)


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_main(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exists:
        mocked_path_exists.return_value = False
        with patch('builtins.open', mock_open()):
            main('__main__')
            mocked_print.assert_any_call(utils.constants.MENU_DESCRIPTION)
            mocked_print.assert_any_call('0:\tExit')
            mocked_print.assert_any_call('See you soon!')


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_load_datafile(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)):
        App().run()
    mock_path.exists.assert_called_once()
    assert list(filter(lambda x: 'Murder by Numbers' in str(x), mocked_print.mock_calls))
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_handles_corrupted_datafile(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open(read_data='xyz')):
        App().run()
    mocked_print.assert_any_call('There are songs in the archive!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', 'Alan Sorrenti', 'Figli delle Stelle', 'Pop', '4:22'])
@patch('builtins.print')
def test_app_add_song(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Figli delle Stelle' in str(x), mocked_print.mock_calls))

    handle = mocked_open()
    handle.write.assert_called_once_with('Alan Sorrenti\tFigli delle Stelle\tPop\t4:22\n')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '[This does not comply]', 'System Of A Down', 'Chop Suey!', 'Chop Suey', '@Metal', 'Nu Metal', '3:30'])
@patch('builtins.print')
def test_app_add_song_resists_to_wrong_inputs(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Nu Metal' in str(x), mocked_print.mock_calls))

    handle = mocked_open()
    handle.write.assert_called_once_with('System Of A Down\tChop Suey\tNu Metal\t3:30\n')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_global_exception_handler(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exists:
        mocked_path_exists.side_effect = Mock(side_effect=Exception('Test'))
        App().run()
    assert mocked_input.mock_calls == []
    assert list(filter(lambda x: 'Panic error!' in str(x), mocked_print.mock_calls))


@patch('builtins.input', side_effect=['2', '1'])
@patch('builtins.print')
def test_app_remove_song_with_correct_index_removes_it_correctly(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)):
        App().run()
    mocked_print.assert_any_call('Song removed!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['2', '0'])
@patch('builtins.print')
def test_app_remove_song_with_index_0_cancels_operation(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_print.assert_any_call('Cancelled!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['2', '4', '1'])
@patch('builtins.print')
def test_app_remove_song_with_out_of_bound_index_handled_correctly(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)):
        App().run()
    assert list(filter(lambda x: 'Wrong value' in str(x), mocked_print.mock_calls))
    mocked_print.assert_any_call('Song removed!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['7', 'Coldplay'])
@patch('builtins.print')
def test_app_filter_by_author(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)):
        App().run()
    # I Coldplay appariranno tra le stampe una volta nella lista complessiva ed una volta nella lista filtrata (== 2)
    assert len(list(filter(lambda x: 'Coldplay' in str(x), mocked_print.mock_calls))) == 2
    mocked_input.assert_called()
