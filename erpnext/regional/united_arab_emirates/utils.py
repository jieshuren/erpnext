"""No-op UAE regional helpers for non-UAE deployments."""


def update_grand_total_for_rcm(doc, method=None):
	return doc


def validate_returns(doc, method=None):
	return doc


def update_itemised_tax_data(doc):
	return doc


def make_regional_gl_entries(gl_entries, doc):
	return gl_entries
