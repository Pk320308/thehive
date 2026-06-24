package org.thp.cynox.migration.dto

import org.thp.cynox.models.Dashboard

case class InputDashboard(metaData: MetaData, organisation: Option[(String, Boolean)], dashboard: Dashboard)
