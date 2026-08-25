from builder.builder.doctype.builder_token.builder_token import get_css_variables

# OA-Method fork patch (framework#107, moved here from variables.py in framework#126 when
# upstream made this the canonical route). Without it frappe serves this route with the default
# website headers — `max-age=300, stale-while-revalidate=10800` — so a browser shows the STALE
# tokens for up to 5 minutes and then, for the next 3 hours, serves the old copy while fetching
# the new one in the background. The visible symptom is a one-step lag: the client changes a
# brand colour and sees nothing, changes it back and sees the previous colour appear.
#
# NOT covered by upstream's `delete_page_cache("builder_assets/variables.css")` in
# clear_builder_token_cache — that busts frappe's SERVER-SIDE Redis page cache, which is a
# different layer and is invisible to a browser holding a stale-while-revalidate copy.
#
# It cannot be absorbed by a cache-buster either — builder/templates/generators/webpage.html
# links this route bare, with no `?v=`, unlike Builder's own generated stylesheet.
#
# These are the client's own brand edits, so a stale response reads as "the product is broken".
# The file is a handful of custom properties regenerated per request; the cost is negligible.
no_cache = 1


def get_context(context):
	css_variables, dark_mode_css_variables = get_css_variables()
	context.css_variables = css_variables
	context.dark_mode_css_variables = dark_mode_css_variables
