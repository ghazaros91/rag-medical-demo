from memory import SessionMemory

def test_memory_store_and_retrieve():
    mem = SessionMemory()
    mem.add("hello", "world")

    ctx = mem.context()
    assert "hello" in ctx
    assert "world" in ctx

def test_memory_empty_handling():
    mem = SessionMemory()
    assert mem.context() == ""
