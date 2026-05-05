import frappe
import json
from frappe import _
from frappe.utils import cint

def get_current_employee_info() -> dict:
	current_user = frappe.session.user
	employee = frappe.db.get_value(
		"Employee",
		{"user_id": current_user, "status": "Active"},
		[
			"name",
			"first_name",
			"employee_name",
			"designation",
			"department",
			"company",
			"reports_to",
			"user_id",
		],
		as_dict=True,
	)
	return employee or {}

def _mobile_float(value) -> float:
	try:
		return float(value or 0)
	except (TypeError, ValueError):
		return 0.0

def _mobile_int(value) -> int:
	try:
		return int(float(value or 0))
	except (TypeError, ValueError):
		return 0

def _get_default_company_for_mobile(employee: dict | None = None) -> str | None:
	return (employee or {}).get("company") or frappe.db.get_single_value("Global Defaults", "default_company")

def _get_or_create_project_for_mobile(well_no: str, project: str | None = None, project_name: str | None = None) -> str:
	project = (project or "").strip()
	well_no = (well_no or "").strip()
	project_name = (project_name or well_no or project).strip()
	if project:
		if not frappe.db.exists("Project", project):
			return project
		return project

	if not project_name:
		frappe.throw(_("Please enter Well No or Project Name"))

	existing = frappe.db.get_value("Project", {"project_name": project_name}, "name")
	if existing:
		return existing

	employee = get_current_employee_info()
	doc = frappe.get_doc({
		"doctype": "Project",
		"project_name": project_name,
		"status": "Open",
		"percent_complete_method": "Task Progress",
		"company": _get_default_company_for_mobile(employee),
		"department": employee.get("department"),
	})
	doc.insert(ignore_permissions=True)
	return doc.name

def _get_or_create_activity_type(activity_type: str) -> str:
	activity_type = (activity_type or "施工管理").strip()
	if not frappe.db.exists("Activity Type", activity_type):
		doc = frappe.get_doc({"doctype": "Activity Type", "activity_type": activity_type})
		doc.insert(ignore_permissions=True)
	return activity_type

def _create_or_update_task_for_log(project: str, data: dict) -> str:
	work_date = data.get("work_date")
	shift = data.get("shift") or "其他"
	well_no = data.get("well_no") or frappe.db.get_value("Project", project, "project_name") or project
	subject = data.get("task_subject") or f"{well_no} {work_date} {shift}施工"
	filters = {"project": project, "subject": subject}
	existing = frappe.db.get_value("Task", filters, "name")
	values = {
		"subject": subject,
		"project": project,
		"status": data.get("task_status") or "Working",
		"progress": _mobile_float(data.get("task_progress") or data.get("progress") or 0),
		"exp_start_date": work_date,
		"exp_end_date": work_date,
		"description": data.get("construction_process") or data.get("raw_report") or "",
	}
	if existing:
		doc = frappe.get_doc("Task", existing)
		doc.update(values)
		doc.save(ignore_permissions=True)
		return doc.name
	doc = frappe.get_doc({"doctype": "Task", **values})
	doc.insert(ignore_permissions=True)
	return doc.name

def _create_timesheet_for_log(project: str, task: str, data: dict) -> str | None:
	total_hours = _mobile_float(data.get("timesheet_hours") or data.get("rig_total_hours") or data.get("pump_total_hours"))
	if total_hours <= 0:
		return None
	employee = get_current_employee_info()
	if not employee.get("name"):
		return None
	company = _get_default_company_for_mobile(employee)
	activity_type = _get_or_create_activity_type(data.get("activity_type") or "施工管理")
	doc = frappe.get_doc({
		"doctype": "Timesheet",
		"company": company,
		"employee": employee.get("name"),
		"parent_project": project,
		"start_date": data.get("work_date"),
		"end_date": data.get("work_date"),
		"note": data.get("construction_process") or data.get("raw_report") or "",
		"time_logs": [{
			"activity_type": activity_type,
			"project": project,
			"task": task,
			"hours": total_hours,
			"description": f"{data.get('shift') or ''} {data.get('well_no') or ''} 施工日报",
		}],
	})
	doc.insert(ignore_permissions=True)
	return doc.name

@frappe.whitelist()
def get_mobile_project_management_overview(project: str | None = None, limit: int = 100) -> dict:
	project_filters = {"name": project} if project else {}
	projects = frappe.get_list(
		"Project",
		filters=project_filters,
		fields=["name", "project_name", "status", "percent_complete", "expected_start_date", "expected_end_date", "customer", "company", "department", "priority", "project_type"],
		order_by="modified desc",
		limit=cint(limit) or 100,
		ignore_permissions=True,
	)
	task_filters = {"project": project} if project else {}
	tasks = frappe.get_list(
		"Task",
		filters=task_filters,
		fields=["name", "subject", "status", "priority", "progress", "exp_start_date", "exp_end_date", "project"],
		order_by="modified desc",
		limit=200,
		ignore_permissions=True,
	)
	log_filters = {"project": project} if project else {}
	logs = frappe.get_list(
		"Construction Work Log",
		filters=log_filters,
		fields=["name", "project", "project_name", "task", "status", "work_date", "shift", "team", "reporter", "well_no", "footage", "rig_total_hours", "pump_total_hours", "drill_pipe_count", "construction_process", "risk", "next_plan", "sand_flushing_hours", "standby_hours", "oil_added_vehicle", "oil_added_pump", "drill_pipe_73_count", "tubing_62_count", "kelly_count", "creation"],
		order_by="work_date desc, creation desc",
		limit=200,
		ignore_permissions=True,
	)
	timesheets = frappe.get_list(
		"Timesheet",
		filters={"parent_project": project} if project else {},
		fields=["name", "employee", "employee_name", "start_date", "end_date", "total_hours", "status", "docstatus", "note", "parent_project"],
		order_by="modified desc",
		limit=100,
		ignore_permissions=True,
	)
	return {"projects": projects, "tasks": tasks, "logs": logs, "timesheets": timesheets}

