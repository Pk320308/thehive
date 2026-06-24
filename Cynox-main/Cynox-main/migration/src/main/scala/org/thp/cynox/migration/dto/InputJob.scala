package org.thp.cynox.migration.dto

import org.thp.cynox.connector.cortex.models.Job

case class InputJob(metaData: MetaData, job: Job)
