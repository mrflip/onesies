from clockwords.solver.smush import max_overlap, smush


class TestMaxOverlap:
    def test_no_overlap(self):
        assert max_overlap("one", "two") == 0     # e … t — no match

    def test_single_char_overlap(self):
        assert max_overlap("to", "one") == 1       # "o" suffix == "o" prefix

    def test_two_char_overlap(self):
        assert max_overlap("noon", "one") == 2     # "on" suffix == "on" prefix

    def test_word_is_prefix_of_next(self):
        # "six" is a 3-char prefix of "sixteen"
        assert max_overlap("six", "sixteen") == 3

    def test_identical_strings(self):
        assert max_overlap("past", "past") == 4

    def test_empty_a(self):
        assert max_overlap("", "one") == 0

    def test_empty_b(self):
        assert max_overlap("one", "") == 0


class TestSmush:
    def test_empty(self):
        assert smush([]) == ""

    def test_single_word(self):
        assert smush(["one"]) == "one"

    def test_no_overlap(self):
        # "one" ends "e", "two" starts "t" — no match
        assert smush(["one", "two"]) == "onetwo"

    def test_single_char_overlap(self):
        # "to" + "one": shared "o" → "tone"
        assert smush(["to", "one"]) == "tone"
        assert "to"  in smush(["to", "one"])
        assert "one" in smush(["to", "one"])

    def test_two_char_overlap(self):
        # "noon" + "one": shared "on" → "noone"
        assert smush(["noon", "one"]) == "noone"
        assert "noon" in smush(["noon", "one"])
        assert "one"  in smush(["noon", "one"])

    def test_word_absorbed_into_longer(self):
        # "six" is a prefix of "sixteen" → no extra characters needed
        assert smush(["six", "sixteen"]) == "sixteen"

    def test_canonical_tenoone(self):
        # ten→noon overlap "n" (len 6), tenoon→one overlap "on" (len 7)
        assert smush(["ten", "noon", "one"]) == "tenoone"

    def test_tenoone_contains_all_three(self):
        g = smush(["ten", "noon", "one"])
        assert "ten"  in g
        assert "noon" in g
        assert "one"  in g

    def test_ordering_affects_length(self):
        # ten→noon→one compresses better than one→ten→noon
        a = smush(["ten", "noon", "one"])
        b = smush(["one", "ten", "noon"])
        assert len(a) <= len(b)

    def test_accumulation_uses_full_tail(self):
        # After smushing "past"+"one" = "pastone", appending "ten":
        # max_overlap("pastone", "ten"): "e" vs "t" no, "ne" vs "te" no,
        # "one" vs "ten" no, "tone" vs "ten" no ... = 0 → "pastoneten"
        assert smush(["past", "one", "ten"]) == "pastoneten"
