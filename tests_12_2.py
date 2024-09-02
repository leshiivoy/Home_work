import unittest


class TournamentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    @classmethod
    def tearDownClass(cls):
        out ={}
        for key, value in cls.all_results.items():
            for k, v in value.items():
                out[k] = str(v)
            print(value)

    def setUp(self):
        """Переменные для теста"""
        self.usain = runner_and_tournament.Runner("Усэйн", 10)
        self.andrew = runner_and_tournament.Runner("Андрей", 9)
        self.nick = runner_and_tournament.Runner("Ник", 3)
        print("Переменные имена [" + self.shortDescription() + "]")

    def test_start_tour_1(self):
        """первый забег"""
        print("id: " + self.id())
        tour = runner_and_tournament.Tournament(90, self.usain, self.nick)
        results = tour.start()
        last_runner = list(results.values())
        self.assertTrue(last_runner[-1] == "Ник")
        self.all_results[self.shortDescription()] = results

    def test_start_tour_2(self):
        """второй забег"""
        print("id: " + self.id())
        tour = runner_and_tournament.Tournament(90, self.andrew, self.nick)
        results = tour.start()
        last_runner = list(results.values())
        self.assertTrue(last_runner[-1] == "Ник")
        self.all_results[self.shortDescription()] = results

    def test_start_tour_3(self):
        """третий забег"""
        print("id: " + self.id())
        tour = runner_and_tournament.Tournament(90, self.andrew, self.usain, self.nick)
        results = tour.start()
        last_runner = list(results.values())
        self.assertTrue(last_runner[-1] == "Ник")
        self.all_results[self.shortDescription()] = results


if __name__ == "__main__":
    unittest.main()