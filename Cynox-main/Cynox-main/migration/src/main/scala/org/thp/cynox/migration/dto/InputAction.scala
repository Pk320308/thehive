package org.thp.cynox.migration.dto

import org.thp.cynox.connector.cortex.models.Action

case class InputAction(metaData: MetaData, objectType: String, action: Action)
