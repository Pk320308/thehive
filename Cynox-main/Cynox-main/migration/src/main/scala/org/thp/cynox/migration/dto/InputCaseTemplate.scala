package org.thp.cynox.migration.dto

import org.thp.cynox.dto.v1.InputCustomFieldValue
import org.thp.cynox.models.CaseTemplate

case class InputCaseTemplate(
    metaData: MetaData,
    caseTemplate: CaseTemplate,
    organisation: String,
    customFields: Seq[InputCustomFieldValue]
)
