package org.thp.cynox.migration.dto

import org.thp.cynox.models.Log

case class InputLog(metaData: MetaData, log: Log, attachments: Seq[InputAttachment])
