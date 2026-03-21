"""Collector module - exports all collectors."""

from src.collector.base import BaseCollector
from src.collector.crunchbase import CrunchbaseClient
from src.collector.angellist import AngelListClient
from src.collector.rss import RSSCollector

__all__ = [
    "BaseCollector",
    "CrunchbaseClient",
    "AngelListClient",
    "RSSCollector",
]
