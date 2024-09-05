import runner_and_tournament
import unittest


class TournamentTest(unittest.TestCase):
    @unittest.skipIf(True, 'Тесты в этом кейсе заморожены')
    def test_start_tour_1(self):
        tour = runner_and_tournament.Tournament(90, self.usain, self.nick)
        results = tour.start()
        last_runner = list(results.values())
        self.assertTrue(last_runner[-1] == "Ник")
        self.all_results[self.shortDescription()] = results

    @unittest.skipIf(True, 'Тесты в этом кейсе заморожены')
    def test_start_tour_2(self):
        tour = runner_and_tournament.Tournament(90, self.andrew, self.nick)
        results = tour.start()
        last_runner = list(results.values())
        self.assertTrue(last_runner[-1] == "Ник")
        self.all_results[self.shortDescription()] = results

    @unittest.skipIf(True, 'Тесты в этом кейсе заморожены')
    def test_start_tour_3(self):
        tour = runner_and_tournament.Tournament(90, self.andrew, self.usain, self.nick)
        results = tour.start()
        last_runner = list(results.values())
        self.assertTrue(last_runner[-1] == "Ник")
        self.all_results[self.shortDescription()] = results