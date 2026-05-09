"""Run the full pipeline end-to-end: Scrape → Bronze → Silver → Gold → Warehouse."""

from shared.logging import get_logger

_log = get_logger(__name__)


def main() -> None:
    _log.info("=== STEP 1: Scraping → Bronze ===")
    from scripts.batch_scrape import main as batch_scrape
    batch_scrape()

    _log.info("=== STEP 2: Bronze → Silver ===")
    from scripts.bronze_to_silver import main as bronze_to_silver
    bronze_to_silver()

    _log.info("=== STEP 3: Silver → Gold ===")
    from scripts.silver_to_gold import main as silver_to_gold
    silver_to_gold()

    _log.info("=== STEP 4: Gold → Warehouse ===")
    from scripts.gold_to_warehouse import main as gold_to_warehouse
    gold_to_warehouse()

    _log.info("=== PIPELINE COMPLETE ===")


if __name__ == "__main__":
    main()
