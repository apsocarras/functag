from functag import annotate


def test_annotate():
    @annotate(**{"my_key": "my_value"}, my_key_2="my_value_2")
    def function_to_annotate(self=None) -> tuple[str]:
        return (self.my_key, self.my_key_2)

    x = function_to_annotate()
    assert x[0] == "my_value" == function_to_annotate.my_key
    assert x[1] == "my_value_2" == function_to_annotate.my_key_2
