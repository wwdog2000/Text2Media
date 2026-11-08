from src.text_utils import split_sentences

def test_split_sentences():
    parts = split_sentences("你好。世界！")
    assert parts == ["你好。", "世界！"]

def test_empty_text():
    try:
        split_sentences("   ")
    except ValueError:
        return
    assert False, "Expected ValueError"
