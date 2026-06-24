package org.thp.cynox.migration.dto

import org.thp.cynox.models.Task

case class InputTask(metaData: MetaData, task: Task, owner: Option[String], organisations: Set[String])
