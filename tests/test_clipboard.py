import pytest

from passpie import clipboard


def test_clipboard_on_osx_ensure_commands(mocker):
    mocker.patch('passpie.clipboard.Popen')
    mock_ensure_commands = mocker.patch('passpie.clipboard.ensure_commands')
    commands = clipboard.OSX_COMMANDS

    clipboard._copy_osx('text')

    mock_ensure_commands.assert_called_once_with(commands)


def test_clipboard_on__ensure_commands(mocker):
    mocker.patch('passpie.clipboard.Popen')
    mock_ensure_commands = mocker.patch('passpie.clipboard.ensure_commands')
    commands = clipboard.LINUX_COMMANDS

    clipboard._copy_linux('text')

    mock_ensure_commands.assert_called_once_with(commands)


def test_copy_calls_copy_osx_when_on_darwin_system(mocker):
    mocker.patch('passpie.clipboard.Popen')
    mocker.patch('passpie.clipboard.platform.system', return_value='Darwin')
    mock_copy_osx = mocker.patch('passpie.clipboard._copy_osx')
    mock_copy_linux = mocker.patch('passpie.clipboard._copy_linux')
    mock_copy_windows = mocker.patch('passpie.clipboard._copy_windows')

    clipboard.copy('text')

    assert mock_copy_osx.called is True
    assert mock_copy_linux.called is False
    assert mock_copy_windows.called is False
    mock_copy_osx.assert_called_once_with('text')


def test_copy_calls_copy_linux_when_on_linux_system(mocker):
    mocker.patch('passpie.clipboard.Popen')
    mocker.patch('passpie.clipboard.platform.system', return_value='Linux')
    mock_copy_osx = mocker.patch('passpie.clipboard._copy_osx')
    mock_copy_linux = mocker.patch('passpie.clipboard._copy_linux')
    mock_copy_windows = mocker.patch('passpie.clipboard._copy_windows')

    clipboard.copy('text')

    assert mock_copy_linux.called is True
    assert mock_copy_osx.called is False
    assert mock_copy_windows.called is False
    mock_copy_linux.assert_called_once_with('text')


def test_copy_calls_copy_windows_when_on_windows_system(mocker):
    mocker.patch('passpie.clipboard.Popen')
    mocker.patch('passpie.clipboard.platform.system', return_value='Windows')
    mock_copy_osx = mocker.patch('passpie.clipboard._copy_osx')
    mock_copy_linux = mocker.patch('passpie.clipboard._copy_linux')
    mock_copy_windows = mocker.patch('passpie.clipboard._copy_windows')

    clipboard.copy('text')

    assert mock_copy_windows.called is True
    assert mock_copy_osx.called is False
    assert mock_copy_linux.called is False
    mock_copy_windows.assert_called_once_with('text')


def test_copy_calls_copy_cygwin_when_on_cygwin_system(mocker):
    mocker.patch('passpie.clipboard.platform.system', return_value='cygwin system')
    mock_copy_cygwin = mocker.patch('passpie.clipboard._copy_cygwin')
    text = 's3cr3t'

    clipboard.copy(text)

    assert mock_copy_cygwin.called
    mock_copy_cygwin.assert_called_once_with(text)


def test_copy_calls_copy_cygwin_when_on_cygwin_system(mocker):
    mocker.patch('passpie.clipboard.platform.system', return_value='cygwin system')
    mock_copy_cygwin = mocker.patch('passpie.clipboard._copy_cygwin')
    text = 's3cr3t'

    clipboard.copy(text)

    assert mock_copy_cygwin.called
    mock_copy_cygwin.assert_called_once_with(text)

def test_logs_error_msg_when_platform_not_supported(mocker):
    mocker.patch('passpie.clipboard.platform.system', return_value='unknown')
    mock_logger = mocker.patch('passpie.clipboard.logger')

    clipboard.copy('text')
    assert mock_logger.error.called
    msg = "platform 'unknown' copy to clipboard not supported"
    mock_logger.error.assert_called_once_with(msg)

def test_ensure_commands_raises_system_error_when_command_not_found(mocker):
    mocker.patch('passpie.clipboard.which', return_value=False)

    with pytest.raises(SystemError):
        clipboard.ensure_commands(clipboard.LINUX_COMMANDS)


def test_ensure_commands_raises_system_error_when_no_command_args(mocker):
    mocker.patch('passpie.clipboard.which', return_value=True)
    mock_commands = {k: [] for k, _ in clipboard.LINUX_COMMANDS.items()}

    with pytest.raises(SystemError):
        clipboard.ensure_commands(mock_commands)


def test_ensure_commands_returns_command(mocker):
    commands = {'xclip': ['xclip']}
    mocker.patch('passpie.clipboard.which', return_value=True)

    result = clipboard.ensure_commands(commands)

    assert result == commands['xclip']
