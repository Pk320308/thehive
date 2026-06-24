package org.thp.cynox.migration.dto

import org.thp.cynox.models.{Observable, ReportTag}

case class InputObservable(
    metaData: MetaData,
    observable: Observable,
    organisations: Set[String],
    dataOrAttachment: Either[String, InputAttachment],
    reportTags: Seq[ReportTag]
)
