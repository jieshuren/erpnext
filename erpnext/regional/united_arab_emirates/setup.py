"""Minimal UAE regional setup hooks.

This fork does not ship the full UAE localization package, but core hooks and
old patches still import these symbols. Keep them as no-ops so non-UAE sites
can continue using the common buying/accounting flows.
"""


def make_custom_fields():
	return None


def setup(company=None):
	return company

