import pytest

from calculator import calculate_prefix
from calculator import calculate_infix


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
        assert calculate_prefix("3") == 3

    def test_base_case(self):
        assert calculate_prefix("+ 1 2") == 3

    @pytest.mark.parametrize("case, expected", [
        ("+ 1 * 2 3", 7),
        ("+ * 1 2 3", 5),
        ("- / 10 + 1 1 * 1 2", 3),
        ("- / 100 + 1 1 * 1 2", 48),
        ("- 0 3", -3),
        ("/ 3 2", 1.5),
    ])
    def test_nested_cases(self, case, expected):
        assert calculate_prefix(case) == expected

    def test_empty_string(self):
        with pytest.raises(ValueError):
            calculate_prefix("")

    @pytest.mark.parametrize("case", non_string_input)
    def test_non_string(self, case):
        with pytest.raises(ValueError):
            calculate_prefix(case)

    def test_additional_whitespace(self):
        assert calculate_prefix("     +    1   2    ") == 3

    @pytest.mark.parametrize("case", [
        "+ 1 2 3",
        "+ 1 2 3 4",
    ])
    def test_additional_digits(self, case):
        with pytest.raises(ValueError):
            calculate_prefix(case)

    def test_additional_operators(self):
        with pytest.raises(ValueError):
            calculate_prefix("+ - * 1 2")

    def test_unknown_operator(self):
        with pytest.raises(ValueError):
            calculate_prefix("& 1 2")


class TestInfixCalc:
    def test_single_number(self):
        assert calculate_infix("( 3 )") == 3

    def test_base_case(self):
        assert calculate_infix("( 1 + 2 )") == 3

    @pytest.mark.parametrize("case, expected", [
        ("( 10 + ( 2 * 3 ) )", 16),
        ("( ( 1 * 2 ) + 3 )", 5),
        ("( ( ( 1 + 1 ) / 10 ) - ( 1 * 2 ) )", -1.8),
    ])
    def test_nested_cases(self, case, expected):
        assert calculate_infix(case) == expected

    def test_empty_string(self):
        with pytest.raises(ValueError):
            calculate_infix("")

    @pytest.mark.parametrize("case", non_string_input)
    def test_non_string(self, case):
        with pytest.raises(ValueError):
            calculate_infix(case)

    def test_additional_whitespace(self):
        assert calculate_infix("     (    1   +  2     )  ") == 3

    @pytest.mark.parametrize("case", [
        "( 1 + 2 2 )",
        "( 1 1 + 2 )",
    ])
    def test_additional_digits(self, case):
        with pytest.raises(ValueError):
            calculate_infix(case)

    @pytest.mark.parametrize("case, expected", [
        ("( ( 1 ) + ( 2 ) )", 3),
        ("( ( ( ( 1 + 2 ) ) ) )", 3),
    ])
    def test_additional_brackets(self, case, expected):
        assert calculate_infix(case) == expected

    def test_additional_operators(self):
        with pytest.raises(ValueError):
            calculate_infix("( 1 + * 2 )")

    def test_unknown_operator(self):
        with pytest.raises(ValueError):
            calculate_infix("( 1 & 2 )")

    @pytest.mark.parametrize("case", [
        ") 1 + 2 (",
        ")( 1 + 2 )",
        "( 1 + 2 ))",
    ])
    def test_bracket_mismatch(self, case):
        with pytest.raises(ValueError):
            calculate_infix(case)

