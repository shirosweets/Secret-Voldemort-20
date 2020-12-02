import unittest
import db_functions as dbf
import helpers_functions as hf

# run with $ python3 unittest_deck.py

class TestDiscardCard(unittest.TestCase):
    def test_generate_new_deck_0_0(self):
        result= hf.generate_new_deck(0, 0)
        return result
    def test_encode_deck(self):
        deck_list= [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1]
        result= hf.encode_deck(deck_list)
        expected= 254779
        self.assertEqual(expected, result)
    def test_decode_deck(self):
        deck_example= 254779
        result= hf.decode_deck(deck_example)
        expected= [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1]
        self.assertEqual(expected, result)
    def test_remove_card_for_proclamation(self):
        coded_game_deck_example= 254779
        decoded_game_deck_example = hf.decode_deck(coded_game_deck_example)
        discarted_deck_example= decoded_game_deck_example
        discarted_deck_example.pop(0)
        coded_game_deck_example = hf.encode_deck(discarted_deck_example)
        result= coded_game_deck_example
        expected= 123707 
        self.assertEqual(expected, result)
    def test_example0(self):
        result= 1
        expected= 1
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()