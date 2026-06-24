package org.thp.cynox.migration.dto

import org.thp.cynox.models.User

case class InputUser(metaData: MetaData, user: User, organisations: Map[String, String], avatar: Option[InputAttachment])
