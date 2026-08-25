# Compat route: pages published before the Builder Token rename link
# /builder_assets/variables.css. Serves the same CSS as tokens.css.
from builder.www.builder_assets.tokens import get_context

# OA-Method fork patch (framework#107, re-applied for framework#126). `no_cache` is read from
# the ROUTE module, so re-exporting get_context does not carry it across from tokens.py — this
# compat route needs its own. See tokens.py for why it exists at all.
no_cache = 1

__all__ = ["get_context"]
