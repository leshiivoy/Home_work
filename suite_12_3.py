import unittest
import test_runner, test_tournament


my_suite = unittest.TestSuite()
my_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_runner.RunnerTest))
my_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_tournament.TournamentTest))
runner = unittest.TextTestRunner(verbosity=2)


if __name__ == "__main__":
    runner.run(my_suite)



