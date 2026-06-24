package org.thp.cynox.migration.dto

import org.thp.cynox.models.Alert

case class InputAlert(
    metaData: MetaData,
    alert: Alert,
    caseId: Option[String],
    organisation: String,
    customFields: Map[String, Option[Any]],
    caseTemplate: Option[String]
) {
  def updateCaseId(caseId: Option[String]): InputAlert = copy(caseId = caseId)
}
