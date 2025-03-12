from utils.mongodb import MongoCon


def results_manager(results: list[dict]) -> None:
    MongoCon().save_results(results)
