class TestClass:
    def test_input_phrase(self):
        phrase = input("Set a phrase:")
        assert len(phrase) < 15, "Phrase length is 15 or more symbols"