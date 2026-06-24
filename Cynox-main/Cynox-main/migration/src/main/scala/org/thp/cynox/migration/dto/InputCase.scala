package org.thp.cynox.migration.dto

import org.thp.cynox.models.Case

case class InputCase(
    `case`: Case,
    organisations: Map[String, String],
    customFields: Map[String, Option[Any]],
    metaData: MetaData
)
