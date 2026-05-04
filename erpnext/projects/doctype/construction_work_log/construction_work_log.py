import frappe
from frappe.model.document import Document


class ConstructionWorkLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		artificial_bottom: DF.Float
		blocked_depth: DF.Float
		cement_return_height: DF.Float
		channel_finding_hours: DF.Float
		construction_process: DF.LongText | None
		diesel_info: DF.SmallText | None
		drill_pipe_73_count: DF.Int
		drill_pipe_count: DF.Int
		employee: DF.Link | None
		fishing_hours: DF.Float
		footage: DF.Float
		forging_milling_hours: DF.Float
		hired_vehicle_cost: DF.Data | None
		kelly_count: DF.Int
		manager: DF.SmallText | None
		material_cost: DF.Data | None
		milling_after_depth: DF.Float
		milling_hours: DF.Float
		next_plan: DF.SmallText | None
		oil_added_pump: DF.Float
		oil_added_vehicle: DF.Float
		perforation_interval: DF.Data | None
		pre_shift_meeting: DF.SmallText | None
		project: DF.Link
		project_name: DF.Data | None
		pump_forging_milling_hours: DF.Float
		pump_idle_hours: DF.Float
		pump_milling_hours: DF.Float
		pump_oil_remaining: DF.Data | None
		pump_sand_flushing_hours: DF.Float
		pump_total_hours: DF.Float
		raw_report: DF.LongText | None
		repair_cost: DF.Data | None
		reporter: DF.Data | None
		rig_idle_hours: DF.Float
		rig_total_hours: DF.Float
		risk: DF.SmallText | None
		sand_flushing_hours: DF.Float
		shift: DF.Literal["\u767d\u73ed", "\u591c\u73ed", "\u5168\u5929", "\u5176\u4ed6"]
		standby_hours: DF.Float
		status: DF.Literal["Draft", "Submitted", "Reviewed", "Closed"]
		task: DF.Link | None
		team: DF.Data | None
		total_tools_count: DF.Int
		tripping_hours: DF.Float
		tubing_62_count: DF.Int
		vehicle_oil_remaining: DF.Data | None
		well_no: DF.Data
		work_date: DF.Date
		work_time: DF.Data | None
		workload_summary: DF.SmallText | None
	# end: auto-generated types

	def validate(self):
		if self.project and not self.project_name:
			self.project_name = frappe.db.get_value("Project", self.project, "project_name") or self.project
		if self.status == "Draft" and self.docstatus == 1:
			self.status = "Submitted"
