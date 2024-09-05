import unittest
import runner_and_tournament


class RunnerTest(unittest.TestCase):

    @unittest.skipIf(False, 'Тесты в этом кейсе заморожены')
    def test_walk(self):
        rn = runner_and_tournament.Runner("child")
        for i in range(10):
            rn.walk()
        self.assertEqual(rn.distance, 50)

    @unittest.skipIf(False, 'Тесты в этом кейсе заморожены')
    def test_run(self):
        rn1 = runner_and_tournament.Runner("Auto")
        for i in range(10):
            rn1.run()
        self.assertEqual(rn1.distance, 100)

    @unittest.skipIf(False, 'Тесты в этом кейсе заморожены')
    def test_challenge(self):
        rn2 = runner_and_tournament.Runner("man")
        rn3 = runner_and_tournament.Runner("bicycle")
        for i in range(10):
            rn2.walk()
            rn3.run()
        self.assertNotEqual(rn2.distance, rn3.distance)