@frappe.whitelist(methods=["POST"])
def save_mobile_construction_work_log(**kwargs) -> dict:
	data = frappe._dict(kwargs)
	if data.get("doc") and isinstance(data.get("doc"), str):
		data = frappe._dict(json.loads(data.doc))
	elif data.get("doc") and isinstance(data.get("doc"), dict):
		data = frappe._dict(data.doc)

	project = _get_or_create_project_for_mobile(data.get("well_no"), data.get("project"), data.get("project_name"))
	task = data.get("task") or _create_or_update_task_for_log(project, data)
	timesheet = _create_timesheet_for_log(project, task, data)

	log_name = (data.get("name") or "").strip()
	doc = frappe.get_doc("Construction Work Log", log_name) if log_name and frappe.db.exists("Construction Work Log", log_name) else frappe.new_doc("Construction Work Log")
	
	doc.update({
		"project": project,
		"project_name": frappe.db.get_value("Project", project, "project_name") or project,
		"task": task,
		"status": data.get("status") or "Submitted",
		"work_date": data.get("work_date"),
		"shift": data.get("shift"),
		"team": data.get("team"),
		"reporter": data.get("reporter"),
		"employee": get_current_employee_info().get("name"),
		"well_no": data.get("well_no"),
		"manager": data.get("manager"),
		"artificial_bottom": _mobile_float(data.get("artificial_bottom")),
		"perforation_interval": data.get("perforation_interval"),
		"cement_return_height": _mobile_float(data.get("cement_return_height")),
		"pre_shift_meeting": data.get("pre_shift_meeting"),
		"work_time": data.get("work_time"),
		"construction_process": data.get("construction_process"),
		"blocked_depth": _mobile_float(data.get("blocked_depth")),
		"milling_after_depth": _mobile_float(data.get("milling_after_depth")),
		"footage": _mobile_float(data.get("footage")),
		"material_cost": data.get("material_cost"),
		"hired_vehicle_cost": data.get("hired_vehicle_cost"),
		"repair_cost": data.get("repair_cost"),
		"diesel_info": data.get("diesel_info"),
		"oil_added_vehicle": _mobile_float(data.get("oil_added_vehicle")),
		"oil_added_pump": _mobile_float(data.get("oil_added_pump")),
		"vehicle_oil_remaining": data.get("vehicle_oil_remaining"),
		"pump_oil_remaining": data.get("pump_oil_remaining"),
		"rig_total_hours": _mobile_float(data.get("rig_total_hours")),
		"rig_idle_hours": _mobile_float(data.get("rig_idle_hours")),
		"standby_hours": _mobile_float(data.get("standby_hours")),
		"tripping_hours": _mobile_float(data.get("tripping_hours")),
		"fishing_hours": _mobile_float(data.get("fishing_hours")),
		"milling_hours": _mobile_float(data.get("milling_hours")),
		"channel_finding_hours": _mobile_float(data.get("channel_finding_hours")),
		"forging_milling_hours": _mobile_float(data.get("forging_milling_hours")),
		"sand_flushing_hours": _mobile_float(data.get("sand_flushing_hours")),
		"pump_total_hours": _mobile_float(data.get("pump_total_hours")),
		"pump_idle_hours": _mobile_float(data.get("pump_idle_hours")),
		"pump_milling_hours": _mobile_float(data.get("pump_milling_hours")),
		"pump_forging_milling_hours": _mobile_float(data.get("pump_forging_milling_hours")),
		"pump_sand_flushing_hours": _mobile_float(data.get("pump_sand_flushing_hours")),
		"drill_pipe_count": _mobile_int(data.get("drill_pipe_count")),
		"drill_pipe_73_count": _mobile_int(data.get("drill_pipe_73_count")),
		"tubing_62_count": _mobile_int(data.get("tubing_62_count")),
		"kelly_count": _mobile_int(data.get("kelly_count")),
		"total_tools_count": _mobile_int(data.get("total_tools_count")),
		"workload_summary": data.get("workload_summary"),
		"risk": data.get("risk"),
		"next_plan": data.get("next_plan"),
		"raw_report": data.get("raw_report"),
	})

	# 保存子表：工序明细
	if data.get("activities"):
		doc.set("activities", [])
		for row in data.get("activities"):
			doc.append("activities", {
				"activity_type": row.get("activity_type"),
				"start_time": row.get("start_time"),
				"end_time": row.get("end_time"),
				"duration": _mobile_float(row.get("duration")),
				"description": row.get("description")
			})

	# 保存子表：工具明细
	if data.get("tools"):
		doc.set("tools", [])
		for row in data.get("tools"):
			doc.append("tools", {
				"tool_name": row.get("tool_name"),
				"outer_diameter": row.get("outer_diameter"),
				"length": _mobile_float(row.get("length")),
				"count": _mobile_int(row.get("count")),
				"total_length": _mobile_float(row.get("length")) * _mobile_int(row.get("count")),
				"remarks": row.get("remarks")
			})

	if log_name and frappe.db.exists("Construction Work Log", log_name):
		doc.save(ignore_permissions=True)
	else:
		doc.insert(ignore_permissions=True)

	frappe.db.commit()
	return {"log": doc.as_dict(), "project": project, "task": task, "timesheet": timesheet}
