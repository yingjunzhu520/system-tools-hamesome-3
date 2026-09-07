import pytest

from greetlab.cli import main


def test_blank_name_exits_code_2(monkeypatch):
    """当 --name 只含空白字符时，main 应以 SystemExit(2) 结束。"""
    monkeypatch.setattr("sys.argv", ["sdt-greet", "--name", "   "])
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 2


def test_normal_name_prints_greeting(monkeypatch, capsys):
    """正常姓名应打印问候语，且不抛出异常。"""
    monkeypatch.setattr("sys.argv", ["sdt-greet", "--name", "Alice"])
    main()
    assert capsys.readouterr().out == "Hello, Alice!\n"
