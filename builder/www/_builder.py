import frappe
from frappe.integrations.frappe_providers.frappecloud_billing import is_fc_site
from frappe.pulse.utils import get_app_version
from frappe.utils.telemetry import capture

from builder.hooks import builder_path

no_cache = 1


def get_context(context):
	csrf_token = frappe.sessions.get_csrf_token()
	frappe.db.commit()
	context.csrf_token = csrf_token
	context.site_name = frappe.local.site
	context.builder_path = builder_path
	context.builder_version = get_app_version("builder")
	# developer mode
	context.is_developer_mode = frappe.conf.developer_mode
	context.is_fc_site = is_fc_site()
	context.is_read_only_mode = bool(frappe.flags.read_only)
	# OA-Method fork patch (framework#107). The editor SPA never loads the global stylesheet —
	# `builderSettings.style` has zero references in frontend/src — so the canvas renders
	# unstyled scaffolding while the published page looks right. Passing the versioned URL lets
	# the shell link it, so what the client sees while editing IS what publishes.
	# Versioned (not the bare path) so a settings change is not masked by a stale cached sheet,
	# which would recreate the same divergence in a subtler form.
	context.builder_style_url = frappe.db.get_single_value("Builder Settings", "style_public_url")
	if frappe.session.user != "Guest":
		capture("active_site", "builder")
