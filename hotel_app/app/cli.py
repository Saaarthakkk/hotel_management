# PLAN: register housekeeping scheduler CLI command
from __future__ import annotations

import click
import logging
from datetime import date

from .services.housekeeping_scheduler import HousekeepingScheduler
from .services.housekeeping_service import HousekeepingService
from .services.overbooking_service import OverbookingService
from .utils import setup_logger

logger = setup_logger(__name__, 'cli.log')


def init_cli(app) -> None:
    """Attach hk schedule command to the Flask app."""

    @app.cli.command('hk')
    @click.option('--date', 'target', default=date.today().isoformat())
    def schedule(target: str) -> None:
        """Generate and apply housekeeping schedule."""
        target_date = date.fromisoformat(target)
        schedule = HousekeepingScheduler.generate_schedule(target_date)
        for uid, tids in schedule.items():
            for tid in tids:
                HousekeepingService.assign_task(tid, uid)
        logger.info('schedule %s', schedule)
        click.echo(schedule)

    @app.cli.command('hk_recurring')
    @click.option('--room', required=True, type=int)
    @click.option('--start', required=True)
    @click.option('--end', required=True)
    @click.option('--interval', required=True, type=int)
    def recurring(room: int, start: str, end: str, interval: int) -> None:
        """Create recurring housekeeping tasks."""
        start_d = date.fromisoformat(start)
        end_d = date.fromisoformat(end)
        tasks = HousekeepingService.schedule_recurring_task(
            room, start_d, end_d, interval
        )
        click.echo({t.id for t in tasks})

    @app.cli.group()
    def revenue() -> None:
        """Revenue related commands."""

    @revenue.command('oversell')
    @click.argument('target')
    def oversell(target: str) -> None:
        target_date = date.fromisoformat(target)
        limit = OverbookingService.compute_limit(target_date)
        OverbookingService.record_plan(target_date, limit)
        click.echo(limit)
