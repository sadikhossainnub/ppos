# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "ppos"
app_title = "PPOS"
app_publisher = "Youssef Restom"
app_description = "PPOS"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "youssef@totrox.com"
app_license = "GPLv3"
required_apps = ["erpnext"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ppos/css/ppos.css"
# app_include_js = "/assets/ppos/js/ppos.js"
app_include_js = [
    "/assets/ppos/node_modules/vue/dist/vue.js",
    "/assets/ppos/node_modules/vuetify/dist/vuetify.js",
    "ppos.bundle.js",
]

# include js, css files in header of web template
# web_include_css = "/assets/ppos/css/ppos.css"
# web_include_js = "/assets/ppos/js/ppos.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "POS Profile": "ppos/api/pos_profile.js",
    "Sales Invoice": "ppos/api/invoice.js",
    "Company": "ppos/api/company.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ppos.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ppos.install.before_install"
# after_install = "ppos.install.after_install"
# before_uninstall = "ppos.uninstall.before_uninstall"
after_uninstall = "ppos.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ppos.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Sales Invoice": {
        "validate": "ppos.ppos.api.invoice.validate",
        "before_submit": "ppos.ppos.api.invoice.before_submit",
        "before_cancel": "ppos.ppos.api.invoice.before_cancel",
    },
    "Customer": {
        "validate": "ppos.ppos.api.customer.validate",
        "after_insert": "ppos.ppos.api.customer.after_insert",
    },
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ppos.tasks.all"
# 	],
# 	"daily": [
# 		"ppos.tasks.daily"
# 	],
# 	"hourly": [
# 		"ppos.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ppos.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ppos.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ppos.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ppos.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ppos.task.get_dashboard_data"
# }

# override_doctype_class = {
# "doctype": "method",
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Sales Invoice-ppos_pos_opening_shift",
                    "Item Barcode-ppos_uom",
                    "POS Profile-ppos_ppos_settings",
                    "POS Profile-ppos_allow_delete",
                    "POS Profile-ppos_allow_user_to_edit_rate",
                    "POS Profile-ppos_allow_user_to_edit_additional_discount",
                    "POS Profile-ppos_allow_user_to_edit_item_discount",
                    "POS Profile-ppos_display_items_in_stock",
                    "POS Profile-ppos_allow_submissions_in_background_job",
                    "POS Profile-ppos_allow_partial_payment",
                    "POS Profile-ppos_allow_credit_sale",
                    "POS Profile-ppos_ppos_advance_settings",
                    "Batch-ppos_batch_price",
                    "POS Profile-ppos_max_discount_allowed",
                    "POS Profile-ppos_allow_return",
                    "POS Profile-ppos_col_1",
                    "POS Profile-ppos_scale_barcode_start",
                    "Sales Invoice-ppos_is_printed",
                    "POS Profile-ppos_local_storage",
                    "POS Profile-ppos_cash_mode_of_payment",
                    "POS Profile-use_customer_credit",
                    "POS Profile-use_cashback",
                    "POS Profile-ppos_hide_closing_shift",
                    "Customer-ppos_discount",
                    "POS Profile-ppos_apply_customer_discount",
                    "Sales Invoice-ppos_offers",
                    "Sales Invoice-ppos_coupons",
                    "Sales Invoice Item-ppos_offers",
                    "Sales Invoice Item-ppos_row_id",
                    "Sales Invoice Item-ppos_offer_applied",
                    "Sales Invoice Item-ppos_is_offer",
                    "Sales Invoice Item-ppos_is_replace",
                    "POS Profile-ppos_auto_set_batch",
                    "POS Profile-ppos_search_serial_no",
                    "Sales Invoice-ppos_additional_notes_section",
                    "Sales Invoice-ppos_notes",
                    "Sales Invoice-ppos_column_break_111",
                    "Sales Invoice-ppos_delivery_date",
                    "Sales Invoice Item-ppos_notes",
                    "Sales Invoice Item-ppos_delivery_date",
                    "Sales Order-ppos_additional_notes_section",
                    "Sales Order-ppos_notes",
                    "Sales Order Item-ppos_notes",
                    "POS Profile-ppos_allow_sales_order",
                    "POS Profile-custom_allow_select_sales_order",
                    "POS Profile-ppos_column_break_112",
                    "POS Profile-ppos_show_template_items",
                    "POS Profile-ppos_hide_variants_items",
                    "Customer-ppos_referral_code",
                    "POS Profile-ppos_fetch_coupon",
                    "Company-ppos_referral_section",
                    "Company-ppos_auto_referral",
                    "Company-ppos_column_break_22",
                    "Company-ppos_customer_offer",
                    "Company-ppos_primary_offer",
                    "Company-ppos_referral_campaign",
                    "Customer-ppos_referral_company",
                    "Customer-ppos_referral_section",
                    "Customer-ppos_birthday",
                    "Sales Order-ppos_offers",
                    "Sales Order-ppos_coupons",
                    "Sales Order Item-ppos_row_id",
                    "POS Profile-ppos_tax_inclusive",
                    "POS Profile-ppos_use_percentage_discount",
                    "POS Profile-ppos_allow_customer_purchase_order",
                    "POS Profile-ppos_allow_print_last_invoice",
                    "POS Profile-ppos_display_additional_notes",
                    "POS Profile-ppos_allow_write_off_change",
                    "POS Profile-ppos_new_line",
                    "POS Profile-ppos_input_qty",
                    "POS Profile-ppos_display_item_code",
                    "POS Profile-ppos_allow_zero_rated_items",
                    "POS Profile-ppos_allow_print_draft_invoices",
                    "Address-ppos_delivery_charges",
                    "Sales Invoice-ppos_delivery_charges",
                    "Sales Invoice-ppos_delivery_charges_rate",
                    "POS Profile-ppos_auto_set_delivery_charges",
                    "POS Profile-ppos_use_delivery_charges",
                    "POS Profile-hide_expected_amount",
                    "POS Profile-ppos_allow_change_posting_date",
                    "POS Profile-ppos_default_card_view",
                    "POS Profile-ppos_default_sales_order",
                    "POS Profile-column_break_dqsba",
                    "POS Profile-ppos_use_server_cache",
                    "POS Profile-ppos_server_cache_duration",
                    "POS Profile-ppos_allow_duplicate_customer_names",
                    "POS Profile-column_break_anyol",
                    "POS Profile-pose_use_limit_search",
                    "POS Profile-ppos_search_limit",
                    "POS Profile-ppos_search_batch_no",
                    "POS Profile-ppos_payments",
                    "POS Profile-ppos_use_ppos_payments",
                    "POS Profile-ppos_allow_make_new_payments",
                    "POS Profile-ppos_allow_reconcile_payments",
                    "POS Profile-column_break_uolvm",
                    "POS Profile-ppos_allow_mpesa_reconcile_payments",
                ),
            ]
        ],
    },
    {
        "doctype": "Property Setter",
        "filters": [["name", "in", ("Sales Invoice-ppos_pos_opening_shift-no_copy")]],
    },
]
