package org.thp.cynox.migration.dto

import java.util.Date

case class MetaData(id: String, createdBy: String, createdAt: Date, updatedBy: Option[String], updatedAt: Option[Date])
