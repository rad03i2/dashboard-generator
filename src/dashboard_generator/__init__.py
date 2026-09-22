"""Local, dependency-free HTML dashboard generation."""

from .core import BuildResult, DashboardError, build_dashboard, load_records

__version__ = "1.0.0"
__author__ = "Radwan Abdulhadi Ahmed (@rad03i2)"

__all__ = ["BuildResult", "DashboardError", "build_dashboard", "load_records"]
