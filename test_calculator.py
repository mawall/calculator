import pytest

from calculator import prefix_calc
from calculator import infix_calc


non_string_input = [
        12,
        12.0,
        1j,
        [1, 2],
        {'a': 1, 'b': 2},
        False,
        b"bytes",
]


class TestPrefixCalc:
    def test_single_number(self):
        assert prefix_calc("3") == 3

    def test_base_case(self):
        assert prefix_calc("+ 1 2") == 3

    @pytest.mark.parametrize("case, expected", [
        ("+ 1 * 2 3", 7),
        ("+ * 1 2 3", 5),
        ("- / 10 + 1 1 * 1 2", 3),
        ("- / 100 + 1 1 * 1 2", 48),
        ("- 0 3", -3),
        ("/ 3 2", 1.5),
    ])
    def test_nested_cases(self, case, expected):
        assert prefix_calc(case) == expected

    def test_empty_string(self):
        with pytest.raises(ValueError):
            prefix_calc("")

    @pytest.mark.parametrize("case", non_string_input)
    def test_non_string(self, case):
        with pytest.raises(ValueError):
            prefix_calc(case)

    def test_additional_whitespace(self):
        assert prefix_calc("     +    1   2    ") == 3

    @pytest.mark.parametrize("case", [
        "+ 1 2 3",
        "+ 1 2 3 4",
    ])
    def test_additional_digits(self, case):
        with pytest.raises(ValueError):
            prefix_calc(case)

    def test_additional_operators(self):
        with pytest.raises(ValueError):
            prefix_calc("+ - * 1 2")

    def test_unknown_operator(self):
        with pytest.raises(ValueError):
            prefix_calc("& 1 2")


class TestInfixCalc:
    def test_single_number(self):
        assert infix_calc("( 3 )") == 3

    def test_base_case(self):
        assert infix_calc("( 1 + 2 )") == 3

    @pytest.mark.parametrize("case, expected", [
        ("( 1 + ( 2 * 3 ) )", 7),
        ("( ( 1 * 2 ) + 3 )", 5),
        ("( ( ( 1 + 1 ) / 10 ) - ( 1 * 2 ) )", -1.8),
    ])
    def test_nested_cases(self, case, expected):
        assert infix_calc(case) == expected

    def test_empty_string(self):
        with pytest.raises(ValueError):
            infix_calc("")

    @pytest.mark.parametrize("case", non_string_input)
    def test_non_string(self, case):
        with pytest.raises(ValueError):
            infix_calc(case)

    def test_additional_whitespace(self):
        assert infix_calc("     (    1   +  2     )  ") == 3

    @pytest.mark.parametrize("case", [
        "( 1 + 2 2 )",
        "( 1 1 + 2 )",
    ])
    def test_additional_digits(self, case):
        with pytest.raises(ValueError):
            infix_calc(case)

    @pytest.mark.parametrize("case, expected", [
        ("( ( 1 ) + ( 2 ) )", 3),
        ("( ( ( ( 1 + 2 ) ) ) )", 3),
    ])
    def test_additional_brackets(self, case, expected):
        assert infix_calc(case) == expected

    def test_additional_operators(self):
        with pytest.raises(ValueError):
            infix_calc("( 1 + * 2 )")

    def test_unknown_operator(self):
        with pytest.raises(ValueError):
            infix_calc("( 1 & 2 )")

    @pytest.mark.parametrize("case", [
        ") 1 + 2 (",
        ")( 1 + 2 )",
        "( 1 + 2 ))",
    ])
    def test_bracket_mismatch(self, case):
        with pytest.raises(ValueError):
            infix_calc(case)

